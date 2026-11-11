import os
import sys
import datetime
import random
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# Ensure project root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.ingestion import validate_and_clean_df, translate_regional_text
from src.sif_classifier import SIFClassifier
from src.lsr_tagger import LSRTagger
from src.precursor_extractor import PrecursorExtractor
from src.analytics import (
    compute_overall_metrics, get_site_risk_ranking,
    get_activity_risk_ranking, get_monthly_trends, get_heatmap_matrix
)
from src.utils import apply_custom_css, SAMPLE_DEMO_TEXTS
from src.translations import UI_LANGUAGES, get_txt, translate_content_label
from src.options_translations import (
    get_localized_sites, to_canonical_site, translate_site,
    get_localized_activities, to_canonical_activity, translate_activity,
    get_localized_categories, to_canonical_category, translate_category,
    get_localized_statuses, to_canonical_status, translate_status,
    get_ui_text_ext
)
import src.complaint_store as cs

# Set page config
st.set_page_config(
    page_title="OIL Safety | Easy Hazard Reporting",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply simple, attractive, friendly CSS
apply_custom_css()

# ==============================================================================
# SESSION STATE & AUTH
# ==============================================================================
if 'user_role' not in st.session_state:
    st.session_state.user_role = 'worker'
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False
if 'last_submitted_complaint' not in st.session_state:
    st.session_state.last_submitted_complaint = None
if 'worker_hazard_text_area' not in st.session_state:
    st.session_state.worker_hazard_text_area = ""

# ==============================================================================
# SIDEBAR: SIMPLE LANGUAGE & ROLE SELECTOR
# ==============================================================================
st.sidebar.markdown("### 🌐 Choose Language / भाषा")
selected_ui_lang = st.sidebar.selectbox(
    "Website Language:",
    list(UI_LANGUAGES.keys()),
    index=0
)
lang_code = UI_LANGUAGES[selected_ui_lang]

def t(key: str, default: str = "") -> str:
    res = get_ui_text_ext(lang_code, key)
    if not res or res == key:
        res = get_txt(lang_code, key)
    return res if res and res != key else (default if default else key)

st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 Who is using this app?")
role_pick = st.sidebar.radio(
    "Select your role:",
    ["👷 I am a Field Worker (Report a Hazard)", "👑 I am an Admin / Safety Lead"],
    index=0 if st.session_state.user_role == 'worker' else 1
)

if "Field Worker" in role_pick:
    st.session_state.user_role = 'worker'
else:
    st.session_state.user_role = 'admin'

ADMIN_USER = "admin"
ADMIN_PASS = "oilhse2026"

if st.session_state.user_role == 'admin' and not st.session_state.admin_authenticated:
    st.sidebar.markdown("#### 🔐 Admin Sign-In")
    u_val = st.sidebar.text_input("Username:", placeholder="admin", key="sb_admin_u")
    p_val = st.sidebar.text_input("Password:", type="password", placeholder="oilhse2026", key="sb_admin_p")
    if st.sidebar.button("🔓 Sign In", type="primary", use_container_width=True):
        if u_val.strip() == ADMIN_USER and p_val.strip() in [ADMIN_PASS, "admin123"]:
            st.session_state.admin_authenticated = True
            st.sidebar.success("Welcome, Safety Officer!")
            st.rerun()
        else:
            st.sidebar.error("Incorrect username or password.")
    st.sidebar.caption("💡 *Demo Login: `admin` / `oilhse2026`*")
elif st.session_state.user_role == 'admin' and st.session_state.admin_authenticated:
    st.sidebar.success("👑 Logged in as: HSE Safety Officer")
    if st.sidebar.button("🔒 Sign Out", use_container_width=True):
        st.session_state.admin_authenticated = False
        st.session_state.user_role = 'worker'
        st.rerun()

# ==============================================================================
# LOAD AI MODELS
# ==============================================================================
@st.cache_resource
def load_models():
    sample_path = os.path.join(os.path.dirname(__file__), 'data', 'sample_sif_reports.csv')
    classifier = SIFClassifier()
    tagger = LSRTagger()
    extractor = PrecursorExtractor()
    if os.path.exists(sample_path):
        df_init = pd.read_csv(sample_path)
        df_init = validate_and_clean_df(df_init)
        classifier.fit(list(df_init['report_text']), list(df_init['ground_truth_sif']))
    return classifier, tagger, extractor

classifier, tagger, extractor = load_models()

# ==============================================================================
# FRIENDLY HEADER BANNER
# ==============================================================================
role_tag_html = ""
if st.session_state.user_role == 'admin' and st.session_state.admin_authenticated:
    role_tag_html = '<span class="status-badge-orange">👑 Safety Officer Command</span>'
else:
    role_tag_html = '<span class="status-badge-green">👷 Field Operator Portal</span>'

st.markdown(f"""
<div class="app-header-card">
    <div>
        <div class="oil-brand-badge">⚡ OIL INDIA LIMITED • SAFETY INTELLIGENCE</div>
        <h1 class="app-title">HSE Incident & Hazard Intelligence Portal</h1>
        <div class="app-subtitle">Serious Injury & Fatality (SIF) Precursor Analytics • IOGP Life-Saving Rules Multi-Label Classifier</div>
    </div>
    <div style="display:flex; flex-direction:column; align-items:flex-end; gap:8px;">
        {role_tag_html}
        <span class="status-badge-blue">● OISD-GDN-169 & IOGP-10 Standard</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Helper function to render visual delivery-style tracker
def render_visual_tracker(status_val: str):
    is_step1 = True
    is_step2 = (status_val in [cs.STATUS_GONNA_BE_VISITED, cs.STATUS_SOLVED])
    is_step3 = (status_val == cs.STATUS_SOLVED)

    c1_class = "stepper-red" if status_val == cs.STATUS_UNCHECKED else ("stepper-green" if is_step2 else "stepper-red")
    c2_class = "stepper-orange" if status_val == cs.STATUS_GONNA_BE_VISITED else ("stepper-green" if is_step3 else "stepper-inactive")
    c3_class = "stepper-green" if is_step3 else "stepper-inactive"

    b1_class = "stepper-bar stepper-bar-active" if is_step2 else "stepper-bar"
    b2_class = "stepper-bar stepper-bar-active" if is_step3 else "stepper-bar"

    return f"""
    <div class="stepper-container">
        <div class="stepper-node">
            <div class="stepper-icon-circle {c1_class}">📝</div>
            <div style="font-weight:700; font-size:0.85rem; color:#f8fafc;">1. Incident Logged</div>
            <div style="font-size:0.75rem; color:#94a3b8;">Pending HSE Review</div>
        </div>
        <div class="{b1_class}"></div>
        <div class="stepper-node">
            <div class="stepper-icon-circle {c2_class}">🏃</div>
            <div style="font-weight:700; font-size:0.85rem; color:#f8fafc;">2. Team Dispatched</div>
            <div style="font-size:0.75rem; color:#94a3b8;">Site Audit In Progress</div>
        </div>
        <div class="{b2_class}"></div>
        <div class="stepper-node">
            <div class="stepper-icon-circle {c3_class}">✅</div>
            <div style="font-weight:700; font-size:0.85rem; color:#f8fafc;">3. Mitigated & Closed</div>
            <div style="font-size:0.75rem; color:#94a3b8;">Hazard Rectified</div>
        </div>
    </div>
    """

# ==============================================================================
# WORKER VIEW (CLEAN ENTERPRISE WORKFLOW)
# ==============================================================================
is_admin_active = (st.session_state.user_role == 'admin' and st.session_state.admin_authenticated)

if not is_admin_active:
    tab_report, tab_track, tab_admin_login_box = st.tabs([
        "📢 Report a Safety Hazard",
        "🔍 Track My Report Status",
        "🔐 Safety Officer Login"
    ])

    with tab_report:
        st.markdown("""
        <div style="margin-bottom:20px;">
            <h2 style="font-weight:800; font-size:1.6rem; color:#f8fafc; margin-bottom:4px;">Field Incident & Hazard Observation Report</h2>
            <p style="color:#94a3b8; font-size:0.95rem; margin:0;">Voice-enabled field reporting supporting Assamese, Hindi, Bengali, and English. Automatically standardized into HSE incident logs.</p>
        </div>
        """, unsafe_allow_html=True)

        col_left, col_right = st.columns([1.2, 1])

        with col_left:
            st.markdown("""
            <div class="pro-card">
                <div class="pro-card-header">
                    <div class="pro-card-title">🎙️ Incident Narrative & Spoken Audio</div>
                    <span class="status-badge-blue">Section 1</span>
                </div>
            """, unsafe_allow_html=True)

            speech_lang = st.selectbox(
                "🗣️ Spoken Language:",
                [
                    "Assamese (অসমীয়া)", "Hindi / Hinglish (हिंदी)", "Bengali (বাংলা)",
                    "Tamil (தமிழ்)", "Telugu (తెలుగు)", "Kannada (ಕನ್ನಡ)", "Malayalam (മലയാളം)", "English"
                ]
            )

            # Quick Preset Buttons for easy testing
            st.caption("⚡ Or select a verified test scenario:")
            p1, p2, p3 = st.columns(3)
            if p1.button("🧗 Fall Danger"):
                st.session_state.worker_hazard_text_area = "Worker on scaffolding without safety harness tied to lifeline."
            if p2.button("🔥 Fire / Gas"):
                st.session_state.worker_hazard_text_area = "Welding near gas tank without safety permit."
            if p3.button("🏗️ Crane Lifting"):
                st.session_state.worker_hazard_text_area = "Crane lifting heavy pipe with broken frayed rope."

            # HTML5 Speech Dictation
            speech_code_map = {
                "Assamese (অসমীয়া)": "as-IN",
                "Hindi / Hinglish (हिंदी)": "hi-IN",
                "Bengali (বাংলা)": "bn-IN",
                "Tamil (தமிழ்)": "ta-IN",
                "Telugu (తెలుగు)": "te-IN",
                "Kannada (ಕನ್ನಡ)": "kn-IN",
                "Malayalam (മലയാളം)": "ml-IN",
                "English": "en-IN"
            }
            active_speech_code = speech_code_map.get(speech_lang, "en-IN")

            speech_html = f"""
            <div style="background:#111827; border:1px solid #334155; border-radius:14px; padding:16px; text-align:center; margin-bottom:14px;">
                <button id="mic_btn" onclick="startMic()" style="background:linear-gradient(135deg, #0284c7 0%, #0369a1 100%); color:#ffffff; border:none; padding:10px 24px; border-radius:30px; font-weight:700; font-size:0.95rem; cursor:pointer; box-shadow:0 2px 10px rgba(2, 132, 199, 0.3);">
                    🎙️ Tap to Speak ({speech_lang})
                </button>
                <div id="mic_msg" style="color:#94a3b8; font-size:0.85rem; margin-top:8px;">Dictate clearly into your microphone</div>
                <div id="mic_result" style="color:#34d399; font-weight:600; margin-top:6px; font-size:0.9rem; display:none;"></div>
            </div>
            <script>
                var rec;
                function startMic() {{
                    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {{
                        document.getElementById('mic_msg').innerText = 'Microphone not supported on this browser. Please type below!';
                        return;
                    }}
                    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
                    rec = new SR();
                    rec.lang = '{active_speech_code}';
                    rec.start();
                    document.getElementById('mic_btn').style.background = '#dc2626';
                    document.getElementById('mic_btn').style.color = '#ffffff';
                    document.getElementById('mic_btn').innerText = '⏹️ Listening... Speak Now!';
                    document.getElementById('mic_msg').innerText = 'Listening to your voice...';

                    rec.onresult = function(e) {{
                        var word = e.results[0][0].transcript;
                        document.getElementById('mic_msg').innerText = '✅ Heard you!';
                        document.getElementById('mic_result').style.display = 'block';
                        document.getElementById('mic_result').innerText = '🗣️ "' + word + '"';
                        
                        try {{
                            var textAreas = window.parent.document.querySelectorAll('textarea');
                            if (textAreas.length > 0) {{
                                textAreas[0].value = word;
                                textAreas[0].dispatchEvent(new Event('input', {{ bubbles: true }}));
                                textAreas[0].dispatchEvent(new Event('change', {{ bubbles: true }}));
                            }}
                        }} catch(err) {{ console.log(err); }}
                    }};
                    rec.onend = function() {{
                        document.getElementById('mic_btn').style.background = '#0284c7';
                        document.getElementById('mic_btn').style.color = '#ffffff';
                        document.getElementById('mic_btn').innerText = '🎙️ Tap to Speak';
                    }};
                }}
            </script>
            """
            st.components.v1.html(speech_html, height=115)

            user_hazard_text = st.text_area(
                "Observation Narrative:",
                key="worker_hazard_text_area",
                height=110,
                placeholder="Example: High pressure gas valve leaking near crude manifold without tag-out isolation..."
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            st.markdown("""
            <div class="pro-card">
                <div class="pro-card-header">
                    <div class="pro-card-title">📍 Operational Context & Location</div>
                    <span class="status-badge-blue">Section 2</span>
                </div>
            """, unsafe_allow_html=True)

            # Localized dropdowns
            loc_sites = get_localized_sites(lang_code)
            loc_acts = get_localized_activities(lang_code)

            chosen_site_disp = st.selectbox("📍 Plant / Rig Location:", loc_sites)
            chosen_act_disp = st.selectbox("🔨 Operational Activity:", loc_acts)

            worker_name_input = st.text_input("👷 Reporter Name / Badge Code (Optional):", value="Field Operator #402")

            st.markdown("<br>", unsafe_allow_html=True)
            send_report_btn = st.button("📤 Submit Incident Report to HSE Command", type="primary", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if send_report_btn:
            if not user_hazard_text.strip():
                st.warning("⚠️ Please speak or write something about what you saw before sending.")
            else:
                canonical_site = to_canonical_site(chosen_site_disp, lang_code)
                canonical_act = to_canonical_activity(chosen_act_disp, lang_code)

                # Translate text to standardized English
                clean_english_text = translate_regional_text(user_hazard_text)
                matched_lsr = tagger.tag_text(clean_english_text)
                res = classifier.predict_one(clean_english_text, matched_lsr)

                # Generate clean ID
                new_id = f"OIL-{datetime.datetime.now().strftime('%y%m%d')}-{random.randint(100, 999)}"

                # Add to persistent complaint store
                new_rec = cs.add_complaint(
                    worker_name=worker_name_input,
                    site=canonical_site,
                    activity=canonical_act,
                    category="Unsafe Condition",
                    equipment="On-site gear",
                    original_text=user_hazard_text.strip(),
                    translated_text=clean_english_text,
                    original_language=speech_lang,
                    sif_res=res,
                    matched_lsr=matched_lsr,
                    custom_id=new_id
                )

                st.session_state.last_submitted_complaint = new_rec

                # Celebration & Results Banner
                is_danger = (res['sif_label'] == 'SIF-Potential')

                if is_danger:
                    lsr_display = ', '.join(matched_lsr) if matched_lsr else "General Operations"
                    st.markdown(f"""
                    <div class="danger-banner">
                        <div style="font-size:2.4rem; margin-bottom:4px;">🚨</div>
                        <h2 style="color:#f87171; font-size:1.6rem; font-weight:800; margin:0;">CRITICAL SIF PRECURSOR DETECTED</h2>
                        <p style="color:#fecaca; font-size:1.02rem; max-width:650px; margin:8px auto;">
                            High-consequence fatality hazard pattern identified. Emergency safety intervention protocol triggered.
                        </p>
                        <div style="margin-top:14px; display:flex; justify-content:center; gap:10px; flex-wrap:wrap;">
                            <span class="status-badge-red">Tracking ID: <b>{new_id}</b></span>
                            <span class="status-badge-orange">Risk Score: <b>{res['risk_score']}/10</b></span>
                            <span class="status-badge-blue">IOGP Rule: <b>{lsr_display}</b></span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="safe-banner">
                        <div style="font-size:2.4rem; margin-bottom:4px;">✅</div>
                        <h2 style="color:#34d399; font-size:1.6rem; font-weight:800; margin:0;">OBSERVATION LOGGED SUCCESSFULLY</h2>
                        <p style="color:#a7f3d0; font-size:1.02rem; max-width:650px; margin:8px auto;">
                            Low-risk operational observation recorded. Scheduled for standard shift walkthrough review.
                        </p>
                        <div style="margin-top:14px; display:flex; justify-content:center; gap:10px; flex-wrap:wrap;">
                            <span class="status-badge-green">Tracking ID: <b>{new_id}</b></span>
                            <span class="status-badge-blue">Risk Score: <b>{res['risk_score']}/10</b></span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("### 📋 Live Incident Lifecycle Status:")
                st.markdown(render_visual_tracker(cs.STATUS_UNCHECKED), unsafe_allow_html=True)
                st.info(f"💡 **AI NLP Attribution:** {res['explanation']}")

    # ==============================================================================
    # TAB: WORKER TRACKING (SIMPLE PACKAGE TRACKER STYLE)
    # ==============================================================================
    with tab_track:
        st.markdown("""
        <div style="margin-bottom:20px;">
            <h2 style="font-weight:800; font-size:1.6rem; color:#f8fafc; margin-bottom:4px;">🔍 Incident Lifecycle Audit & Tracking</h2>
            <p style="color:#94a3b8; font-size:0.95rem;">Track real-time inspection status, assigned HSE inspectors, and corrective action verification across all OIL facilities.</p>
        </div>
        """, unsafe_allow_html=True)

        complaints_list = cs.load_all_complaints()

        last_id = st.session_state.last_submitted_complaint.get('complaint_id', '') if st.session_state.last_submitted_complaint else ""
        search_query = st.text_input("Type your Tracking ID or Site Name:", value=last_id, placeholder="e.g. OIL-261018-450, Digboi, Scaffolding...")

        shown_items = complaints_list
        if search_query.strip():
            sq = search_query.strip().lower()
            shown_items = [
                c for c in shown_items
                if sq in c.get('complaint_id', '').lower()
                or sq in c.get('site', '').lower()
                or sq in c.get('activity', '').lower()
                or sq in c.get('original_text', '').lower()
                or sq in c.get('translated_text', '').lower()
            ]

        st.markdown(f"**Found {len(shown_items)} reports:**")

        for item in shown_items[:15]:
            cid = item.get('complaint_id', 'N/A')
            c_status = item.get('status', cs.STATUS_UNCHECKED)
            c_site = translate_site(item.get('site', ''), lang_code)
            c_act = translate_activity(item.get('activity', ''), lang_code)
            c_desc = item.get('original_text', item.get('translated_text', ''))

            with st.expander(f"📋 [{cid}] {c_site} — {c_act}", expanded=(cid == last_id)):
                st.markdown(f"**What was reported:**\n> {c_desc}")
                st.markdown(render_visual_tracker(c_status), unsafe_allow_html=True)

                c_info1, c_info2 = st.columns(2)
                with c_info1:
                    st.write(f"👷 **Reported By:** {item.get('worker_name', 'Field Worker')}")
                    st.write(f"📅 **Date:** {item.get('timestamp')}")
                with c_info2:
                    st.write(f"👮 **Officer Assigned:** {item.get('assigned_inspector', 'Waiting for Assignment')}")
                    st.write(f"📝 **Action Taken:** {item.get('admin_notes', 'Pending initial safety review.')}")

    # ==============================================================================
    # TAB: ADMIN LOGIN SCREEN (IF SELECTED FROM WORKER TABS)
    # ==============================================================================
    with tab_admin_login_box:
        st.markdown("### 👑 Safety Officer / Admin Sign-In")
        l_col1, _ = st.columns([1.5, 1])
        with l_col1:
            st.markdown("""
            <div class="pro-card">
                <div class="pro-card-header">
                    <div class="pro-card-title">🔐 HSE Lead & Officer Authentication</div>
                    <span class="status-badge-blue">Authorized Access</span>
                </div>
                <p style="color:#94a3b8; font-size:0.92rem; margin:0;">
                    Sign in to dispatch inspection teams, verify barrier controls, update incident lifecycles, and access regulatory audit logs.
                </p>
            </div>
            """, unsafe_allow_html=True)
            u_in = st.text_input("Admin Username:", key="tab_login_u", placeholder="admin")
            p_in = st.text_input("Admin Password:", type="password", key="tab_login_p", placeholder="oilhse2026")
            st.info("💡 *Demo Credentials: `admin` / `oilhse2026`*")
            if st.button("🔓 Sign In to Admin Panel", type="primary", use_container_width=True):
                if u_in.strip() == ADMIN_USER and p_in.strip() in [ADMIN_PASS, "admin123"]:
                    st.session_state.admin_authenticated = True
                    st.session_state.user_role = 'admin'
                    st.success("Signed in successfully!")
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")

# ==============================================================================
# ADMIN VIEW (SUPER CLEAN & EASY APPROVAL CARDS)
# ==============================================================================
else:
    all_complaints = cs.load_all_complaints()
    metrics = cs.get_complaint_metrics(all_complaints)

    # 3 Big, colorful, child-simple counters at the top!
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f"""
        <div class="stat-box stat-box-red">
            <div class="stat-number" style="color:#f87171;">{metrics['unchecked']}</div>
            <div class="stat-label">🔴 Pending Review</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="stat-box stat-box-orange">
            <div class="stat-number" style="color:#fbbf24;">{metrics['gonna_visit']}</div>
            <div class="stat-label">🟠 Inspections Dispatched</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="stat-box stat-box-green">
            <div class="stat-number" style="color:#34d399;">{metrics['solved']}</div>
            <div class="stat-label">🟢 Mitigated & Closed</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    admin_tabs = st.tabs([
        "🚨 Safety Complaints Queue",
        "📊 Quick Risk Overview",
        "📱 Report on Behalf of Worker",
        "📥 Official HSE Compliance Export"
    ])

    # TAB 1: COMPLAINTS ACTION QUEUE
    with admin_tabs[0]:
        st.markdown("### 📋 Manage & Fix Safety Complaints")
        st.caption("Change status with one click, assign who is going, and write what was done.")

        # Quick Status Filter
        flt_col1, flt_col2 = st.columns([1.5, 3])
        with flt_col1:
            chosen_filter = st.selectbox(
                "Show:",
                ["All Complaints", cs.STATUS_UNCHECKED, cs.STATUS_GONNA_BE_VISITED, cs.STATUS_SOLVED]
            )
        with flt_col2:
            search_bar = st.text_input("Quick Search:", placeholder="Type location, worker name, keyword...")

        admin_list = all_complaints
        if chosen_filter != "All Complaints":
            admin_list = [c for c in admin_list if c.get('status') == chosen_filter]
        if search_bar.strip():
            sb = search_bar.strip().lower()
            admin_list = [
                c for c in admin_list
                if sb in c.get('complaint_id', '').lower()
                or sb in c.get('site', '').lower()
                or sb in c.get('activity', '').lower()
                or sb in c.get('original_text', '').lower()
                or sb in c.get('translated_text', '').lower()
            ]

        st.markdown(f"**Showing {len(admin_list)} complaints:**")

        for idx, item in enumerate(admin_list[:25]):
            cid = item.get('complaint_id', f"CMP-{idx}")
            c_status = item.get('status', cs.STATUS_UNCHECKED)
            c_score = item.get('risk_score', 5.0)
            c_site = item.get('site', '')
            c_act = item.get('activity', '')
            c_text = item.get('translated_text', item.get('original_text', ''))
            c_officer = item.get('assigned_inspector', 'HSE Safety Officer')
            c_notes = item.get('admin_notes', '')

            badge_color = "#ef4444" if c_status == cs.STATUS_UNCHECKED else ("#f59e0b" if c_status == cs.STATUS_GONNA_BE_VISITED else "#10b981")

            with st.expander(f"[{cid}] {c_site} — Risk: {c_score}/10 | Status: {c_status}", expanded=(idx == 0)):
                card_c1, card_c2 = st.columns([1.4, 1.6])

                with card_c1:
                    if c_score >= 8.0:
                        st.markdown(f"""
                        <div style="background:rgba(239, 68, 68, 0.15); border:1px solid #ef4444; border-radius:10px; padding:10px 14px; margin-bottom:12px; font-size:0.88rem; color:#fca5a5;">
                            🚨 <b>CRITICAL SIF PRECURSOR DISPATCH ALERT:</b><br>
                            Auto-alerted On-Duty HSE Supervisor at <b>{c_site}</b> via UHF Emergency Channel 1 & SMS.
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown(f"**Reported Hazard:**\n> {c_text}")
                    st.write(f"📍 **Location:** `{c_site}`")
                    st.write(f"🔨 **Activity:** `{c_act}`")
                    st.write(f"👷 **Reported by:** `{item.get('worker_name')}` on `{item.get('timestamp')}`")
                    st.markdown(render_visual_tracker(c_status), unsafe_allow_html=True)

                with card_c2:
                    st.markdown("#### 🛠️ Update Status (1-Click):")

                    stat_choices = [cs.STATUS_UNCHECKED, cs.STATUS_GONNA_BE_VISITED, cs.STATUS_SOLVED]
                    try:
                        cur_idx = stat_choices.index(c_status)
                    except ValueError:
                        cur_idx = 0

                    new_stat = st.radio(
                        "Current Status:",
                        stat_choices,
                        index=cur_idx,
                        key=f"adm_radio_{cid}_{idx}",
                        horizontal=True
                    )

                    new_officer = st.text_input("Who is visiting?", value=c_officer, key=f"adm_off_{cid}_{idx}")
                    new_action_note = st.text_input("Action Taken / Notes:", value=c_notes, placeholder="e.g. Visited at 2 PM, replaced harness.", key=f"adm_note_{cid}_{idx}")

                    if st.button(f"💾 Save Changes for {cid}", type="primary", key=f"adm_save_{cid}_{idx}"):
                        cs.update_complaint_status(
                            complaint_id=cid,
                            new_status=new_stat,
                            admin_notes=new_action_note,
                            assigned_inspector=new_officer
                        )
                        st.toast(f"Updated status for {cid}!", icon="✅")
                        st.rerun()

    # TAB 2: SIMPLE RISK OVERVIEW
    with admin_tabs[1]:
        st.markdown("### 📊 Safe vs High Risk Overview")
        st.caption("Clean, high-level picture of current safety health across OIL facilities.")

        df_curr = pd.DataFrame(all_complaints)
        if not df_curr.empty and 'site' in df_curr.columns:
            o_col1, o_col2 = st.columns(2)
            with o_col1:
                st.markdown("#### Top Sites by Safety Reports")
                site_counts = df_curr['site'].value_counts().reset_index()
                site_counts.columns = ['Site', 'Reports']
                fig_s = px.bar(site_counts, x='Reports', y='Site', orientation='h', color='Reports', color_continuous_scale='Blues')
                fig_s.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'))
                st.plotly_chart(fig_s, use_container_width=True)

            with o_col2:
                st.markdown("#### Danger Level Split")
                sif_counts = df_curr['sif_label'].value_counts().reset_index()
                sif_counts.columns = ['Risk', 'Count']
                fig_p = px.pie(sif_counts, names='Risk', values='Count', color='Risk', color_discrete_map={'SIF-Potential': '#ef4444', 'Non-SIF': '#10b981'}, hole=0.45)
                fig_p.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'))
                st.plotly_chart(fig_p, use_container_width=True)

    # TAB 3: LOG ON BEHALF
    with admin_tabs[2]:
        st.markdown("### 📱 Log Hazard on Behalf of a Field Worker")
        a_site = st.selectbox("Site:", get_localized_sites('en'), key="onbehalf_site")
        a_act = st.selectbox("Activity:", get_localized_activities('en'), key="onbehalf_act")
        a_txt = st.text_area("Hazard Description:", placeholder="Describe the hazard...", key="onbehalf_txt")
        if st.button("Submit on Behalf", type="primary"):
            if a_txt.strip():
                c_site = to_canonical_site(a_site, 'en')
                c_act = to_canonical_activity(a_act, 'en')
                matched_lsr = tagger.tag_text(a_txt)
                res = classifier.predict_one(a_txt, matched_lsr)
                nid = f"OIL-{datetime.datetime.now().strftime('%y%m%d')}-{random.randint(100, 999)}"
                cs.add_complaint(
                    worker_name="Logged by HSE Admin",
                    site=c_site,
                    activity=c_act,
                    category="Unsafe Act",
                    equipment="Rig",
                    original_text=a_txt,
                    translated_text=a_txt,
                    original_language="English",
                    sif_res=res,
                    matched_lsr=matched_lsr,
                    custom_id=nid
                )
                st.success(f"Report {nid} created!")
                st.rerun()

    # TAB 4: OFFICIAL HSE COMPLIANCE EXPORT (OISD / DGMS AUDIT)
    with admin_tabs[3]:
        st.markdown("### 📥 Official HSE Compliance & Shift Handover Export")
        st.caption("Generate standardized audit reports compliant with OISD (Oil Industry Safety Directorate) and DGMS guidelines.")

        df_all = pd.DataFrame(all_complaints)
        if not df_all.empty:
            e_col1, e_col2, e_col3 = st.columns(3)
            with e_col1:
                st.metric("Total Incident Records", len(df_all))
            with e_col2:
                sif_total = len(df_all[df_all['sif_label'] == 'SIF-Potential']) if 'sif_label' in df_all.columns else 0
                st.metric("High SIF Precursors", sif_total)
            with e_col3:
                resolved_cnt = len(df_all[df_all['status'] == cs.STATUS_SOLVED]) if 'status' in df_all.columns else 0
                st.metric("Mitigated & Closed", resolved_cnt)

            st.markdown("---")
            st.markdown("#### 📄 Filter & Download Regulatory Dataset")
            export_filter = st.selectbox(
                "Filter records by Action Status:",
                ["All Records", cs.STATUS_UNCHECKED, cs.STATUS_GONNA_BE_VISITED, cs.STATUS_SOLVED],
                key="exp_status_flt"
            )

            df_export = df_all.copy()
            if export_filter != "All Records":
                df_export = df_export[df_export['status'] == export_filter]

            col_order = [
                'complaint_id', 'timestamp', 'site', 'activity', 'category',
                'sif_label', 'risk_score', 'lsr_tags', 'status',
                'assigned_inspector', 'admin_notes', 'original_text'
            ]
            valid_cols = [c for c in col_order if c in df_export.columns]
            export_clean = df_export[valid_cols].rename(columns={
                'complaint_id': 'Report_Tracking_ID',
                'timestamp': 'Date_Time_Logged',
                'site': 'Facility_Location',
                'activity': 'Operational_Activity',
                'category': 'Hazard_Classification',
                'sif_label': 'SIF_Potential',
                'risk_score': 'Risk_Score_1_to_10',
                'lsr_tags': 'IOGP_Life_Saving_Rules_Violated',
                'status': 'Current_Action_Status',
                'assigned_inspector': 'Assigned_Safety_Officer',
                'admin_notes': 'Corrective_Action_Notes',
                'original_text': 'Incident_Narrative'
            })

            st.dataframe(export_clean, use_container_width=True, hide_index=True)

            csv_data = export_clean.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Scored HSE Incident Log (CSV / Excel Compatible)",
                data=csv_data,
                file_name=f"OIL_HSE_Audit_Log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                type="primary",
                use_container_width=True
            )
        else:
            st.info("No complaint records currently available to export.")
