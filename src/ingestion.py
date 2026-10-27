import re
import pandas as pd
import numpy as np

REQUIRED_COLUMNS = ['report_id', 'report_text', 'site', 'date', 'category']

REGIONAL_DICTIONARY = {
    # Hinglish & Hindi terms
    'uunchai': 'height', 'unchai': 'height', 'harness nahi': 'without safety harness',
    'belt nahi': 'without safety harness', 'gas test nahi': 'without gas testing',
    'welding near': 'hot work welding near', 'kaam kar raha': 'working',
    'latka load': 'suspended load', 'crane lift': 'crane lifting operations',
    'loto nahi': 'without lock out tag out isolation', 'power off nahi': 'without energy isolation',
    'khadda': 'trench excavation', 'mitti collapse': 'trench soil collapse',
    'speeding': 'speeding vehicle driving', 'gaadi': 'vehicle driving',
    'interlock bypass': 'bypassed safety interlock', 'tripping off': 'bypassed safety controls',
    'chot lag sakta': 'line of fire risk', 'pinch point': 'pinch zone line of fire',
    
    # Assamese & Bengali Script & Transliteration
    'উচ্চতাত': 'at height', 'কাম': 'working', 'গ্যাস': 'gas', 'পৰীক্ষা': 'testing',
    'বেল্ট': 'harness belt', 'বিপদ': 'danger hazard', 'দূৰ্ঘটনা': 'near miss accident',
    'পাইপ': 'pipe line', 'ওয়েল্ডিং': 'hot work welding', 'কনফাইন্ড': 'confined space',

    # South Indian Languages (Tamil, Telugu, Kannada, Malayalam & Transliteration)
    # Tamil
    'உயரத்தில்': 'at height', 'உயரம்': 'height', 'ஹார்னஸ் இல்லை': 'without safety harness',
    'கேஸ் டெஸ்ட் இல்லை': 'without gas testing', 'வேலை': 'working', 'அபாயம்': 'danger hazard',
    'harness illamal': 'without safety harness', 'uyarathil': 'at height', 'gas test illai': 'without gas testing',
    
    # Telugu
    'ఎత్తులో': 'at height', 'బెల్ట్ లేదు': 'without safety harness', 'గ్యాస్ టెస్ట్ లేదు': 'without gas testing',
    'పని': 'working', 'ప్రమాదం': 'danger hazard', 'ettulo': 'at height', 'belt lekunda': 'without safety harness',
    
    # Kannada
    'ಎತ್ತರದಲ್ಲಿ': 'at height', 'ಬೆಲ್ಟ್ ಇಲ್ಲ': 'without safety harness', 'ಗ್ಯಾಸ್ ಪರೀಕ್ಷೆ': 'without gas testing',
    'ಕೆಲಸ': 'working', 'ಅಪಾಯ': 'danger hazard', 'ettaradalli': 'at height', 'belt illa': 'without safety harness',
    
    # Malayalam
    'ഉയരത്തിൽ': 'at height', 'ബെൽറ്റ് ഇല്ല': 'without safety harness', 'ഗ്യാസ് ടെസ്റ്റ് ഇല്ല': 'without gas testing',
    'ജോലി': 'working', 'അപകടം': 'danger hazard', 'uyarathil': 'at height', 'belt illa': 'without safety harness'
}

def translate_regional_text(text: str) -> str:
    """Translate regional Indian languages (Hindi, Assamese, Bengali, Hinglish) to English HSE text."""
    if not isinstance(text, str) or not text.strip():
        return ""
    
    text_clean = text.lower().strip()
    translated = text_clean

    for reg_word, eng_trans in REGIONAL_DICTIONARY.items():
        if reg_word in translated:
            translated = translated.replace(reg_word, eng_trans)

    return clean_text(translated)

def clean_text(text: str) -> str:
    """Normalize free text safety report for NLP processing."""
    if not isinstance(text, str) or pd.isna(text):
        return ""
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def validate_and_clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """Validate CSV structure and clean data fields."""
    df_clean = df.copy()
    
    df_clean.columns = [str(c).strip().lower() for c in df_clean.columns]
    
    for col in REQUIRED_COLUMNS:
        if col not in df_clean.columns:
            if col == 'report_id':
                df_clean['report_id'] = [f"REP-GEN-{i+1:03d}" for i in range(len(df_clean))]
            elif col == 'site':
                df_clean['site'] = "OIL Facility - Unspecified"
            elif col == 'date':
                df_clean['date'] = "2026-01-01"
            elif col == 'category':
                df_clean['category'] = "Unsafe Act/Condition"
            elif col == 'report_text':
                df_clean['report_text'] = "No description provided."

    if 'activity' not in df_clean.columns:
        df_clean['activity'] = "General Operations"

    df_clean['report_text'] = df_clean['report_text'].astype(str).apply(translate_regional_text)
    df_clean['site'] = df_clean['site'].astype(str).fillna("OIL Site")
    df_clean['category'] = df_clean['category'].astype(str).fillna("General")
    df_clean['activity'] = df_clean['activity'].astype(str).fillna("General Maintenance")
    df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce').dt.strftime('%Y-%m-%d').fillna("2026-01-01")

    return df_clean
