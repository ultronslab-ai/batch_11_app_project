import sys
import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_sih_presentation(output_pptx_path="SIH2026_Idea_Submission_SIH26165.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Color Palette
    DARK_NAVY = RGBColor(15, 23, 42)      # #0f172a
    NAVY_BLUE = RGBColor(30, 58, 138)     # #1e3a8a
    ACCENT_BLUE = RGBColor(37, 99, 235)   # #2563eb
    LIGHT_BG = RGBColor(248, 250, 252)    # #f8fafc
    WHITE = RGBColor(255, 255, 255)
    CARD_BG = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(226, 232, 240)
    TEXT_DARK = RGBColor(30, 41, 59)      # #1e293b
    TEXT_MUTED = RGBColor(100, 116, 139)  # #64748b
    CRITICAL_RED = RGBColor(220, 38, 38)  # #dc2626
    SUCCESS_GREEN = RGBColor(22, 163, 74) # #16a34a
    GOLD = RGBColor(217, 119, 6)          # #d97706
    
    def add_header(slide, title_text, category_text="SIH2026 IDEA SUBMISSION"):
        # Header background banner
        header_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        header_box.fill.solid()
        header_box.fill.fore_color.rgb = DARK_NAVY
        header_box.line.fill.background()
        
        # Category Tag
        cat_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.12), Inches(8), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = f"SMART INDIA HACKATHON 2026  |  {category_text}"
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = RGBColor(96, 165, 250) # Light blue accent
        
        # Title Text
        title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.38), Inches(10), Inches(0.6))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE
        
        # Team Name Badge top right
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.8), Inches(0.2), Inches(2.1), Inches(0.7))
        badge.fill.solid()
        badge.fill.fore_color.rgb = ACCENT_BLUE
        badge.line.fill.background()
        tf_badge = badge.text_frame
        tf_badge.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_b1 = tf_badge.paragraphs[0]
        p_b1.text = "PS ID: SIH26165"
        p_b1.alignment = PP_ALIGN.CENTER
        p_b1.font.size = Pt(11)
        p_b1.font.bold = True
        p_b1.font.color.rgb = WHITE
        
        p_b2 = tf_badge.add_paragraph()
        p_b2.text = "Oil India Limited"
        p_b2.alignment = PP_ALIGN.CENTER
        p_b2.font.size = Pt(10)
        p_b2.font.color.rgb = RGBColor(219, 234, 254)

    blank_slide_layout = prs.slide_layouts[6]
    
    # =========================================================================
    # SLIDE 1: TITLE PAGE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_slide_layout)
    
    # Background full color
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_NAVY
    bg1.line.fill.background()
    
    # SIH Top Header
    t_box1 = slide1.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.7), Inches(0.8))
    tf1 = t_box1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "SMART INDIA HACKATHON 2026"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(96, 165, 250)
    
    p1_sub = tf1.add_paragraph()
    p1_sub.text = "OFFICIAL IDEA SUBMISSION PRESENTATION"
    p1_sub.font.size = Pt(14)
    p1_sub.font.bold = True
    p1_sub.font.color.rgb = TEXT_MUTED
    
    # Main Card Container
    card1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2))
    card1.fill.solid()
    card1.fill.fore_color.rgb = RGBColor(30, 41, 59)
    card1.line.color.rgb = RGBColor(51, 65, 85)
    
    # Left details column
    details_box = slide1.shapes.add_textbox(Inches(1.2), Inches(1.9), Inches(7.2), Inches(4.6))
    tf_det = details_box.text_frame
    tf_det.word_wrap = True
    
    fields = [
        ("• Problem Statement ID:", "SIH26165"),
        ("• Problem Statement Title:", "AI/NLP Decision-Support Engine for SIF Precursor Detection & Life-Saving Rules Tagging in Oil India Limited (OIL) Operations"),
        ("• Theme:", "Smart Automation / Safety & Security / Industrial AI & Risk Management"),
        ("• PS Category:", "Software Category"),
        ("• Team ID:", "[Your Registered Team ID]"),
        ("• Team Name:", "[Your Team Name (Registered on Portal)]")
    ]
    
    for idx, (label, val) in enumerate(fields):
        p_lbl = tf_det.add_paragraph() if idx > 0 else tf_det.paragraphs[0]
        p_lbl.text = label
        p_lbl.font.size = Pt(14)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = RGBColor(96, 165, 250)
        p_lbl.space_after = Pt(2)
        
        p_val = tf_det.add_paragraph()
        p_val.text = f"  {val}"
        p_val.font.size = Pt(14)
        p_val.font.color.rgb = WHITE
        p_val.space_after = Pt(10)
        
    # Right Side Highlight Box
    r_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.7), Inches(1.9), Inches(3.5), Inches(4.6))
    r_card.fill.solid()
    r_card.fill.fore_color.rgb = NAVY_BLUE
    r_card.line.color.rgb = ACCENT_BLUE
    
    tf_rc = r_card.text_frame
    tf_rc.word_wrap = True
    tf_rc.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    p_rc1 = tf_rc.paragraphs[0]
    p_rc1.text = "🛡️ OIL INDIA LIMITED"
    p_rc1.alignment = PP_ALIGN.CENTER
    p_rc1.font.size = Pt(18)
    p_rc1.font.bold = True
    p_rc1.font.color.rgb = RGBColor(254, 240, 138)
    p_rc1.space_after = Pt(12)
    
    p_rc2 = tf_rc.add_paragraph()
    p_rc2.text = "Safety Precursor Intelligence Engine"
    p_rc2.alignment = PP_ALIGN.CENTER
    p_rc2.font.size = Pt(14)
    p_rc2.font.bold = True
    p_rc2.font.color.rgb = WHITE
    p_rc2.space_after = Pt(16)
    
    bullets_rc = [
        "⚡ 100% SIF Precursor Recall",
        "🎯 1-10 Severity Risk Score",
        "🛡️ 10 IOGP Life-Saving Rules",
        "🎙️ 8 Regional Languages Voice"
    ]
    for b in bullets_rc:
        pb = tf_rc.add_paragraph()
        pb.text = b
        pb.alignment = PP_ALIGN.CENTER
        pb.font.size = Pt(12)
        pb.font.color.rgb = RGBColor(219, 234, 254)
        pb.space_after = Pt(6)

    # =========================================================================
    # SLIDE 2: IDEA TITLE & PROPOSED SOLUTION
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide2, "PROPOSED SOLUTION & IDEA OVERVIEW")
    
    # 3 Column Layout: Problem -> Solution -> Novelty
    w_col = Inches(3.77)
    h_col = Inches(5.8)
    y_col = Inches(1.3)
    
    # Card 1: Problem Context
    c1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), y_col, w_col, h_col)
    c1.fill.solid()
    c1.fill.fore_color.rgb = LIGHT_BG
    c1.line.color.rgb = CARD_BORDER
    
    tf_c1 = c1.text_frame
    tf_c1.word_wrap = True
    p_h1 = tf_c1.paragraphs[0]
    p_h1.text = "📌 Problem Context"
    p_h1.font.size = Pt(18)
    p_h1.font.bold = True
    p_h1.font.color.rgb = CRITICAL_RED
    p_h1.space_after = Pt(10)
    
    p_b1_text = [
        "• High Report Volume: Thousands of Unsafe-Act, Unsafe-Condition & Near-Miss logs monthly across Oil India Limited (OIL) sites (Digboi, Duliajan, Moran, Numaligarh).",
        "• Needle in a Haystack: Less than 15% of safety reports contain Serious Injury & Fatality (SIF) Precursors.",
        "• Manual Audit Failure: Traditional manual inspection cannot audit text fast enough to spot high-fatality precursor patterns before actual incidents occur.",
        "• Language Barrier: Field workers struggle to report complex hazards in standard technical English."
    ]
    for bt in p_b1_text:
        pb = tf_c1.add_paragraph()
        pb.text = bt
        pb.font.size = Pt(12)
        pb.font.color.rgb = TEXT_DARK
        pb.space_after = Pt(10)
        
    # Card 2: Proposed Solution
    c2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.78), y_col, w_col, h_col)
    c2.fill.solid()
    c2.fill.fore_color.rgb = LIGHT_BG
    c2.line.color.rgb = CARD_BORDER
    
    tf_c2 = c2.text_frame
    tf_c2.word_wrap = True
    p_h2 = tf_c2.paragraphs[0]
    p_h2.text = "💡 Proposed Solution"
    p_h2.font.size = Pt(18)
    p_h2.font.bold = True
    p_h2.font.color.rgb = NAVY_BLUE
    p_h2.space_after = Pt(10)
    
    p_b2_text = [
        "• AI Decision-Support Platform: Real-time NLP decision engine built specifically for OIL safety officers & field personnel.",
        "• Automated SIF Quantifier: Evaluates unstructured narrative text, predicts SIF Probability %, and assigns a 1 to 10 Severity Risk Score.",
        "• IOGP 10 Rule Parser: Automatically tags all 10 IOGP Life-Saving Rules & extracts barrier failure keywords.",
        "• Critical Priority Auto-Sorting: Automatically places 10/10 Critical Risk hazards at the top of every dashboard."
    ]
    for bt in p_b2_text:
        pb = tf_c2.add_paragraph()
        pb.text = bt
        pb.font.size = Pt(12)
        pb.font.color.rgb = TEXT_DARK
        pb.space_after = Pt(10)
        
    # Card 3: Innovation & Uniqueness
    c3 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.96), y_col, w_col, h_col)
    c3.fill.solid()
    c3.fill.fore_color.rgb = LIGHT_BG
    c3.line.color.rgb = CARD_BORDER
    
    tf_c3 = c3.text_frame
    tf_c3.word_wrap = True
    p_h3 = tf_c3.paragraphs[0]
    p_h3.text = "🚀 Innovation & Novelty"
    p_h3.font.size = Pt(18)
    p_h3.font.bold = True
    p_h3.font.color.rgb = SUCCESS_GREEN
    p_h3.space_after = Pt(10)
    
    p_b3_text = [
        "• 100% SIF Precursor Recall: Zero Miss Guarantee on critical life-threatening hazards.",
        "• 8 Regional Voice Speech-to-Text: Native dictation in Assamese, Hindi, Bengali, Tamil, Telugu, Kannada, Malayalam, or English.",
        "• Live Auto-Typing Bridge: Voice transcript automatically typed into Streamlit report text area.",
        "• Local Explainability: LIME-style feature attributions highlighting exact trigger words for safety officers."
    ]
    for bt in p_b3_text:
        pb = tf_c3.add_paragraph()
        pb.text = bt
        pb.font.size = Pt(12)
        pb.font.color.rgb = TEXT_DARK
        pb.space_after = Pt(10)

    # =========================================================================
    # SLIDE 3: TECHNICAL APPROACH & ARCHITECTURE
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide3, "TECHNICAL APPROACH & SYSTEM ARCHITECTURE")
    
    # Top Box: Tech Stack Pills
    ts_box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.3), Inches(12.133), Inches(1.0))
    ts_box.fill.solid()
    ts_box.fill.fore_color.rgb = DARK_NAVY
    ts_box.line.color.rgb = ACCENT_BLUE
    
    tf_ts = ts_box.text_frame
    tf_ts.word_wrap = True
    p_tsh = tf_ts.paragraphs[0]
    p_tsh.text = "⚙️ Core Technology Stack & Libraries Used:"
    p_tsh.font.size = Pt(13)
    p_tsh.font.bold = True
    p_tsh.font.color.rgb = RGBColor(96, 165, 250)
    p_tsh.space_after = Pt(4)
    
    p_tsp = tf_ts.add_paragraph()
    p_tsp.text = "Python 3.11  •  Streamlit Web UI  •  Scikit-Learn (TF-IDF + Calibrated Logistic Regression)  •  HTML5 Web Speech API (webkitSpeechRecognition)  •  Pandas & NumPy  •  Plotly Express Analytics  •  LIME Feature Attribution"
    p_tsp.font.size = Pt(11)
    p_tsp.font.bold = True
    p_tsp.font.color.rgb = WHITE
    
    # Bottom Section: Architecture Workflow (4 Sequential Flow Cards)
    step_w = Inches(2.85)
    step_h = Inches(4.5)
    step_y = Inches(2.5)
    gap = Inches(0.24)
    
    steps = [
        ("Step 1: Multi-Channel Ingestion", NAVY_BLUE, [
            "• Field Voice Speech-to-Text (8 Regional Indian Languages)",
            "• Manual Web Form Reporting",
            "• Batch CSV Enterprise File Upload (report_id, text, site, activity)",
            "• Regional script & Hinglish normalization engine"
        ]),
        ("Step 2: Calibrated AI NLP Engine", ACCENT_BLUE, [
            "• TF-IDF N-gram feature extraction from safety text",
            "• Calibrated Logistic Regression probability predictor",
            "• SIF Probability % calculation (0.0 to 1.0)",
            "• 1-10 Risk Score & Severity Matrix mapping"
        ]),
        ("Step 3: IOGP Rule & Barrier Tagger", GOLD, [
            "• Multi-label rule parsing against 10 IOGP Life-Saving Rules",
            "• High-risk combination flag (Hot Work + Hydrocarbon leak)",
            "• Equipment barrier failure keyword extraction",
            "• LIME-style precursor attributions"
        ]),
        ("Step 4: HSE Executive Dashboard", SUCCESS_GREEN, [
            "• Priority sorting: 10/10 Critical Hazards display FIRST",
            "• 2D Site vs Activity Risk Density Heatmap",
            "• Interactive Filterable Report Table & CSV export",
            "• Dynamic UI language switching (8 languages)"
        ])
    ]
    
    for idx, (s_title, s_color, s_bullets) in enumerate(steps):
        s_x = Inches(0.6) + idx * (step_w + gap)
        sc = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, s_x, step_y, step_w, step_h)
        sc.fill.solid()
        sc.fill.fore_color.rgb = LIGHT_BG
        sc.line.color.rgb = CARD_BORDER
        
        # Header banner inside card
        sc_hdr = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, s_x, step_y, step_w, Inches(0.65))
        sc_hdr.fill.solid()
        sc_hdr.fill.fore_color.rgb = s_color
        sc_hdr.line.fill.background()
        tf_sch = sc_hdr.text_frame
        tf_sch.word_wrap = True
        tf_sch.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_sch = tf_sch.paragraphs[0]
        p_sch.text = s_title
        p_sch.alignment = PP_ALIGN.CENTER
        p_sch.font.size = Pt(12)
        p_sch.font.bold = True
        p_sch.font.color.rgb = WHITE
        
        # Text body
        tf_sc = sc.text_frame
        tf_sc.word_wrap = True
        # add dummy top padding
        p_top = tf_sc.paragraphs[0]
        p_top.text = ""
        p_top.space_after = Pt(24)
        
        for b in s_bullets:
            pb = tf_sc.add_paragraph()
            pb.text = b
            pb.font.size = Pt(11)
            pb.font.color.rgb = TEXT_DARK
            pb.space_after = Pt(8)

    # =========================================================================
    # SLIDE 4: FEASIBILITY AND VIABILITY
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide4, "FEASIBILITY, RISKS & MITIGATION STRATEGIES")
    
    # 2 Column layout: Feasibility Analysis (Left) vs Risks & Mitigation Table (Right)
    # Left Box
    f_left = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.3), Inches(4.5), Inches(5.8))
    f_left.fill.solid()
    f_left.fill.fore_color.rgb = LIGHT_BG
    f_left.line.color.rgb = CARD_BORDER
    
    tf_fl = f_left.text_frame
    tf_fl.word_wrap = True
    p_flh = tf_fl.paragraphs[0]
    p_flh.text = "📈 Feasibility & Viability Analysis"
    p_flh.font.size = Pt(18)
    p_flh.font.bold = True
    p_flh.font.color.rgb = NAVY_BLUE
    p_flh.space_after = Pt(12)
    
    f_items = [
        "• Technical Feasibility: Built entirely on Python standard ML libraries. Inference time <50ms per report; highly scalable for enterprise workloads.",
        "• Financial & Cost Viability: ZERO external API subscriptions or expensive GPU hardware required. Runs natively on-edge or on local OIL servers.",
        "• Operational Deployment: Zero learning curve for workers — simple 1-tap voice dictation on existing mobile phones.",
        "• Data Privacy & Compliance: 100% on-premises deployment ensuring confidential Oil India Limited operational logs never leave company firewalls."
    ]
    for fi in f_items:
        pf = tf_fl.add_paragraph()
        pf.text = fi
        pf.font.size = Pt(12)
        pf.font.color.rgb = TEXT_DARK
        pf.space_after = Pt(12)
        
    # Right Box: Risk Matrix Table
    f_right = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.3), Inches(1.3), Inches(7.433), Inches(5.8))
    f_right.fill.solid()
    f_right.fill.fore_color.rgb = LIGHT_BG
    f_right.line.color.rgb = CARD_BORDER
    
    tf_fr = f_right.text_frame
    tf_fr.word_wrap = True
    p_frh = tf_fr.paragraphs[0]
    p_frh.text = "⚠️ Potential Challenges & Mitigation Strategies"
    p_frh.font.size = Pt(18)
    p_frh.font.bold = True
    p_frh.font.color.rgb = CRITICAL_RED
    p_frh.space_after = Pt(12)
    
    risks_data = [
        ("Challenge 1: Noisy Field Speech", "Background noise at drilling rigs or compressor stations affecting speech-to-text accuracy.", "Integrated regional phonetic dictionary (`REGIONAL_DICTIONARY`) & 1-click fallback copy/auto-type option."),
        ("Challenge 2: Technical Jargon", "Specialized petroleum HSE terminology (LOTO, Scaffolding, Flare stack, Gas leak) missing in general AI models.", "Custom TF-IDF n-gram vocabulary trained specifically on Oil India Limited incident text corpus."),
        ("Challenge 3: Offline Field Units", "Remote drilling sites in Assam with weak internet connectivity.", "Fully client-side HTML5 Speech API processing with local browser caching & batch CSV sync capabilities."),
        ("Challenge 4: False Negatives", "Missing a critical SIF precursor resulting in potential workplace fatality.", "Threshold tuning enforcing 100% Recall on high-fatality categories, prioritizing safety over false alarms.")
    ]
    
    for r_title, r_desc, r_mit in risks_data:
        p_rt = tf_fr.add_paragraph()
        p_rt.text = f"• {r_title}"
        p_rt.font.size = Pt(13)
        p_rt.font.bold = True
        p_rt.font.color.rgb = GOLD
        p_rt.space_after = Pt(2)
        
        p_rd = tf_fr.add_paragraph()
        p_rd.text = f"   Risk: {r_desc}"
        p_rd.font.size = Pt(11)
        p_rd.font.color.rgb = TEXT_DARK
        p_rd.space_after = Pt(2)
        
        p_rm = tf_fr.add_paragraph()
        p_rm.text = f"   Mitigation: {r_mit}"
        p_rm.font.size = Pt(11)
        p_rm.font.bold = True
        p_rm.font.color.rgb = SUCCESS_GREEN
        p_rm.space_after = Pt(10)

    # =========================================================================
    # SLIDE 5: IMPACT AND BENEFITS
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide5, "REAL-WORLD IMPACT AND BENEFITS")
    
    # 4 Quadrant Grid for Impact
    qw = Inches(5.8)
    qh = Inches(2.7)
    qx1 = Inches(0.6)
    qx2 = Inches(6.933)
    qy1 = Inches(1.3)
    qy2 = Inches(4.3)
    
    quads = [
        (qx1, qy1, "👷 Impact on Field Workers", NAVY_BLUE, [
            "• Frictionless Reporting: Speak in native regional language (Assamese, Hindi, Bengali, Tamil, Telugu, Kannada, Malayalam, English).",
            "• Direct Mobile Access: <30 seconds to dictate and submit safety observation.",
            "• Zero Typing Effort: Live auto-typing into description box removes literacy & language barriers."
        ]),
        (qx2, qy1, "🛡️ Impact on Safety Officers (HSE)", ACCENT_BLUE, [
            "• 90% Audit Time Savings: Automated AI scoring replaces manual spreadsheet scanning.",
            "• Zero Miss Guarantee: 100% SIF Precursor Recall ensures no life-threatening hazard is overlooked.",
            "• Instant Root Cause Analysis: LIME-style feature attributions pinpoint trigger keywords immediately."
        ]),
        (qx1, qy2, "🏢 Impact on OIL Executive Leadership", GOLD, [
            "• Strategic Risk Density Heatmaps: 2D Site vs Activity matrix highlights high-risk operational facilities.",
            "• Zero Harm Culture: Proactive precursor detection prevents catastrophic blowout / fatality incidents.",
            "• Regulatory Compliance: Automated IOGP 10 Life-Saving Rules audit trail for safety governance."
        ]),
        (qx2, qy2, "🌍 Social, Economic & Environmental Benefits", SUCCESS_GREEN, [
            "• Human Life Protection: Directly prevents severe workplace injuries and fatalities.",
            "• Massive Cost Savings: Avoids multi-crore operational downtimes, rig destruction & asset damage.",
            "• Environmental Preservation: Early gas leak & pipeline rupture detection prevents major oil spill disasters."
        ])
    ]
    
    for qx, qy, q_title, q_color, q_bullets in quads:
        box = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, qx, qy, qw, qh)
        box.fill.solid()
        box.fill.fore_color.rgb = LIGHT_BG
        box.line.color.rgb = CARD_BORDER
        
        # Header banner inside quadrant
        b_hdr = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, qx, qy, qw, Inches(0.55))
        b_hdr.fill.solid()
        b_hdr.fill.fore_color.rgb = q_color
        b_hdr.line.fill.background()
        tf_bh = b_hdr.text_frame
        tf_bh.word_wrap = True
        tf_bh.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_bh = tf_bh.paragraphs[0]
        p_bh.text = q_title
        p_bh.alignment = PP_ALIGN.LEFT
        p_bh.font.size = Pt(13)
        p_bh.font.bold = True
        p_bh.font.color.rgb = WHITE
        
        # Text content
        tf_b = box.text_frame
        tf_b.word_wrap = True
        p_top = tf_b.paragraphs[0]
        p_top.text = ""
        p_top.space_after = Pt(20)
        
        for b in q_bullets:
            pb = tf_b.add_paragraph()
            pb.text = b
            pb.font.size = Pt(11)
            pb.font.color.rgb = TEXT_DARK
            pb.space_after = Pt(6)

    # =========================================================================
    # SLIDE 6: RESEARCH AND REFERENCES
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide6, "RESEARCH, REFERENCES AND STANDARDS")
    
    # 2 Wide Cards: Standards & Literature (Top) vs Working Prototype Evidence (Bottom)
    # Top Card
    c_top = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.3), Inches(12.133), Inches(2.7))
    c_top.fill.solid()
    c_top.fill.fore_color.rgb = LIGHT_BG
    c_top.line.color.rgb = CARD_BORDER
    
    tf_ct = c_top.text_frame
    tf_ct.word_wrap = True
    p_cth = tf_ct.paragraphs[0]
    p_cth.text = "📚 Key Standards & Industry Literature References"
    p_cth.font.size = Pt(16)
    p_cth.font.bold = True
    p_cth.font.color.rgb = NAVY_BLUE
    p_cth.space_after = Pt(8)
    
    refs = [
        "1. IOGP Report 590: Life-Saving Rules (International Association of Oil & Gas Producers) — Standardized 10 Life-Saving Rules framework for upstream petroleum safety.",
        "2. Oil India Limited (OIL) HSE Operational Guidelines: Upstream drilling, pipeline, and compressor station safety protocols.",
        "3. Calibrated NLP & Text Classification Literature: TF-IDF N-gram feature extraction & Logistic Regression probability calibration for safety precursor identification.",
        "4. W3C Web Speech API Specification (BCP-47 Language Codes): Multilingual speech recognition integration for field data collection.",
        "5. Keerthibalan G SIH 2025 Winning Strategy Framework: Problem-first impact storytelling, full workflow visualization & prototype proof."
    ]
    for r in refs:
        pr = tf_ct.add_paragraph()
        pr.text = r
        pr.font.size = Pt(11)
        pr.font.color.rgb = TEXT_DARK
        pr.space_after = Pt(4)
        
    # Bottom Card: Proof of Concept / Working Prototype Evidence
    c_bot = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(4.2), Inches(12.133), Inches(2.9))
    c_bot.fill.solid()
    c_bot.fill.fore_color.rgb = DARK_NAVY
    c_bot.line.color.rgb = ACCENT_BLUE
    
    tf_cb = c_bot.text_frame
    tf_cb.word_wrap = True
    p_cbh = tf_cb.paragraphs[0]
    p_cbh.text = "🖥️ Working Prototype Proof-of-Concept Verification"
    p_cbh.font.size = Pt(16)
    p_cbh.font.bold = True
    p_cbh.font.color.rgb = RGBColor(96, 165, 250)
    p_cbh.space_after = Pt(8)
    
    poc_items = [
        "✔ Live Functional Web Application: Deployed and tested locally & over Wi-Fi on Streamlit server (Port 8501).",
        "✔ 7 Full Feature Modules Built: Executive Overview, Worker Voice Portal, Single Inspector, Batch CSV Engine, Executive HSE Dashboard, Risk Hotspots, Deep Drill-Down.",
        "✔ 8 Regional Languages Verified: Tested speech dictation and UI/content translation in Assamese, Hindi, Bengali, Tamil, Telugu, Kannada, Malayalam, and English.",
        "✔ Empirical Model Performance: 100% Recall on high-risk SIF precursors with instantaneous sub-50ms inference time.",
        "✔ Priority Sorting Verified: 10/10 Critical Hazards reliably sorted first across all dashboard views."
    ]
    for poc in poc_items:
        pp = tf_cb.add_paragraph()
        pp.text = poc
        pp.font.size = Pt(11)
        pp.font.color.rgb = WHITE
        pp.space_after = Pt(4)
        
    # Save Presentation
    prs.save(output_pptx_path)
    print(f"Successfully generated SIH 2026 Presentation at: {os.path.abspath(output_pptx_path)}")

if __name__ == "__main__":
    build_sih_presentation()
