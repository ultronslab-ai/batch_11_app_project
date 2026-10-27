import streamlit as st

def apply_custom_css():
    """Apply clean, ultra-friendly, attractive UI styling that anyone can use easily."""
    st.markdown("""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global App Background & Clean Typography */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b 0%, #0f172a 100%);
        font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
        color: #f8fafc;
    }

    /* Friendly Header */
    .app-header-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 16px;
    }

    .app-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .app-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 500;
        margin-top: 4px;
    }

    /* Big Friendly Step Card */
    .step-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .step-card:hover {
        border-color: rgba(56, 189, 248, 0.4);
        transform: translateY(-2px);
    }

    .step-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 0.9rem;
        font-weight: 700;
        margin-bottom: 12px;
    }

    /* Super Clean Traffic Light Result Banners */
    .danger-banner {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(185, 28, 28, 0.3) 100%);
        border: 2px solid #ef4444;
        border-radius: 20px;
        padding: 24px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 0 30px rgba(239, 68, 68, 0.25);
    }

    .safe-banner {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(4, 120, 87, 0.3) 100%);
        border: 2px solid #10b981;
        border-radius: 20px;
        padding: 24px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.2);
    }

    /* 3-Step Visual Progress Tracker (Like Pizza/Delivery Tracker) */
    .tracker-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 20px 30px;
        margin: 16px 0;
        gap: 10px;
    }

    .tracker-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        flex: 1;
    }

    .tracker-circle {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        font-weight: 800;
        margin-bottom: 8px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }

    .tracker-circle-active-red {
        background: #ef4444;
        color: white;
        box-shadow: 0 0 16px rgba(239, 68, 68, 0.6);
    }

    .tracker-circle-active-orange {
        background: #f59e0b;
        color: white;
        box-shadow: 0 0 16px rgba(245, 158, 11, 0.6);
    }

    .tracker-circle-active-green {
        background: #10b981;
        color: white;
        box-shadow: 0 0 16px rgba(16, 185, 129, 0.6);
    }

    .tracker-circle-inactive {
        background: #334155;
        color: #94a3b8;
    }

    .tracker-line {
        height: 4px;
        flex: 1;
        background: #334155;
        margin: 0 8px;
        border-radius: 2px;
        margin-bottom: 24px;
    }

    .tracker-line-done {
        background: #10b981;
    }

    /* Big Friendly Metric Pill Cards */
    .stat-box {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .stat-number {
        font-size: 2.4rem;
        font-weight: 800;
        line-height: 1.1;
    }
    .stat-label {
        font-size: 0.95rem;
        font-weight: 600;
        color: #94a3b8;
        margin-top: 6px;
    }

    /* Friendly Status Badges */
    .status-badge-red {
        background: rgba(239, 68, 68, 0.2);
        color: #f87171;
        border: 1.5px solid #ef4444;
        padding: 6px 16px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .status-badge-orange {
        background: rgba(245, 158, 11, 0.2);
        color: #fbbf24;
        border: 1.5px solid #f59e0b;
        padding: 6px 16px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .status-badge-green {
        background: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1.5px solid #10b981;
        padding: 6px 16px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Button Tweaks */
    div.stButton > button:first-child {
        border-radius: 16px;
        font-weight: 700;
        font-size: 1.05rem;
        padding: 12px 24px;
        transition: all 0.2s ease;
    }

    div.stButton > button:first-child:hover {
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

SAMPLE_DEMO_TEXTS = {
    "Working at Height (High SIF)": "Scaffolding worker standing at 20 meters height without tying safety harness lanyard.",
    "Hot Work near Gas (High SIF)": "Welding pipe line near storage tank without gas test or hot work permit.",
    "Unsafe Crane Lift (High SIF)": "Crane operator lifting heavy drill pipe with cracked, broken sling over active walkway.",
    "Safe / Minor Issue (Low Risk)": "Empty water bottle and food wrappers found on break room table."
}
