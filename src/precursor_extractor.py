import re
import pandas as pd
from collections import Counter

EQUIPMENT_KEYWORDS = {
    'Scaffolding': ['scaffold', 'scaffolding', 'platform', 'plank'],
    'Crane & Hoist': ['crane', 'hoist', 'wire rope', 'sling', 'rigging', 'forklift'],
    'Harness & Lifeline': ['harness', 'lanyard', 'life line', 'snap hook'],
    'Valves & Piping': ['psv', 'manifold', 'pipeline', 'valve', 'flange'],
    'Electrical Equipment': ['breaker', '11kv', 'cable', 'panel', 'busbar', 'generator'],
    'Vessels & Tanks': ['vessel', 'storage tank', 'oil pit'],
    'Vehicles & Tankers': ['tanker', 'truck', 'pickup', 'vehicle'],
    'Excavator & Trench': ['excavator', 'trench', 'digging', 'bucket']
}

BARRIER_FAILURES = {
    'PPE Non-Compliance': ['harness', 'seatbelt', 'eye protection', 'helmet', 'lanyard'],
    'Isolation & LOTO Failure': ['loto', 'isolation', 'lock-out', 'tag-out', 'lockout', 'energized'],
    'Permit & Gas Testing Bypass': ['gas test', 'permit', 'ptw', 'gas testing', 'ventilation'],
    'Equipment Degradation / Uncertified': ['damaged', 'frayed', 'broken wire', 'corrosion', 'uncertified'],
    'Procedural / Interlock Override': ['bypassed', 'interlock', 'unattended', 'speeding', 'override']
}

class PrecursorExtractor:
    def __init__(self):
        pass

    def extract_precursors(self, text: str) -> dict:
        """Extract equipment, barrier failures, and unsafe condition details from text."""
        text_clean = str(text).lower()

        # Equipment extraction
        equip_found = []
        for eq_cat, kws in EQUIPMENT_KEYWORDS.items():
            if any(kw in text_clean for kw in kws):
                equip_found.append(eq_cat)

        # Barrier failure extraction
        barriers_found = []
        for b_cat, kws in BARRIER_FAILURES.items():
            if any(kw in text_clean for kw in kws):
                barriers_found.append(b_cat)

        return {
            "equipment": equip_found if equip_found else ["General Machinery"],
            "barrier_failures": barriers_found if barriers_found else ["Behavioral / Procedural"],
        }

    def extract_top_phrases(self, texts: list, top_n: int = 10) -> list:
        """Extract top recurring n-gram phrases across safety reports."""
        words_list = []
        stopwords = {'was', 'were', 'the', 'and', 'with', 'for', 'near', 'from', 'without', 'during', 'that', 'this', 'into', 'under', 'over', 'observed', 'area'}
        
        bigrams = []
        for txt in texts:
            tokens = [w.strip('.,;:"()') for w in str(txt).lower().split() if len(w) > 2]
            tokens = [t for t in tokens if t not in stopwords]
            for i in range(len(tokens) - 1):
                bigrams.append(f"{tokens[i]} {tokens[i+1]}")
                
        counts = Counter(bigrams)
        return counts.most_common(top_n)
