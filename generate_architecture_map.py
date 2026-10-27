import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def create_technical_approach_map(output_path="technical_approach_map.png"):
    # Set up 16:9 figure with high DPI
    fig, ax = plt.subplots(figsize=(13.333, 5.4), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 13.333)
    ax.set_ylim(0, 5.4)
    ax.axis('off')
    
    # Color Palette
    NAVY = '#0f3f7a'
    BLUE_ACCENT = '#1f6feb'
    DASH_BLUE = '#0284c7'
    RED_ACCENT = '#dc2626'
    GREEN_ACCENT = '#16a34a'
    GOLD_ACCENT = '#d97706'
    DARK_TEXT = '#1e293b'
    CARD_BG = '#f8fafc'

    # Title Sub-header
    ax.text(6.666, 5.15, "SYSTEM ARCHITECTURE & TECHNICAL WORKFLOW MAP", 
            ha='center', va='center', fontsize=15, fontweight='bold', color=NAVY)
    ax.plot([0.4, 12.933], [4.9, 4.9], color='#cbd5e1', linestyle='--', linewidth=1.5)

    # Function to draw rounded dashed container box
    def draw_dashed_box(x, y, w, h, title, title_color=NAVY, bg_color=CARD_BG, border_color=DASH_BLUE):
        rect = patches.FancyBboxPatch((x, y), w, h,
                                    boxstyle="round,pad=0.08,rounding_size=0.15",
                                    linewidth=2, linestyle='--',
                                    edgecolor=border_color, facecolor=bg_color)
        ax.add_patch(rect)
        if title:
            hp_w = len(title) * 0.10 + 0.35
            hp = patches.FancyBboxPatch((x + w/2 - hp_w/2, y + h - 0.22), hp_w, 0.38,
                                        boxstyle="round,pad=0.04,rounding_size=0.1",
                                        linewidth=1, edgecolor=title_color, facecolor=title_color)
            ax.add_patch(hp)
            ax.text(x + w/2, y + h - 0.03, title, ha='center', va='center',
                    fontsize=9.5, fontweight='bold', color='#ffffff')

    # 1. LEFT BOXES: INPUT & INGESTION SOURCES
    draw_dashed_box(0.4, 3.25, 3.2, 1.45, "MULTILINGUAL VOICE INPUT", NAVY, '#f0f9ff', DASH_BLUE)
    ax.text(0.6, 4.25, "• Native Web Speech API Engine", fontsize=8.5, fontweight='bold', color=DARK_TEXT)
    ax.text(0.6, 3.95, "• 8 Indian Languages (AS, HI, BN,", fontsize=8, color=DARK_TEXT)
    ax.text(0.6, 3.75, "  TA, TE, KN, ML, EN)", fontsize=8, color=DARK_TEXT)
    ax.text(0.6, 3.48, "• Auto-typing JS Bridge into Text Box", fontsize=8, fontweight='bold', color=BLUE_ACCENT)

    draw_dashed_box(0.4, 1.7, 3.2, 1.45, "FIELD WORKER PORTAL", NAVY, '#f0f9ff', DASH_BLUE)
    ax.text(0.6, 2.7, "• Operator Incident Reporting", fontsize=8.5, fontweight='bold', color=DARK_TEXT)
    ax.text(0.6, 2.43, "• Regional Phonetic Normalizer", fontsize=8, color=DARK_TEXT)
    ax.text(0.6, 2.22, "• 1-Tap Voice Dictation Component", fontsize=8, color=DARK_TEXT)
    ax.text(0.6, 1.93, "• <30s Rapid Mobile Submission", fontsize=8, fontweight='bold', color=GREEN_ACCENT)

    draw_dashed_box(0.4, 0.15, 3.2, 1.45, "BATCH CSV INGESTION", NAVY, '#f0f9ff', DASH_BLUE)
    ax.text(0.6, 1.15, "• OIL Enterprise Incident Logs", fontsize=8.5, fontweight='bold', color=DARK_TEXT)
    ax.text(0.6, 0.88, "• Sites: Digboi, Duliajan, Moran...", fontsize=8, color=DARK_TEXT)
    ax.text(0.6, 0.67, "• Automated Text Preprocessing", fontsize=8, color=DARK_TEXT)
    ax.text(0.6, 0.38, "• Ground Truth Benchmark Evaluation", fontsize=8, fontweight='bold', color=GOLD_ACCENT)

    # 2. CENTRAL CORE PROCESSOR: CALIBRATED AI/NLP DECISION ENGINE
    draw_dashed_box(4.1, 0.15, 4.9, 4.55, "CALIBRATED AI/NLP DECISION CORE", NAVY, '#ffffff', '#1f6feb')
    
    # Inner Model Boxes
    m1 = patches.FancyBboxPatch((4.3, 3.2), 4.5, 1.1, boxstyle="round,pad=0.05,rounding_size=0.1",
                                linewidth=1.5, edgecolor=BLUE_ACCENT, facecolor='#eff6ff')
    ax.add_patch(m1)
    ax.text(4.5, 3.95, "[Engine 1] Calibrated SIF Classifier", fontsize=9.5, fontweight='bold', color=NAVY)
    ax.text(4.5, 3.65, "• TF-IDF N-gram Vectorizer + Calibrated Logistic Regression", fontsize=8, color=DARK_TEXT)
    ax.text(4.5, 3.4, "• Predicts SIF Probability % (0.0-1.0) & 1-10 Risk Score", fontsize=8, fontweight='bold', color=BLUE_ACCENT)

    m2 = patches.FancyBboxPatch((4.3, 1.9), 4.5, 1.1, boxstyle="round,pad=0.05,rounding_size=0.1",
                                linewidth=1.5, edgecolor=GREEN_ACCENT, facecolor='#f0fdf4')
    ax.add_patch(m2)
    ax.text(4.5, 2.65, "[Engine 2] IOGP 10 Life-Saving Rules Tagger", fontsize=9.5, fontweight='bold', color=GREEN_ACCENT)
    ax.text(4.5, 2.35, "• Multi-label NLP Regex & Semantic Pattern Parser", fontsize=8, color=DARK_TEXT)
    ax.text(4.5, 2.1, "• Energy Isolation, Hot Work, Line of Fire, Confined Space...", fontsize=8, color=DARK_TEXT)

    m3 = patches.FancyBboxPatch((4.3, 0.6), 4.5, 1.1, boxstyle="round,pad=0.05,rounding_size=0.1",
                                linewidth=1.5, edgecolor=GOLD_ACCENT, facecolor='#fffbeb')
    ax.add_patch(m3)
    ax.text(4.5, 1.35, "[Engine 3] Barrier Failure & LIME Attribution", fontsize=9.5, fontweight='bold', color=GOLD_ACCENT)
    ax.text(4.5, 1.05, "• Extracts equipment barrier breakdown keywords", fontsize=8, color=DARK_TEXT)
    ax.text(4.5, 0.8, "• LIME precursor word highlights for Safety Officers", fontsize=8, color=DARK_TEXT)

    # 3. RIGHT BOXES: OUTPUT & EXECUTIVE DASHBOARD ACTIONS
    draw_dashed_box(9.5, 3.25, 3.4, 1.45, "PRIORITY HAZARD ALERTING", RED_ACCENT, '#fef2f2', RED_ACCENT)
    ax.text(9.7, 4.25, "• 10/10 Critical Risks Sorted FIRST", fontsize=8.5, fontweight='bold', color=RED_ACCENT)
    ax.text(9.7, 3.98, "• Zero Miss Guarantee (100% SIF Recall)", fontsize=8, fontweight='bold', color=DARK_TEXT)
    ax.text(9.7, 3.75, "• Instant Safety Officer Notifications", fontsize=8, color=DARK_TEXT)
    ax.text(9.7, 3.48, "• High-Risk Combo Alert (Hot Work + Gas)", fontsize=8, color=DARK_TEXT)

    draw_dashed_box(9.5, 1.7, 3.4, 1.45, "RISK DENSITY HEATMAP", GOLD_ACCENT, '#fffbeb', GOLD_ACCENT)
    ax.text(9.7, 2.7, "• 2D Site vs Activity Risk Density Matrix", fontsize=8.5, fontweight='bold', color=DARK_TEXT)
    ax.text(9.7, 2.43, "• Operational Risk Hotspots (Digboi...)", fontsize=8, color=DARK_TEXT)
    ax.text(9.7, 2.22, "• Monthly SIF Precursor Trend Charts", fontsize=8, color=DARK_TEXT)
    ax.text(9.7, 1.93, "• Targeted Preventive HSE Audits", fontsize=8, fontweight='bold', color=GOLD_ACCENT)

    draw_dashed_box(9.5, 0.15, 3.4, 1.45, "EXECUTIVE HSE DASHBOARD", NAVY, '#f0f9ff', DASH_BLUE)
    ax.text(9.7, 1.15, "• Filterable Report Inspection Table", fontsize=8.5, fontweight='bold', color=DARK_TEXT)
    ax.text(9.7, 0.88, "• Dynamic 8-Language UI Switcher", fontsize=8, color=DARK_TEXT)
    ax.text(9.7, 0.67, "• Exportable Audit Log Reports (CSV)", fontsize=8, color=DARK_TEXT)
    ax.text(9.7, 0.38, "• Sub-50ms Real-Time Inference Latency", fontsize=8, fontweight='bold', color=BLUE_ACCENT)

    # 4. CONNECTING ARROWS
    arrow_props = dict(arrowstyle="->", color='#2563eb', lw=2, mutation_scale=14)
    red_arrow_props = dict(arrowstyle="->", color='#dc2626', lw=2.5, ls='--', mutation_scale=14)

    ax.annotate('', xy=(4.1, 3.97), xytext=(3.6, 3.97), arrowprops=arrow_props)
    ax.annotate('', xy=(4.1, 2.42), xytext=(3.6, 2.42), arrowprops=arrow_props)
    ax.annotate('', xy=(4.1, 0.87), xytext=(3.6, 0.87), arrowprops=arrow_props)

    ax.annotate('', xy=(9.5, 3.97), xytext=(9.0, 3.97), arrowprops=red_arrow_props)
    ax.annotate('', xy=(9.5, 2.42), xytext=(9.0, 2.42), arrowprops=arrow_props)
    ax.annotate('', xy=(9.5, 0.87), xytext=(9.0, 0.87), arrowprops=arrow_props)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#ffffff')
    plt.close()
    print(f"Successfully generated architecture map image at: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    create_technical_approach_map()
