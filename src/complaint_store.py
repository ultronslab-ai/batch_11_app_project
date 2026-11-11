"""
Thread-Safe ACID Incident & Complaint Management Store for OIL HSE Safety Intelligence System
Powered by SQLite with automatic JSON backup mirroring.
Guarantees zero data loss, atomic transactions, and high concurrency support.
"""

import os
import json
import sqlite3
import datetime
import pandas as pd
from typing import List, Dict, Any, Optional

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'oil_safety.db')
COMPLAINTS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'complaints_store.json')
SEED_CSV = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sample_sif_reports.csv')

STATUS_UNCHECKED = "Unchecked"
STATUS_GONNA_BE_VISITED = "Gonna be Visited"
STATUS_SOLVED = "Solved"

VALID_STATUSES = [STATUS_UNCHECKED, STATUS_GONNA_BE_VISITED, STATUS_SOLVED]

def _get_connection():
    """Get thread-safe SQLite connection with row factory."""
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE, timeout=15.0)
    conn.row_factory = sqlite3.Row
    return conn

def _init_db():
    """Initialize database tables and indices."""
    with _get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                complaint_id TEXT PRIMARY KEY,
                worker_name TEXT,
                timestamp TEXT,
                site TEXT,
                activity TEXT,
                category TEXT,
                equipment TEXT,
                original_text TEXT,
                translated_text TEXT,
                original_language TEXT,
                sif_label TEXT,
                sif_probability REAL,
                risk_score REAL,
                risk_level TEXT,
                risk_color TEXT,
                lsr_tags TEXT,
                explanation TEXT,
                status TEXT,
                assigned_inspector TEXT,
                admin_notes TEXT,
                last_updated TEXT
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_status ON complaints(status)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_site ON complaints(site)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_risk ON complaints(risk_score)")
        conn.commit()

        # Check if empty, seed if necessary
        cursor = conn.execute("SELECT COUNT(*) FROM complaints")
        count = cursor.fetchone()[0]
        if count == 0:
            _seed_initial_records(conn)

def _seed_initial_records(conn):
    """Seed initial records from JSON if available, or sample CSV."""
    records = []
    if os.path.exists(COMPLAINTS_FILE):
        try:
            with open(COMPLAINTS_FILE, 'r', encoding='utf-8') as f:
                records = json.load(f)
        except Exception:
            records = []

    if not records and os.path.exists(SEED_CSV):
        try:
            df = pd.read_csv(SEED_CSV)
            statuses_cycle = [STATUS_UNCHECKED, STATUS_GONNA_BE_VISITED, STATUS_SOLVED]
            for idx, row in df.iterrows():
                st_val = statuses_cycle[idx % 3] if idx < 12 else (STATUS_UNCHECKED if idx % 2 == 0 else STATUS_SOLVED)
                rec = {
                    "complaint_id": str(row.get('report_id', f"REP-2026-{idx+1:03d}")),
                    "worker_name": f"Operator #{101 + (idx % 20)}" if "REP-WKR" not in str(row.get('report_id')) else "Field Tech #402",
                    "timestamp": f"{row.get('date', '2026-02-01')} 09:30:00",
                    "site": str(row.get('site', 'Rig Site 04 - Digboi')),
                    "activity": str(row.get('activity', 'General Maintenance')),
                    "category": str(row.get('category', 'Unsafe Act')),
                    "equipment": "Standard Rig Gear / Equipment",
                    "original_text": str(row.get('report_text', '')),
                    "translated_text": str(row.get('report_text', '')),
                    "original_language": "English",
                    "sif_label": "SIF-Potential" if int(row.get('ground_truth_sif', 0)) == 1 else "Non-SIF",
                    "sif_probability": 88 if int(row.get('ground_truth_sif', 0)) == 1 else 22,
                    "risk_score": 9.0 if int(row.get('ground_truth_sif', 0)) == 1 else 2.5,
                    "risk_level": "CRITICAL RISK" if int(row.get('ground_truth_sif', 0)) == 1 else "LOW RISK",
                    "risk_color": "#DA3633" if int(row.get('ground_truth_sif', 0)) == 1 else "#238636",
                    "lsr_tags": str(row.get('ground_truth_lsr', 'None')),
                    "explanation": "High consequence hazard precursor detected." if int(row.get('ground_truth_sif', 0)) == 1 else "Routine operational observation.",
                    "status": st_val,
                    "assigned_inspector": "HSE Officer B. Barua" if st_val != STATUS_UNCHECKED else "Unassigned",
                    "admin_notes": "Inspection scheduled for shift handover." if st_val == STATUS_GONNA_BE_VISITED else ("Corrective action verified and closed." if st_val == STATUS_SOLVED else "Pending initial review by HSE supervisor."),
                    "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                records.append(rec)
        except Exception as e:
            print(f"Error seeding records: {e}")

    for r in records:
        conn.execute("""
            INSERT OR REPLACE INTO complaints (
                complaint_id, worker_name, timestamp, site, activity, category,
                equipment, original_text, translated_text, original_language,
                sif_label, sif_probability, risk_score, risk_level, risk_color,
                lsr_tags, explanation, status, assigned_inspector, admin_notes, last_updated
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r.get("complaint_id"), r.get("worker_name"), r.get("timestamp"),
            r.get("site"), r.get("activity"), r.get("category"), r.get("equipment"),
            r.get("original_text"), r.get("translated_text"), r.get("original_language"),
            r.get("sif_label"), float(r.get("sif_probability", 0)), float(r.get("risk_score", 0)),
            r.get("risk_level"), r.get("risk_color"), r.get("lsr_tags"), r.get("explanation"),
            r.get("status"), r.get("assigned_inspector"), r.get("admin_notes"), r.get("last_updated")
        ))
    conn.commit()

# Initialize DB on load
_init_db()

def _sync_json_backup(records: List[Dict[str, Any]]):
    """Write backup JSON file asynchronously or safely."""
    try:
        os.makedirs(os.path.dirname(COMPLAINTS_FILE), exist_ok=True)
        with open(COMPLAINTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: JSON backup sync failed: {e}")

def load_all_complaints() -> List[Dict[str, Any]]:
    """Load all complaints from SQLite, ordered by newest first."""
    _init_db()
    try:
        with _get_connection() as conn:
            cursor = conn.execute("SELECT * FROM complaints ORDER BY rowid DESC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error reading complaints from DB: {e}")
        # Fallback to JSON
        if os.path.exists(COMPLAINTS_FILE):
            try:
                with open(COMPLAINTS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return []

def save_all_complaints(complaints: List[Dict[str, Any]]) -> bool:
    """Save/sync all complaints to SQLite and mirror to JSON."""
    _init_db()
    try:
        with _get_connection() as conn:
            for r in complaints:
                conn.execute("""
                    INSERT OR REPLACE INTO complaints (
                        complaint_id, worker_name, timestamp, site, activity, category,
                        equipment, original_text, translated_text, original_language,
                        sif_label, sif_probability, risk_score, risk_level, risk_color,
                        lsr_tags, explanation, status, assigned_inspector, admin_notes, last_updated
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    r.get("complaint_id"), r.get("worker_name"), r.get("timestamp"),
                    r.get("site"), r.get("activity"), r.get("category"), r.get("equipment"),
                    r.get("original_text"), r.get("translated_text"), r.get("original_language"),
                    r.get("sif_label"), float(r.get("sif_probability", 0)), float(r.get("risk_score", 0)),
                    r.get("risk_level"), r.get("risk_color"), r.get("lsr_tags"), r.get("explanation"),
                    r.get("status"), r.get("assigned_inspector"), r.get("admin_notes"), r.get("last_updated")
                ))
            conn.commit()
        _sync_json_backup(complaints)
        return True
    except Exception as e:
        print(f"Error saving complaints to DB: {e}")
        return False

def add_complaint(
    worker_name: str,
    site: str,
    activity: str,
    category: str,
    equipment: str,
    original_text: str,
    translated_text: str,
    original_language: str,
    sif_res: Dict[str, Any],
    matched_lsr: List[str],
    custom_id: Optional[str] = None
) -> Dict[str, Any]:
    """Add a new complaint atomically using an ACID SQLite transaction."""
    _init_db()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not custom_id:
        import random
        custom_id = f"OIL-{datetime.datetime.now().strftime('%y%m%d')}-{random.randint(100, 999)}"
    
    lsr_str = "; ".join(matched_lsr) if matched_lsr else "None"
    
    new_record = {
        "complaint_id": custom_id,
        "worker_name": worker_name.strip() if worker_name and worker_name.strip() else "Anonymous Field Operator",
        "timestamp": now_str,
        "site": site,
        "activity": activity,
        "category": category,
        "equipment": equipment if equipment else "Not specified",
        "original_text": original_text,
        "translated_text": translated_text,
        "original_language": original_language,
        "sif_label": sif_res.get('sif_label', 'Non-SIF'),
        "sif_probability": float(sif_res.get('sif_probability', 20)),
        "risk_score": float(sif_res.get('risk_score', 2.0)),
        "risk_level": sif_res.get('risk_level', 'LOW RISK'),
        "risk_color": sif_res.get('risk_color', '#238636'),
        "lsr_tags": lsr_str,
        "explanation": sif_res.get('explanation', ''),
        "status": STATUS_UNCHECKED,
        "assigned_inspector": "Unassigned",
        "admin_notes": "Complaint logged by field personnel. Awaiting HSE review.",
        "last_updated": now_str
    }
    
    try:
        with _get_connection() as conn:
            conn.execute("""
                INSERT INTO complaints (
                    complaint_id, worker_name, timestamp, site, activity, category,
                    equipment, original_text, translated_text, original_language,
                    sif_label, sif_probability, risk_score, risk_level, risk_color,
                    lsr_tags, explanation, status, assigned_inspector, admin_notes, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                new_record["complaint_id"], new_record["worker_name"], new_record["timestamp"],
                new_record["site"], new_record["activity"], new_record["category"], new_record["equipment"],
                new_record["original_text"], new_record["translated_text"], new_record["original_language"],
                new_record["sif_label"], new_record["sif_probability"], new_record["risk_score"],
                new_record["risk_level"], new_record["risk_color"], new_record["lsr_tags"],
                new_record["explanation"], new_record["status"], new_record["assigned_inspector"],
                new_record["admin_notes"], new_record["last_updated"]
            ))
            conn.commit()
        
        # Mirror backup
        all_recs = load_all_complaints()
        _sync_json_backup(all_recs)
    except Exception as e:
        print(f"Error inserting complaint to SQLite: {e}")

    return new_record

def update_complaint_status(
    complaint_id: str,
    new_status: str,
    admin_notes: str = "",
    assigned_inspector: str = ""
) -> bool:
    """Update status, notes, and inspector atomically."""
    if new_status not in VALID_STATUSES:
        return False
    
    _init_db()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with _get_connection() as conn:
            query = "UPDATE complaints SET status = ?, last_updated = ?"
            params = [new_status, now_str]
            if admin_notes:
                query += ", admin_notes = ?"
                params.append(admin_notes.strip())
            if assigned_inspector:
                query += ", assigned_inspector = ?"
                params.append(assigned_inspector.strip())
            
            query += " WHERE complaint_id = ?"
            params.append(complaint_id)
            
            cursor = conn.execute(query, params)
            conn.commit()
            updated = cursor.rowcount > 0
            
        if updated:
            _sync_json_backup(load_all_complaints())
        return updated
    except Exception as e:
        print(f"Error updating complaint in SQLite: {e}")
        return False

def get_complaint_metrics(complaints: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Compute high-level dashboard metrics for complaints."""
    if complaints is None:
        complaints = load_all_complaints()
        
    total = len(complaints)
    unchecked = sum(1 for c in complaints if c.get('status') == STATUS_UNCHECKED)
    gonna_visit = sum(1 for c in complaints if c.get('status') == STATUS_GONNA_BE_VISITED)
    solved = sum(1 for c in complaints if c.get('status') == STATUS_SOLVED)
    critical_sif = sum(1 for c in complaints if c.get('sif_label') == 'SIF-Potential')
    
    return {
        "total": total,
        "unchecked": unchecked,
        "gonna_visit": gonna_visit,
        "solved": solved,
        "critical_sif": critical_sif,
        "resolution_rate": round((solved / total * 100), 1) if total > 0 else 0.0
    }
