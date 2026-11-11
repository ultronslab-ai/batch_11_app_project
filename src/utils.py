import streamlit as st

def apply_custom_css():
    """Apply modern, high-tech enterprise HSE portal styling."""
    st.markdown("""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Global App Canvas */
    .stApp {
        background-color: #0b0f19;
        background-image: 
            radial-gradient(at 0% 0%, rgba(14, 165, 233, 0.08) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(99, 102, 241, 0.08) 0px, transparent 50%),
            radial-gradient(at 50% 100%, rgba(15, 23, 42, 0.6) 0px, transparent 100%);
        font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
        color: #f1f5f9;
    }

    /* Streamlit Top Header & Toolbar Cleanup */
    header[data-testid="stHeader"] {
        background: rgba(11, 15, 25, 0.85) !important;
        backdrop-filter: blur(12px) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
    }

    /* Sidebar Clean Professional Dark Styling */
    section[data-testid="stSidebar"] {
        background-color: #0d1322 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        font-size: 0.95rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        color: #94a3b8 !important;
        font-weight: 700 !important;
        margin-top: 10px !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 1400px !important;
    }

    /* Enterprise Header Card */
    .app-header-card {
        background: linear-gradient(135deg, rgba(22, 31, 50, 0.85) 0%, rgba(13, 19, 34, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 24px 32px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 16px;
        backdrop-filter: blur(10px);
    }

    .oil-brand-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(245, 158, 11, 0.12);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .app-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }

    .app-subtitle {
        color: #94a3b8;
        font-size: 0.98rem;
        font-weight: 500;
        margin-top: 6px;
    }

    /* Professional Executive Cards */
    .pro-card {
        background: rgba(22, 31, 50, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(8px);
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .pro-card:hover {
        border-color: rgba(56, 189, 248, 0.3);
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.35);
    }

    .pro-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .pro-card-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #f8fafc;
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 0;
    }

    /* Traffic Light Hazard Banners */
    .danger-banner {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(153, 27, 27, 0.25) 100%);
        border: 1.5px solid #ef4444;
        border-radius: 18px;
        padding: 24px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.2);
    }

    .safe-banner {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(4, 120, 87, 0.25) 100%);
        border: 1.5px solid #10b981;
        border-radius: 18px;
        padding: 24px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.15);
    }

    /* Minimalist High-End Stepper Timeline */
    .stepper-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #111827;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 18px 28px;
        margin: 16px 0;
        gap: 12px;
    }

    .stepper-node {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        flex: 1;
    }

    .stepper-icon-circle {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        font-weight: 800;
        margin-bottom: 8px;
        transition: all 0.2s ease;
    }

    .stepper-red {
        background: #dc2626;
        color: white;
        box-shadow: 0 0 14px rgba(220, 38, 38, 0.5);
    }

    .stepper-orange {
        background: #d97706;
        color: white;
        box-shadow: 0 0 14px rgba(217, 119, 6, 0.5);
    }

    .stepper-green {
        background: #059669;
        color: white;
        box-shadow: 0 0 14px rgba(5, 150, 105, 0.5);
    }

    .stepper-inactive {
        background: #1f2937;
        color: #6b7280;
        border: 1px solid #374151;
    }

    .stepper-bar {
        height: 3px;
        flex: 1;
        background: #374151;
        margin: 0 10px;
        border-radius: 2px;
        margin-bottom: 22px;
    }

    .stepper-bar-active {
        background: #059669;
    }

    /* Executive KPI Stat Cards */
    .stat-box {
        background: linear-gradient(145deg, rgba(26, 36, 56, 0.8) 0%, rgba(17, 24, 39, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
        position: relative;
        overflow: hidden;
    }

    .stat-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
    }
    .stat-box-red::before { background: #ef4444; }
    .stat-box-orange::before { background: #f59e0b; }
    .stat-box-green::before { background: #10b981; }

    .stat-number {
        font-size: 2.6rem;
        font-weight: 800;
        line-height: 1;
        font-family: 'JetBrains Mono', monospace;
    }
    .stat-label {
        font-size: 0.88rem;
        font-weight: 600;
        color: #94a3b8;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Corporate Status Badges */
    .status-badge-red {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 5px 14px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.82rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .status-badge-orange {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.4);
        padding: 5px 14px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.82rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .status-badge-green {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 5px 14px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.82rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .status-badge-blue {
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.4);
        padding: 5px 14px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.82rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #111827;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
        font-size: 0.92rem;
        padding: 0 18px;
        border: none !important;
        background: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        background: #1e293b !important;
        color: #38bdf8 !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
    }

    /* Form Controls & Inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        background-color: #111827 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        color: #f8fafc !important;
        font-size: 0.95rem !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #0284c7 !important;
        box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.25) !important;
    }

    /* Action Buttons */
    div.stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
        padding: 10px 20px !important;
        transition: all 0.15s ease-in-out !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }

    /* Primary Accent Button */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.3) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.45) !important;
    }

    /* Native Expander Styling */
    div[data-testid="stExpander"] {
        background: rgba(17, 24, 39, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        margin-bottom: 12px !important;
        overflow: hidden !important;
    }
    div[data-testid="stExpander"] summary {
        font-weight: 600 !important;
        padding: 14px 18px !important;
    }
    </style>
    """, unsafe_allow_html=True)

SAMPLE_DEMO_TEXTS = {
    "Working at Height (High SIF)": "Scaffolding worker standing at 20 meters height without tying safety harness lanyard.",
    "Hot Work near Gas (High SIF)": "Welding pipe line near storage tank without gas test or hot work permit.",
    "Unsafe Crane Lift (High SIF)": "Crane operator lifting heavy drill pipe with cracked, broken sling over active walkway.",
    "Safe / Minor Issue (Low Risk)": "Empty water bottle and food wrappers found on break room table."
}
