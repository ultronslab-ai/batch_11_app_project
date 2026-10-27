"""
Incident & Complaint Management Store for OIL HSE Safety Intelligence System
Manages persistence, status lifecycle (Unchecked, Gonna be Visited, Solved),
audit trails, and administrative action notes.
"""

import os
import json
import datetime
import pandas as pd
from typing import List, Dict, Any, Optional

COMPLAINTS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'complaints_store.json')
SEED_CSV = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sample_sif_reports.csv')

STATUS_UNCHECKED = "Unchecked"
STATUS_GONNA_BE_VISITED = "Gonna be Visited"
STATUS_SOLVED = "Solved"

VALID_STATUSES = [STATUS_UNCHECKED, STATUS_GONNA_BE_VISITED, STATUS_SOLVED]

def _ensure_data_dir():
    d = os.path.dirname(COMPLAINTS_FILE)
    if not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

def _generate_default_seed_records() -> List[Dict[str, Any]]:
    """Seed initial records from sample_sif_reports.csv if complaints store doesn't exist yet."""
    records = []
    if os.path.exists(SEED_CSV):
        try:
            df = pd.read_csv(SEED_CSV)
            statuses_cycle = [STATUS_UNCHECKED, STATUS_GONNA_BE_VISITED, STATUS_SOLVED]
            for idx, row in df.iterrows():
                # distribute some realistic initial statuses
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
    return records

def load_all_complaints() -> List[Dict[str, Any]]:
    """Load all complaints from persistent JSON file."""
    _ensure_data_dir()
    if not os.path.exists(COMPLAINTS_FILE):
        initial = _generate_default_seed_records()
        save_all_complaints(initial)
        return initial
    
    try:
        with open(COMPLAINTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception as e:
        print(f"Error reading complaints file: {e}")
        return []

def save_all_complaints(complaints: List[Dict[str, Any]]) -> bool:
    """Save all complaints to persistent JSON storage."""
    _ensure_data_dir()
    try:
        with open(COMPLAINTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(complaints, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving complaints file: {e}")
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
    """Add a new complaint submitted by a field worker with default 'Unchecked' status."""
    complaints = load_all_complaints()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not custom_id:
        import random
        custom_id = f"OIL-CMP-{datetime.datetime.now().strftime('%y%m%d')}-{random.randint(100, 999)}"
    
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
        "sif_probability": sif_res.get('sif_probability', 20),
        "risk_score": sif_res.get('risk_score', 2.0),
        "risk_level": sif_res.get('risk_level', 'LOW RISK'),
        "risk_color": sif_res.get('risk_color', '#238636'),
        "lsr_tags": lsr_str,
        "explanation": sif_res.get('explanation', ''),
        "status": STATUS_UNCHECKED,  # New complaints start as Unchecked
        "assigned_inspector": "Unassigned",
        "admin_notes": "Complaint logged by field personnel. Awaiting HSE review.",
        "last_updated": now_str
    }
    
    # Prepend to list so newest is first
    complaints.insert(0, new_record)
    save_all_complaints(complaints)
    return new_record

def update_complaint_status(
    complaint_id: str,
    new_status: str,
    admin_notes: str = "",
    assigned_inspector: str = ""
) -> bool:
    """Update status, notes, and inspector for a specific complaint."""
    if new_status not in VALID_STATUSES:
        return False
    
    complaints = load_all_complaints()
    updated = False
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for c in complaints:
        if c.get("complaint_id") == complaint_id:
            c["status"] = new_status
            if admin_notes:
                c["admin_notes"] = admin_notes.strip()
            if assigned_inspector:
                c["assigned_inspector"] = assigned_inspector.strip()
            c["last_updated"] = now_str
            updated = True
            break
            
    if updated:
        save_all_complaints(complaints)
    return updated

def get_complaint_metrics(complaints: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Compute dashboard metrics for complaints."""
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
