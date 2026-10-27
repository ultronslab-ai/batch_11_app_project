import re
import pandas as pd

# The 10 Official IOGP Life-Saving Rules with domain keywords
LSR_RULES = {
    "Energy Isolation": [
        "isolation", "isolated", "loto", "lockout", "tagout", "lock-out", "tag-out",
        "live wire", "electrical panel", "11kv", "breaker", "energized", "grounding", "neutral cable"
    ],
    "Hot Work": [
        "hot work", "welding", "grinding", "cutting", "spark", "flame", "torch",
        "flare stack", "diesel drum", "combustible", "gas test", "flammable gas"
    ],
    "Confined Space": [
        "confined space", "vessel", "storage tank", "sludge", "oil pit", "oxygen", "toxic gas",
        "entry hatch", "ventilation", "atmosphere test", "gas testing"
    ],
    "Line of Fire": [
        "line of fire", "pinch zone", "suspended load", "falling object", "rotating",
        "kelly spinner", "tong line", "struck by", "swinging bucket", "flying debris"
    ],
    "Working at Height": [
        "height", "scaffolding", "harness", "lanyard", "life line", "ladder", "platform",
        "roof", "mast", "fall protection", "plank", "unanchored"
    ],
    "Lifting Operations": [
        "lifting", "crane", "hoist", "sling", "wire rope", "rigging", "rigger",
        "forklift", "500kg", "12-ton", "load", "hook"
    ],
    "Driving": [
        "driving", "driver", "vehicle", "tanker", "truck", "speeding", "seatbelt",
        "mobile phone", "reversing", "lease road", "parking"
    ],
    "Excavation": [
        "excavation", "trench", "shoring", "buried cable", "earth moving", "soil collapse",
        "loose soil", "ditch", "digging"
    ],
    "Permit to Work": [
        "permit to work", "ptw", "work permit", "permit issued", "tool-box talk",
        "shift handover", "green tag", "supervisor approval"
    ],
    "Bypassing Safety Controls": [
        "bypassing", "bypassed", "interlock", "safety trip", "alarm muted", "override",
        "safety interlock", "psv isolated", "guard removed", "unattended hatch"
    ]
}

class LSRTagger:
    def __init__(self):
        pass

    def tag_text(self, text: str) -> list:
        """Tag one or more applicable IOGP Life-Saving Rules."""
        text_clean = str(text).lower()
        matched_rules = []

        for rule, keywords in LSR_RULES.items():
            for kw in keywords:
                # Word boundary search for precise matching
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, text_clean):
                    if rule not in matched_rules:
                        matched_rules.append(rule)
                    break

        return matched_rules if matched_rules else ["General Operations"]

    def tag_batch(self, df: pd.DataFrame, text_col: str = 'report_text') -> pd.DataFrame:
        """Add lsr_tags column to dataframe."""
        res_df = df.copy()
        tags_list = []
        tags_str_list = []

        for txt in res_df[text_col]:
            rules = self.tag_text(txt)
            tags_list.append(rules)
            tags_str_list.append("; ".join(rules))

        res_df['lsr_tags_list'] = tags_list
        res_df['lsr_tags'] = tags_str_list
        return res_df
