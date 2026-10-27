"""
Inner Form Options & Dynamic Content Localization Engine for OIL HSE System
Provides deep translation for Field Worker form dropdowns (Sites, Activities, Categories, Statuses)
across all supported languages (English, Hindi, Assamese, Bengali, Tamil, Telugu, Kannada, Malayalam).
Guarantees bidirectional mapping back to canonical HSE English standards.
"""

from typing import List, Dict, Any, Optional

SITE_MAP: Dict[str, Dict[str, str]] = {
    "Rig Site 04 - Digboi": {
        "en": "Rig Site 04 - Digboi",
        "hi": "रिग साइट 04 - डिगबोई (Digboi)",
        "as": "ৰিগ ছাইট 04 - ডিগবৈ (Digboi)",
        "bn": "রিগ সাইট 04 - ডিগবই (Digboi)",
        "ta": "ரிக் தளம் 04 - திக்போய் (Digboi)",
        "te": "రిగ్ సైట్ 04 - డిగ్బోయ్ (Digboi)",
        "kn": "ರಿಗ್ ಸೈಟ್ 04 - ಡಿಗ್ಬೋಯ್ (Digboi)",
        "ml": "റിഗ് സൈറ്റ് 04 - ദിഗ്‌ബോയ് (Digboi)"
    },
    "Compressor Station 02 - Duliajan": {
        "en": "Compressor Station 02 - Duliajan",
        "hi": "कंप्रेसर स्टेशन 02 - दुलियाजान (Duliajan)",
        "as": "কম্প্ৰেছৰ ষ্টেচন 02 - দুলীয়াজান (Duliajan)",
        "bn": "কম্প্রেসার স্টেশন 02 - দুলিয়াজান (Duliajan)",
        "ta": "கம்ப்ரசர் நிலையம் 02 - துலியாஜான்",
        "te": "కంప్రెసర్ స్టేషన్ 02 - దులియాజాన్",
        "kn": "ಸಂಕೋಚಕ ಕೇಂದ್ರ 02 - ದುಲಿಯಾಜಾನ್",
        "ml": "കംപ്രസ്സർ സ്റ്റേഷൻ 02 - ദുലിയാജാൻ"
    },
    "Pipeline Sector 07 - Moran": {
        "en": "Pipeline Sector 07 - Moran",
        "hi": "पाइपलाइन सेक्टर 07 - मोरन (Moran)",
        "as": "পাইপলাইন ছেক্টৰ 07 - মৰাণ (Moran)",
        "bn": "পাইপলাইন সেক্টর 07 - মোরান (Moran)",
        "ta": "குழாய் பிரிவு 07 - மோரான்",
        "te": "పైప్‌లైన్ సెక్టార్ 07 - మోరన్",
        "kn": "ಪೈಪ್‌ಲೈನ್ ಸೆಕ್ಟರ್ 07 - ಮೊರಾನ್",
        "ml": "പൈപ്പ് ലൈൻ സെക്ടർ 07 - മോറാൻ"
    },
    "Crude Distillation Unit - Numaligarh": {
        "en": "Crude Distillation Unit - Numaligarh",
        "hi": "कच्चा आसवन इकाई - नुमालीगढ़ (CDU)",
        "as": "খাৰুৱা তেল পাতন গোট - নুমলীগড় (CDU)",
        "bn": "অপরিশোধিত তেল পাতন - নুমালিগড় (CDU)",
        "ta": "கச்சா எண்ணெய் வடித்தல் பிரிவு - நுமலிகர்",
        "te": "క్రూడ్ డిస్టిలేషన్ యూనిట్ - నుమాలీగఢ్",
        "kn": "ಕಚ್ಚಾ ತೈಲ ಶುದ್ಧೀಕರಣ ಘಟಕ - ನುಮಾಲಿಗಢ",
        "ml": "ക്രൂഡ് ഡിസ്റ്റിലേഷൻ യൂണിറ്റ് - നുമാലിഗഡ്"
    },
    "Drilling Rig 12 - Makum": {
        "en": "Drilling Rig 12 - Makum",
        "hi": "ड्रिलिंग रिग 12 - माकुम (Makum)",
        "as": "ড্ৰিলিং ৰিগ 12 - মাকুম (Makum)",
        "bn": "ড্রিলিং রিগ 12 - মাকুম (Makum)",
        "ta": "துளையிடும் ரிக் 12 - மக்கும்",
        "te": "డ్రిల్లింగ్ రిగ్ 12 - మాకుమ్",
        "kn": "ಡ್ರಿಲ್ಲಿಂಗ್ ರಿಗ್ 12 - ಮಾಕುಮ್",
        "ml": "ഡ്രില്ലിംഗ് റിഗ് 12 - മാക്കും"
    },
    "Gas Gathering Station 01 - Jorhat": {
        "en": "Gas Gathering Station 01 - Jorhat",
        "hi": "गैस संग्रहण स्टेशन 01 - जोरहाट (GGS)",
        "as": "গেছ সংগ্ৰহ কেন্দ্ৰ 01 - যোৰহাট (GGS)",
        "bn": "গ্যাস সংগ্রহ কেন্দ্র 01 - জোরহাট (GGS)",
        "ta": "எரிவாயு சேகரிப்பு நிலையம் 01 - ஜோர்ஹட்",
        "te": "గ్యాస్ సేకరణ కేంద్రం 01 - జోర్హాట్",
        "kn": "ಅನಿಲ ಸಂಗ್ರಹಣಾ ಕೇಂದ್ರ 01 - ಜೋರ್ಹತ್",
        "ml": "ഗ്യാസ് ശേഖരണ സ്റ്റേഷൻ 01 - ജോർഹട്ട്"
    },
    "Other OIL Site": {
        "en": "Other OIL Site",
        "hi": "अन्य OIL संचालन स्थल (Other OIL Site)",
        "as": "অন্যান্য OIL কাৰ্যক্ষেত্ৰ (Other OIL Site)",
        "bn": "অন্যান্য OIL ক্ষেত্র (Other OIL Site)",
        "ta": "மற்ற OIL தளம்",
        "te": "ఇతర OIL సైట్",
        "kn": "ಇತರ OIL ಸೈಟ್",
        "ml": "മറ്റ് OIL സൈറ്റ്"
    }
}

ACTIVITY_MAP: Dict[str, Dict[str, str]] = {
    "Working at Height": {
        "en": "Working at Height",
        "hi": "ऊंचाई पर कार्य (Working at Height)",
        "as": "উচ্চতাত কাম কৰা (Working at Height)",
        "bn": "উচ্চতায় কাজ করা (Working at Height)",
        "ta": "உயரத்தில் வேலை செய்தல் (Working at Height)",
        "te": "ఎత్తులో పని చేయడం (Working at Height)",
        "kn": "ಎತ್ತರದಲ್ಲಿ ಕೆಲಸ ಮಾಡುವುದು (Working at Height)",
        "ml": "ഉയരത്തിൽ ജോലി ചെയ്യൽ (Working at Height)"
    },
    "Hot Work": {
        "en": "Hot Work",
        "hi": "हॉट वर्क - वेल्डिंग/कटिंग (Hot Work)",
        "as": "হট ৱাৰ্ক - ৱেল্ডিং/কাটিং (Hot Work)",
        "bn": "হট ওয়ার্ক - ওয়েল্ডিং/কাটিং (Hot Work)",
        "ta": "வெப்பப் பணி - வெல்டிங்/கட்டிங்",
        "te": "హాట్ వర్క్ - వెల్డింగ్/కట్టింగ్",
        "kn": "ಹಾಟ್ ವರ್ಕ್ - ವೆಲ್ಡಿಂಗ್/ಕಟಿಂಗ್",
        "ml": "ഹോട്ട് വർക്ക് - വെൽഡിംഗ്"
    },
    "Tank Maintenance": {
        "en": "Tank Maintenance",
        "hi": "टैंक रखरखाव व सफाई (Tank Maintenance)",
        "as": "টেংক ৰক্ষণাবেক্ষণ (Tank Maintenance)",
        "bn": "ট্যাঙ্ক রক্ষণাবেক্ষণ (Tank Maintenance)",
        "ta": "தொட்டி பராமரிப்பு பணி",
        "te": "ట్యాంక్ నిర్వహణ పనులు",
        "kn": "ಟ್ಯಾಂಕ್ ನಿರ್ವಹಣೆ",
        "ml": "ടാങ്ക് അറ്റകുറ്റപ്പണി"
    },
    "Lifting Operations": {
        "en": "Lifting Operations",
        "hi": "क्रेन लिफ्टिंग ऑपरेशन्स (Lifting Operations)",
        "as": "ক্ৰেন লিফটিং কাৰ্যসূচী (Lifting Operations)",
        "bn": "ক্রেন লিফটিং অপারেশন (Lifting Operations)",
        "ta": "கிரேன் தூக்கும் பணிகள்",
        "te": "క్రేన్ లిఫ్టింగ్ పనులు",
        "kn": "ಕ್ರೇನ್ ಲಿಫ್ಟಿಂಗ್ ಕೆಲಸಗಳು",
        "ml": "ക്രെയിൻ ലിഫ്റ്റിംഗ് ജോലികൾ"
    },
    "Pipeline Maintenance": {
        "en": "Pipeline Maintenance",
        "hi": "पाइपलाइन मरम्मत व निरीक्षण (Pipeline Maintenance)",
        "as": "পাইপলাইন মেৰামতি আৰু পৰিদৰ্শন",
        "bn": "পাইপলাইন মেরামত ও পরিদর্শন",
        "ta": "குழாய் பராமரிப்பு மற்றும் ஆய்வு",
        "te": "పైప్‌లైన్ నిర్వహణ మరియు తనిఖీ",
        "kn": "ಪೈಪ್‌ಲೈನ್ ನಿರ್ವಹಣೆ",
        "ml": "പൈപ്പ് ലൈൻ അറ്റകുറ്റപ്പണി"
    },
    "Transport & Logistics": {
        "en": "Transport & Logistics",
        "hi": "परिवहन व भारी वाहन संचालन (Transport & Logistics)",
        "as": "পৰিবহন আৰু গধুৰ বাহন চালনা",
        "bn": "পরিবহন ও ভারী যান চলাচল",
        "ta": "போக்குவரத்து மற்றும் தளவாடங்கள்",
        "te": "రవాణా మరియు లాజిస్టిక్స్",
        "kn": "ಸಾರಿಗೆ ಮತ್ತು ಲಾಜಿಸ್ಟಿಕ್ಸ್",
        "ml": "ഗതാഗതവും ലോജിസ്റ്റിക്സും"
    },
    "Excavation": {
        "en": "Excavation",
        "hi": "खुदाई व ट्रेंच कार्य (Excavation)",
        "as": "খনন আৰু খাৱৈ কাৰ্য (Excavation)",
        "bn": "খনন ও পরিখা খনন (Excavation)",
        "ta": "நிலம் தோண்டுதல் பணி",
        "te": "తవ్వకం పనులు",
        "kn": "ಅಗೆಯುವ ಕೆಲಸಗಳು",
        "ml": "ഖനന ജോലികൾ"
    },
    "Electrical Repair": {
        "en": "Electrical Repair",
        "hi": "विद्युत पैनल व केबल मरम्मत (Electrical Repair)",
        "as": "বৈদ্যুতিক পেনেল আৰু মেৰামতি",
        "bn": "বৈদ্যুতিক প্যানেল ও মেরামত",
        "ta": "மின்சார குழு மற்றும் பழுதுபார்ப்பு",
        "te": "విద్యుత్ ప్యానెల్ మరియు మరమ్మత్తులు",
        "kn": "ವಿದ್ಯುತ್ ಪ್ಯಾನೆಲ್ ಮತ್ತು ರಿಪೇರಿ",
        "ml": "വൈദ്യുത അറ്റകുറ്റപ്പണി"
    },
    "General Maintenance": {
        "en": "General Maintenance",
        "hi": "सामान्य संयंत्र रखरखाव (General Maintenance)",
        "as": "সাধাৰণ উদ্যোগ মেৰামতি",
        "bn": "সাধারণ প্ল্যান্ট রক্ষণাবেক্ষণ",
        "ta": "பொது பராமரிப்பு பணி",
        "te": "సాధారణ నిర్వహణ",
        "kn": "ಸಾಮಾನ್ಯ ನಿರ್ವಹಣೆ",
        "ml": "പൊതു അറ്റകുറ്റപ്പണി"
    },
    "Drilling Operations": {
        "en": "Drilling Operations",
        "hi": "रिग ड्रिलिंग संचालन (Drilling Operations)",
        "as": "ৰিগ ড্ৰিলিং কাম-কাজ",
        "bn": "রিগ ড্রিলিং পরিচালনা",
        "ta": "துளையிடும் செயல்பாடுகள்",
        "te": "డ్రిల్లింగ్ కార్యకలాపాలు",
        "kn": "ಕೊರೆಯುವ ಕಾರ್ಯಾಚರಣೆಗಳು",
        "ml": "ഡ്രില്ലിംഗ് പ്രവർത്തനങ്ങൾ"
    }
}

CATEGORY_MAP: Dict[str, Dict[str, str]] = {
    "Unsafe Act": {
        "en": "⚠️ Unsafe Act (Human Behavior / Non-Compliance)",
        "hi": "⚠️ असुरक्षित कार्य (मानवीय व्यवहार / नियम उल्लंघन)",
        "as": "⚠️ অসুৰক্ষিত কাৰ্য (মানৱ আচৰণ / নিয়ম উলংঘন)",
        "bn": "⚠️ অসুরক্ষিত কাজ (মানবিক আচরণ / নিয়ম লঙ্ঘন)",
        "ta": "⚠️ பாதுகாப்பற்ற செயல் (மனித நடத்தை)",
        "te": "⚠️ అసురక్షిత చర్య (మానవ ప్రవర్తన)",
        "kn": "⚠️ ಅಸುರಕ್ಷಿತ ಕೃತ್ಯ (ಮಾನವ ನಡವಳಿಕೆ)",
        "ml": "⚠️ അരക്ഷിതമായ പ്രവർത്തനം"
    },
    "Unsafe Condition": {
        "en": "🚧 Unsafe Condition (Physical / Equipment Hazard)",
        "hi": "🚧 असुरक्षित स्थिति (भौतिक / उपकरण खतरा)",
        "as": "🚧 অসুৰক্ষিত পৰিৱেশ (সঁজুলি বিপদ)",
        "bn": "🚧 অসুরক্ষিত পরিবেশ (সরঞ্জাম ঝুঁকি)",
        "ta": "🚧 பாதுகாப்பற்ற நிலை (உபகரண ஆபத்து)",
        "te": "🚧 అసురక్షిత పరిస్థితి (పరికర ప్రమాదం)",
        "kn": "🚧 ಅಸುರಕ್ಷಿತ ಸ್ಥಿತಿ (ಉಪಕರಣ ಅಪಾಯ)",
        "ml": "🚧 അരക്ഷിതമായ സാഹചര്യം"
    },
    "Near Miss": {
        "en": "⚡ Near Miss (Incident Narrowly Avoided)",
        "hi": "⚡ नियर मिस (बाल-बाल बचा हादसा)",
        "as": "⚡ নিয়াৰ মিছ (কথমপি ৰক্ষা পৰা ঘটনা)",
        "bn": "⚡ নিয়ার মিস (অল্পের জন্য রক্ষা পাওয়া)",
        "ta": "⚡ மயிரிழையில் தப்பிய விபத்து",
        "te": "⚡ ప్రమాదం తృటిలో తప్పిన ఘటన",
        "kn": "⚡ ಕೂದಲೆಳೆಯ ಅಂತರದಲ್ಲಿ ತಪ್ಪಿದ ಅಪಾಯ",
        "ml": "⚡ തലനാരിഴയ്ക്ക് ഒഴിവായ അപകടം"
    }
}

STATUS_MAP: Dict[str, Dict[str, str]] = {
    "Unchecked": {
        "en": "🔴 Unchecked (Pending Review)",
        "hi": "🔴 अनचेक - समीक्षा लंबित (Unchecked)",
        "as": "🔴 পৰীক্ষা নোহোৱা - বিবেচনাধীন (Unchecked)",
        "bn": "🔴 অপরীক্ষিত - পর্যালোচনা বাকি (Unchecked)",
        "ta": "🔴 சரிபார்க்கப்படவில்லை - நிலுவையில்",
        "te": "🔴 పరిశీలించబడలేదు - పెండింగ్",
        "kn": "🔴 ಪರಿಶೀಲಿಸಲಾಗಿಲ್ಲ - ಬಾಕಿ ಇದೆ",
        "ml": "🔴 പരിശോധിച്ചിട്ടില്ല - ശേഷിക്കുന്നു"
    },
    "Gonna be Visited": {
        "en": "🟠 Gonna be Visited (Inspection Scheduled)",
        "hi": "🟠 निरीक्षण निर्धारित - दौरा होगा (Gonna be Visited)",
        "as": "🟠 পৰিদৰ্শন নিৰ্ধাৰিত - দল যাব (Gonna be Visited)",
        "bn": "🟠 পরিদর্শন নির্ধারিত - টিম যাবে (Gonna be Visited)",
        "ta": "🟠 ஆய்வு திட்டமிடப்பட்டது - பார்வையிடப்படும்",
        "te": "🟠 తనిఖీ షెడ్యూల్ చేయబడింది - బృందం వెళ్తుంది",
        "kn": "🟠 ತಪಾಸಣೆ ನಿಗದಿಯಾಗಿದೆ - ಭೇಟಿ ನೀಡಲಾಗುವುದು",
        "ml": "🟠 പരിശോധന നിശ്ചയിച്ചു - സന്ദർശിക്കും"
    },
    "Solved": {
        "en": "🟢 Solved (Hazard Mitigated & Closed)",
        "hi": "🟢 हल हो गया - खतरा दूर किया गया (Solved)",
        "as": "🟢 সমাধান হ'ল - বিপদ দূৰ কৰা হ'ল (Solved)",
        "bn": "🟢 সমাধান হয়েছে - বিপদমুক্ত ও সমাপ্ত (Solved)",
        "ta": "🟢 தீர்க்கப்பட்டது - ஆபத்து நீக்கப்பட்டது",
        "te": "🟢 పరిష్కరించబడింది - ప్రమాదం తొలగించబడింది",
        "kn": "🟢 ಪರಿಹರಿಸಲಾಗಿದೆ - ಅಪಾಯ ನಿವಾರಣೆಯಾಗಿದೆ",
        "ml": "🟢 പരിഹരിച്ചു - അപകടം ഒഴിവാക്കി"
    }
}

EXTRA_UI_STRINGS: Dict[str, Dict[str, str]] = {
    "en": {
        "tab_complaints": "🚨 Incident Complaints & Governance",
        "tab_tracking": "🔍 Track My Complaint Status",
        "role_worker": "👷 Field Worker Portal (1-Click Public Access - No Password)",
        "role_admin": "🔐 HSE Executive Admin Portal (Secure Login)",
        "admin_badge": "👑 Role: HSE Executive Administrator",
        "worker_badge": "👷 Role: Field Worker / Public Reporter (Common Access)",
        "admin_login_title": "🔐 OIL HSE Executive Administration Access",
        "admin_login_sub": "Enter authorized safety officer credentials to review, schedule visits, and resolve complaints.",
        "lbl_admin_user": "Admin Username:",
        "lbl_admin_pass": "Admin Password:",
        "btn_login_admin": "🔓 Authenticate & Access Admin Portal",
        "btn_logout_admin": "🔒 Logout Admin",
        "lbl_status_filter": "Filter by Resolution Status:",
        "lbl_update_status": "Update Incident Status & Log Action",
        "status_unchecked": "Unchecked",
        "status_gonna_visit": "Gonna be Visited",
        "status_solved": "Solved",
        "lbl_assigned_inspector": "Assigned Safety Officer / Inspector:",
        "lbl_action_notes": "Inspection & Mitigation Remarks:",
        "btn_update_status_submit": "💾 Save Status & Log HSE Action",
        "worker_no_creds_banner": "✨ Public & Field Access Enabled: No login credentials required. Report hazards directly to protect coworkers.",
        "track_search_placeholder": "Enter Complaint ID (e.g., OIL-CMP-... or REP-...) or keyword to track...",
        "track_desc": "Real-time visibility into the status of submitted safety complaints and actions taken by HSE administration.",
        "quick_demo_creds": "Demo Admin Credentials: admin / oilhse2026",
        "complaint_submitted_success": "Complaint Successfully Dispatched to HSE Administration!",
        "tracking_id_banner": "Your Official Tracking Reference ID:"
    },
    "hi": {
        "tab_complaints": "🚨 शिकायतें एवं घटना नियंत्रण केंद्र",
        "tab_tracking": "🔍 मेरी शिकायत की स्थिति ट्रैक करें",
        "role_worker": "👷 फील्ड कार्यकर्ता पोर्टल (1-क्लिक सीधी पहुंच - बिना पासवर्ड)",
        "role_admin": "🔐 HSE कार्यकारी व्यवस्थापक पोर्टल (सुरक्षित लॉगिन)",
        "admin_badge": "👑 भूमिका: HSE कार्यकारी प्रशासक",
        "worker_badge": "👷 भूमिका: फील्ड कार्यकर्ता / सार्वजनिक रिपोर्टर (सामान्य पहुंच)",
        "admin_login_title": "🔐 OIL HSE कार्यकारी प्रशासन लॉगिन",
        "admin_login_sub": "शिकायतों की समीक्षा, साइट दौरे और समाधान के लिए अधिकृत सुरक्षा अधिकारी क्रेडेंशियल दर्ज करें।",
        "lbl_admin_user": "व्यवस्थापक उपयोगकर्ता नाम:",
        "lbl_admin_pass": "व्यवस्थापक पासवर्ड:",
        "btn_login_admin": "🔓 व्यवस्थापक पोर्टल में प्रवेश करें",
        "btn_logout_admin": "🔒 व्यवस्थापक लॉगआउट",
        "lbl_status_filter": "समाधान स्थिति द्वारा फ़िल्टर करें:",
        "lbl_update_status": "घटना स्थिति अपडेट करें और कार्रवाई दर्ज करें",
        "status_unchecked": "अनचेक (Unchecked)",
        "status_gonna_visit": "निरीक्षण होगा (Gonna be Visited)",
        "status_solved": "हल हो गया (Solved)",
        "lbl_assigned_inspector": "नामित सुरक्षा अधिकारी / निरीक्षक:",
        "lbl_action_notes": "निरीक्षण एवं निवारण टिप्पणी:",
        "btn_update_status_submit": "💾 स्थिति सहेजें और कार्रवाई दर्ज करें",
        "worker_no_creds_banner": "✨ सीधी फील्ड पहुंच: किसी पासवर्ड की आवश्यकता नहीं है। साथियों की सुरक्षा के लिए सीधे रिपोर्ट दर्ज करें।",
        "track_search_placeholder": "ट्रैक करने के लिए शिकायत आईडी दर्ज करें (उदा. OIL-CMP-...)...",
        "track_desc": "दर्ज शिकायतों की स्थिति और HSE प्रशासन द्वारा की गई कार्रवाई का वास्तविक समय में लाइव विवरण।",
        "quick_demo_creds": "डेमो व्यवस्थापक क्रेडेंशियल: admin / oilhse2026",
        "complaint_submitted_success": "शिकायत सफलतापूर्वक HSE प्रशासन को अग्रेषित की गई!",
        "tracking_id_banner": "आपकी आधिकारिक ट्रैकिंग संदर्भ आईडी:"
    },
    "as": {
        "tab_complaints": "🚨 অভিযোগ আৰু দুৰ্ঘটনা নিয়ন্ত্ৰণ কেন্দ্ৰ",
        "tab_tracking": "🔍 মোৰ অভিযোগৰ স্থিতি চাওক",
        "role_worker": "👷 ফিল্ড কৰ্মী পৰ্টেল (১-ক্লিক প্ৰৱেশ - কোনো পাছৱৰ্ডৰ প্ৰয়োজন নাই)",
        "role_admin": "🔐 HSE কাৰ্যবাহী প্ৰশাসক পৰ্টেল (সুৰক্ষিত প্ৰৱেশ)",
        "admin_badge": "👑 ভূমিকা: HSE কাৰ্যবাহী প্ৰশাসক",
        "worker_badge": "👷 ভূমিকা: ফিল্ড ৱৰ্কাৰ / সাধাৰণ প্ৰৱেশ",
        "admin_login_title": "🔐 OIL HSE প্ৰশাসক প্ৰৱেশাধিকাৰ",
        "admin_login_sub": "অভিযোগ বিবেচনা, পৰিদৰ্শন আৰু সমাধানৰ বাবে প্ৰাধিকৰিক ক্ৰেডেন্সিয়েল দিয়ক।",
        "lbl_admin_user": "প্ৰশাসক ব্যৱহাৰকাৰী নাম:",
        "lbl_admin_pass": "পাছৱৰ্ড:",
        "btn_login_admin": "🔓 প্ৰশাসক পৰ্টেলত প্ৰৱেশ কৰক",
        "btn_logout_admin": "🔒 প্ৰশাসক লগআউট",
        "lbl_status_filter": "স্থিতি অনুসৰি বাছক:",
        "lbl_update_status": "স্থিতি আপডেট কৰক আৰু কাৰ্য লিপিবদ্ধ কৰক",
        "status_unchecked": "পৰীক্ষা নোহোৱা (Unchecked)",
        "status_gonna_visit": "পৰিদৰ্শন নিৰ্ধাৰিত (Gonna be Visited)",
        "status_solved": "সমাধান হ'ল (Solved)",
        "lbl_assigned_inspector": "নিৰ্ধাৰিত সুৰক্ষা বিষয়া / পৰিদৰ্শক:",
        "lbl_action_notes": "পৰিদৰ্শন আৰু প্ৰশমনৰ মন্তব্য:",
        "btn_update_status_submit": "💾 স্থিতি সংৰক্ষণ কৰক",
        "worker_no_creds_banner": "✨ সাধাৰণ প্ৰৱেশ সক্ৰিয়: পাছৱৰ্ডৰ প্ৰয়োজন নাই। সতীৰ্থৰ সুৰক্ষাৰ বাবে পোনপটীয়াকৈ বিপদৰ খবৰ দিয়ক।",
        "track_search_placeholder": "ট্ৰেক কৰিবলৈ অভিযোগ আইডি দিয়ক...",
        "track_desc": "দাখিল কৰা সুৰক্ষা অভিযোগৰ স্থিতি আৰু HSE ব্যৱস্থাৰ লাইভ তথ্য।",
        "quick_demo_creds": "ডেমো প্ৰশাসক ক্ৰেডেন্সিয়েল: admin / oilhse2026",
        "complaint_submitted_success": "অভিযোগ সফলভাৱে HSE প্ৰশাসনলৈ প্ৰেৰণ কৰা হ'ল!",
        "tracking_id_banner": "আপোনাৰ অফিচিয়েল ট্ৰেকিং ৰেফাৰেন্স আইডি:"
    },
    "bn": {
        "tab_complaints": "🚨 অভিযোগ ও ঘটনা নিয়ন্ত্রণ কেন্দ্র",
        "tab_tracking": "🔍 আমার অভিযোগের স্ট্যাটাস দেখুন",
        "role_worker": "👷 ফিল্ড কর্মী পোর্টাল (১-ক্লিকে সরাসরি প্রবেশ - পাসওয়ার্ডহীন)",
        "role_admin": "🔐 HSE নির্বাহী প্রশাসক পোর্টাল (সুরক্ষিত লগইন)",
        "admin_badge": "👑 ভূমিকা: HSE নির্বাহী প্রশাসক",
        "worker_badge": "👷 ভূমিকা: ফিল্ড কর্মী / সাধারণ প্রবেশাধিকার",
        "admin_login_title": "🔐 OIL HSE প্রশাসক লগইন",
        "admin_login_sub": "অভিযোগ পর্যালোচনা, পরিদর্শন নির্ধারণ ও সমাধানের জন্য লগইন করুন।",
        "lbl_admin_user": "প্রশাসক ইউজারনেম:",
        "lbl_admin_pass": "পাসওয়ার্ড:",
        "btn_login_admin": "🔓 প্রশাসক পোর্টালে প্রবেশ করুন",
        "btn_logout_admin": "🔒 প্রশাসক লগআউট",
        "lbl_status_filter": "স্ট্যাটাস অনুযায়ী ফিল্টার করুন:",
        "lbl_update_status": "স্ট্যাটাস আপডেট করুন ও পদক্ষেপ নথিভুক্ত করুন",
        "status_unchecked": "অপরীক্ষিত (Unchecked)",
        "status_gonna_visit": "পরিদর্শন নির্ধারিত (Gonna be Visited)",
        "status_solved": "সমাধান হয়েছে (Solved)",
        "lbl_assigned_inspector": "দায়িত্বপ্রাপ্ত নিরাপত্তা কর্মকর্তা / পরিদর্শক:",
        "lbl_action_notes": "পরিদর্শন ও সমাধানের বিবরণ:",
        "btn_update_status_submit": "💾 স্ট্যাটাস সংরক্ষণ করুন",
        "worker_no_creds_banner": "✨ সর্বজনীন ফিল্ড অ্যাক্সেস: কোনো পাসওয়ার্ড প্রয়োজন নেই। সহকর্মীদের সুরক্ষায় সরাসরি বিপদ রিপোর্ট করুন।",
        "track_search_placeholder": "অভিযোগের আইডি দিন...",
        "track_desc": "দাখিল করা রিপোর্টের অগ্রগতি ও প্রশাসনের পদক্ষেপের সরাসরি বিবরণ।",
        "quick_demo_creds": "ডেমো প্রশাসক ক্রেডেনশিয়াল: admin / oilhse2026",
        "complaint_submitted_success": "অভিযোগ সফলভাবে HSE প্রশাসনের নিকট পাঠানো হয়েছে!",
        "tracking_id_banner": "আপনার অফিসিয়াল ট্র্যাকিং আইডি:"
    }
}

def get_localized_sites(lang_code: str) -> List[str]:
    """Return list of localized site option strings."""
    return [SITE_MAP[k].get(lang_code, SITE_MAP[k].get('en', k)) for k in SITE_MAP.keys()]

def to_canonical_site(localized_str: str, lang_code: str) -> str:
    """Map localized site display string back to canonical English string."""
    for k, v in SITE_MAP.items():
        if v.get(lang_code) == localized_str or v.get('en') == localized_str or k == localized_str:
            return k
    return localized_str

def get_localized_activities(lang_code: str) -> List[str]:
    """Return list of localized activity option strings."""
    return [ACTIVITY_MAP[k].get(lang_code, ACTIVITY_MAP[k].get('en', k)) for k in ACTIVITY_MAP.keys()]

def to_canonical_activity(localized_str: str, lang_code: str) -> str:
    """Map localized activity string back to canonical English string."""
    for k, v in ACTIVITY_MAP.items():
        if v.get(lang_code) == localized_str or v.get('en') == localized_str or k == localized_str:
            return k
    return localized_str

def get_localized_categories(lang_code: str) -> List[str]:
    """Return list of localized category option strings."""
    return [CATEGORY_MAP[k].get(lang_code, CATEGORY_MAP[k].get('en', k)) for k in CATEGORY_MAP.keys()]

def to_canonical_category(localized_str: str, lang_code: str) -> str:
    """Map localized category string back to canonical English category."""
    for k, v in CATEGORY_MAP.items():
        if v.get(lang_code) == localized_str or v.get('en') == localized_str or k == localized_str:
            return k
    return localized_str

def get_localized_statuses(lang_code: str) -> List[str]:
    """Return list of localized status option strings."""
    return [STATUS_MAP[k].get(lang_code, STATUS_MAP[k].get('en', k)) for k in STATUS_MAP.keys()]

def to_canonical_status(localized_str: str, lang_code: str) -> str:
    """Map localized status string back to canonical status."""
    for k, v in STATUS_MAP.items():
        if v.get(lang_code) == localized_str or v.get('en') == localized_str or k == localized_str:
            return k
    return localized_str

def translate_status(status_key: str, lang_code: str) -> str:
    """Translate canonical status key into display string for active language."""
    return STATUS_MAP.get(status_key, {}).get(lang_code, STATUS_MAP.get(status_key, {}).get('en', status_key))

def translate_site(site_key: str, lang_code: str) -> str:
    """Translate canonical site key into display string."""
    return SITE_MAP.get(site_key, {}).get(lang_code, SITE_MAP.get(site_key, {}).get('en', site_key))

def translate_activity(activity_key: str, lang_code: str) -> str:
    """Translate canonical activity key into display string."""
    return ACTIVITY_MAP.get(activity_key, {}).get(lang_code, ACTIVITY_MAP.get(activity_key, {}).get('en', activity_key))

def translate_category(category_key: str, lang_code: str) -> str:
    """Translate canonical category key into display string."""
    return CATEGORY_MAP.get(category_key, {}).get(lang_code, CATEGORY_MAP.get(category_key, {}).get('en', category_key))

def get_ui_text_ext(lang_code: str, key: str, fallback: str = "") -> str:
    """Retrieve UI text with regional translation and graceful fallback."""
    if lang_code in EXTRA_UI_STRINGS and key in EXTRA_UI_STRINGS[lang_code]:
        return EXTRA_UI_STRINGS[lang_code][key]
    if "en" in EXTRA_UI_STRINGS and key in EXTRA_UI_STRINGS["en"]:
        return EXTRA_UI_STRINGS["en"][key]
    return fallback if fallback else key
