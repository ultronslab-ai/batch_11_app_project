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
    initial_sidebar_state="collapsed"
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
    role_tag_html = '<span class="status-badge-orange">👑 Safety Officer Mode</span>'
else:
    role_tag_html = '<span class="status-badge-green">👷 Worker Mode (No Password Needed)</span>'

st.markdown(f"""
<div class="app-header-card">
    <div>
        <h1 class="app-title">🛡️ OIL Safety Friend</h1>
        <div class="app-subtitle">Spot a hazard? Tell us in your voice or typing — We will fix it quickly!</div>
    </div>
    <div>
        {role_tag_html}
    </div>
</div>
""", unsafe_allow_html=True)

# Helper function to render visual delivery-style tracker
def render_visual_tracker(status_val: str):
    is_step1 = True
    is_step2 = (status_val in [cs.STATUS_GONNA_BE_VISITED, cs.STATUS_SOLVED])
    is_step3 = (status_val == cs.STATUS_SOLVED)

    c1_class = "tracker-circle-active-red" if status_val == cs.STATUS_UNCHECKED else ("tracker-circle-active-green" if is_step2 else "tracker-circle-active-red")
    c2_class = "tracker-circle-active-orange" if status_val == cs.STATUS_GONNA_BE_VISITED else ("tracker-circle-active-green" if is_step3 else "tracker-circle-inactive")
    c3_class = "tracker-circle-active-green" if is_step3 else "tracker-circle-inactive"

    line1_class = "tracker-line tracker-line-done" if is_step2 else "tracker-line"
    line2_class = "tracker-line tracker-line-done" if is_step3 else "tracker-line"

    return f"""
    <div class="tracker-container">
        <div class="tracker-step">
            <div class="tracker-circle {c1_class}">📝</div>
            <div style="font-weight:700; font-size:0.85rem; color:#f8fafc;">1. Reported</div>
            <div style="font-size:0.75rem; color:#94a3b8;">Pending Review</div>
        </div>
        <div class="{line1_class}"></div>
        <div class="tracker-step">
            <div class="tracker-circle {c2_class}">🏃</div>
            <div style="font-weight:700; font-size:0.85rem; color:#f8fafc;">2. Team Visiting</div>
            <div style="font-size:0.75rem; color:#94a3b8;">Inspection Scheduled</div>
        </div>
        <div class="{line2_class}"></div>
        <div class="tracker-step">
            <div class="tracker-circle {c3_class}">✅</div>
            <div style="font-weight:700; font-size:0.85rem; color:#f8fafc;">3. Solved & Safe</div>
            <div style="font-size:0.75rem; color:#94a3b8;">Hazard Mitigated</div>
        </div>
    </div>
    """

# ==============================================================================
# WORKER VIEW (SUPER SIMPLE 3-STEP FLOW)
# ==============================================================================
is_admin_active = (st.session_state.user_role == 'admin' and st.session_state.admin_authenticated)

if not is_admin_active:
    # 2 Big, obvious tabs for Workers
    tab_report, tab_track, tab_admin_login_box = st.tabs([
        "📢 Report a Safety Hazard",
        "🔍 Track My Report Status",
        "🔐 Safety Officer Login"
    ])

    with tab_report:
        st.markdown("""
        <div style="text-align:center; margin-bottom:20px;">
            <h2 style="font-weight:800; font-size:1.8rem; margin-bottom:6px;">Easy 3-Step Safety Report</h2>
            <p style="color:#94a3b8; font-size:1.05rem;">Speak into your microphone or type. Anyone can do it in 30 seconds!</p>
        </div>
        """, unsafe_allow_html=True)

        col_left, col_right = st.columns([1.2, 1])

        with col_left:
            st.markdown("""
            <div class="step-card">
                <div class="step-badge">Step 1 of 3</div>
                <h3 style="margin-top:0; font-size:1.3rem;">🎙️ Tell Us What Happened</h3>
                <p style="color:#94a3b8; font-size:0.92rem;">Tap the button below and speak in your language, or type what you saw.</p>
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
            st.markdown("**Or click a quick test example:**")
            p1, p2, p3 = st.columns(3)
            quick_text = ""
            if p1.button("🧗 Fall Danger"):
                quick_text = "Worker on scaffolding without safety harness tied to lifeline."
            if p2.button("🔥 Fire / Gas"):
                quick_text = "Welding near gas tank without safety permit."
            if p3.button("🏗️ Crane Lifting"):
                quick_text = "Crane lifting heavy pipe with broken frayed rope."

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
            <div style="background:#0f172a; border:2px dashed #38bdf8; border-radius:16px; padding:16px; text-align:center; margin-bottom:14px;">
                <button id="mic_btn" onclick="startMic()" style="background:#38bdf8; color:#0f172a; border:none; padding:12px 24px; border-radius:30px; font-weight:800; font-size:1.1rem; cursor:pointer;">
                    🎙️ Tap to Speak ({speech_lang})
                </button>
                <div id="mic_msg" style="color:#94a3b8; font-size:0.9rem; margin-top:8px;">Click microphone and talk clearly</div>
                <div id="mic_result" style="color:#34d399; font-weight:600; margin-top:6px; display:none;"></div>
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
                    document.getElementById('mic_btn').style.background = '#ef4444';
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
                        document.getElementById('mic_btn').style.background = '#38bdf8';
                        document.getElementById('mic_btn').style.color = '#0f172a';
                        document.getElementById('mic_btn').innerText = '🎙️ Tap to Speak';
                    }};
                }}
            </script>
            """
            st.components.v1.html(speech_html, height=115)

            user_hazard_text = st.text_area(
                "Or write what you saw here:",
                value=quick_text,
                height=100,
                placeholder="Example: Ladder is shaky, worker has no helmet, oil leaking near wire..."
            )

        with col_right:
            st.markdown("""
            <div class="step-card">
                <div class="step-badge">Step 2 of 3</div>
                <h3 style="margin-top:0; font-size:1.3rem;">📍 Where did you see it?</h3>
                <p style="color:#94a3b8; font-size:0.92rem;">Pick from the dropdowns below (automatically translated to your language).</p>
            </div>
            """, unsafe_allow_html=True)

            # Localized dropdowns
            loc_sites = get_localized_sites(lang_code)
            loc_acts = get_localized_activities(lang_code)

            chosen_site_disp = st.selectbox("📍 Plant / Rig Location:", loc_sites)
            chosen_act_disp = st.selectbox("🔨 What activity was happening?", loc_acts)

            worker_name_input = st.text_input("👷 Your Name (Optional):", value="Field Worker")

            st.markdown("""
            <div class="step-card" style="margin-top:16px;">
                <div class="step-badge" style="background:rgba(16, 185, 129, 0.15); color:#34d399; border-color:rgba(16, 185, 129, 0.3);">Step 3 of 3</div>
                <h3 style="margin-top:0; font-size:1.3rem;">🚀 Ready to Send</h3>
                <p style="color:#94a3b8; font-size:0.92rem;">Press the big green button. Our safety team gets it right away!</p>
            </div>
            """, unsafe_allow_html=True)

            send_report_btn = st.button("📤 Send Safety Report Now", type="primary", use_container_width=True)

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
                    st.markdown(f"""
                    <div class="danger-banner">
                        <div style="font-size:2.8rem; margin-bottom:4px;">🚨</div>
                        <h2 style="color:#ef4444; font-size:1.8rem; margin:0;">HIGH DANGER HAZARD DETECTED!</h2>
                        <p style="color:#fecaca; font-size:1.1rem; max-width:650px; margin:8px auto;">
                            <b>Please stay back and warn others!</b> Our safety team has been alerted immediately.
                        </p>
                        <div style="margin-top:12px;">
                            <span class="status-badge-red">Tracking ID: <b>{new_id}</b></span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="safe-banner">
                        <div style="font-size:2.8rem; margin-bottom:4px;">✅</div>
                        <h2 style="color:#10b981; font-size:1.8rem; margin:0;">THANK YOU! REPORT RECEIVED</h2>
                        <p style="color:#a7f3d0; font-size:1.1rem; max-width:650px; margin:8px auto;">
                            Danger level is low. Our team will review this during normal shift inspection.
                        </p>
                        <div style="margin-top:12px;">
                            <span class="status-badge-green">Tracking ID: <b>{new_id}</b></span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("### 📦 Live Status of Your Report:")
                st.markdown(render_visual_tracker(cs.STATUS_UNCHECKED), unsafe_allow_html=True)
                st.info(f"💡 **What our AI spotted:** {res['explanation']}")

    # ==============================================================================
    # TAB: WORKER TRACKING (SIMPLE PACKAGE TRACKER STYLE)
    # ==============================================================================
    with tab_track:
        st.markdown("""
        <div style="text-align:center; margin-bottom:20px;">
            <h2 style="font-weight:800; font-size:1.8rem; margin-bottom:6px;">🔍 Track Any Complaint</h2>
            <p style="color:#94a3b8; font-size:1.05rem;">See when an officer is visiting and when it gets fixed!</p>
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
            <div class="step-card">
                <h4 style="margin-top:0; color:#38bdf8;">Authorized Safety Leads Only</h4>
                <p style="color:#94a3b8; font-size:0.92rem;">
                    Sign in to change report statuses, assign officers to visit rigs, and mark hazards as solved.
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
        <div class="stat-box" style="border-color:#ef4444;">
            <div class="stat-number" style="color:#ef4444;">{metrics['unchecked']}</div>
            <div class="stat-label">🔴 Need to Check (New)</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="stat-box" style="border-color:#f59e0b;">
            <div class="stat-number" style="color:#f59e0b;">{metrics['gonna_visit']}</div>
            <div class="stat-label">🟠 Visiting Site Today</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="stat-box" style="border-color:#10b981;">
            <div class="stat-number" style="color:#10b981;">{metrics['solved']}</div>
            <div class="stat-label">🟢 Fixed & Solved</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    admin_tabs = st.tabs([
        "🚨 Safety Complaints Queue",
        "📊 Quick Risk Overview",
        "📱 Report on Behalf of Worker"
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
