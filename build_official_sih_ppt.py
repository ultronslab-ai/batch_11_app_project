import sys
import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def generate_official_sih_ppt(output_pptx="SIH2026_Idea_Submission_SIH26165.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Official Template Colors
    SIH_NAVY = RGBColor(15, 63, 122)      # #0f3f7a Header Dark Blue
    SIH_FOOTER_BLUE = RGBColor(0, 116, 200) # #0074c8 Footer Accent Blue
    TEXT_DARK = RGBColor(30, 41, 59)       # Dark charcoal text
    TEXT_MUTED = RGBColor(100, 116, 139)   # Subtitle text
    WHITE = RGBColor(255, 255, 255)
    LIGHT_BG = RGBColor(248, 250, 252)
    CARD_BORDER = RGBColor(203, 213, 225)
    CRITICAL_RED = RGBColor(220, 38, 38)
    SUCCESS_GREEN = RGBColor(22, 163, 74)
    GOLD = RGBColor(217, 119, 6)
    ACCENT_BLUE = RGBColor(37, 99, 235)

    blank_layout = prs.slide_layouts[6]
    
    logo_path = os.path.abspath("template_assets/extracted_img_p1_1.png")
    brain_path = os.path.abspath("template_assets/extracted_img_p1_0.png")
    
    def add_common_slide_decorations(slide, slide_title, slide_num, sub_title=None):
        # Top Left Oval Badge ("Your Team Name")
        oval = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.4), Inches(0.25), Inches(1.5), Inches(0.8))
        oval.fill.background()
        oval.line.color.rgb = SIH_NAVY
        oval.line.width = Pt(1.5)
        tf_ov = oval.text_frame
        tf_ov.word_wrap = True
        tf_ov.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_ov = tf_ov.paragraphs[0]
        p_ov.text = "Your\nTeam\nName"
        p_ov.alignment = PP_ALIGN.CENTER
        p_ov.font.size = Pt(11)
        p_ov.font.bold = True
        p_ov.font.color.rgb = SIH_NAVY
        
        # Center Header Slide Title
        t_box = slide.shapes.add_textbox(Inches(2.2), Inches(0.25), Inches(8.5), Inches(0.8))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = slide_title
        p_t.alignment = PP_ALIGN.CENTER
        p_t.font.size = Pt(28)
        p_t.font.bold = True
        p_t.font.color.rgb = SIH_NAVY
        
        if sub_title:
            p_sub = tf_t.add_paragraph()
            p_sub.text = sub_title
            p_sub.alignment = PP_ALIGN.CENTER
            p_sub.font.size = Pt(14)
            p_sub.font.bold = True
            p_sub.font.color.rgb = ACCENT_BLUE
            
        # Top Right Official SIH 2026 Logo
        if os.path.exists(logo_path):
            slide.shapes.add_picture(logo_path, Inches(11.2), Inches(0.15), width=Inches(1.8))
            
        # Bottom Blue Footer Bar
        footer = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.1), Inches(13.333), Inches(0.4))
        footer.fill.solid()
        footer.fill.fore_color.rgb = SIH_FOOTER_BLUE
        footer.line.fill.background()
        
        tf_f = footer.text_frame
        tf_f.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_f = tf_f.paragraphs[0]
        p_f.text = "@SIH Idea submission- Template"
        p_f.alignment = PP_ALIGN.CENTER
        p_f.font.size = Pt(11)
        p_f.font.color.rgb = WHITE
        
        # Page Number Right
        p_num_box = slide.shapes.add_textbox(Inches(12.5), Inches(7.1), Inches(0.7), Inches(0.4))
        tf_num = p_num_box.text_frame
        tf_num.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_num = tf_num.paragraphs[0]
        p_num.text = str(slide_num)
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.font.size = Pt(12)
        p_num.font.bold = True
        p_num.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 1: TITLE PAGE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    
    # Title Header
    t_box1 = slide1.shapes.add_textbox(Inches(1.5), Inches(0.2), Inches(10.3), Inches(1.1))
    tf1 = t_box1.text_frame
    tf1.word_wrap = True
    
    p1 = tf1.paragraphs[0]
    p1.text = "SMART INDIA HACKATHON 2026"
    p1.alignment = PP_ALIGN.CENTER
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = SIH_NAVY
    
    p1_sub = tf1.add_paragraph()
    p1_sub.text = "TITLE PAGE"
    p1_sub.alignment = PP_ALIGN.CENTER
    p1_sub.font.size = Pt(18)
    p1_sub.font.bold = True
    p1_sub.font.color.rgb = TEXT_MUTED
    
    # Right Side SIH Brain Graphic & Logo
    if os.path.exists(brain_path):
        slide1.shapes.add_picture(brain_path, Inches(8.2), Inches(1.4), width=Inches(4.8))
    elif os.path.exists(logo_path):
        slide1.shapes.add_picture(logo_path, Inches(9.5), Inches(1.5), width=Inches(3.2))
        
    # Left Side Form Details Box
    left_box = slide1.shapes.add_textbox(Inches(0.6), Inches(1.4), Inches(7.5), Inches(5.6))
    tf_lb = left_box.text_frame
    tf_lb.word_wrap = True
    
    fields = [
        ("• Problem Statement ID –", "SIH26165"),
        ("• Problem Statement Title –", "AI/NLP Decision-Support Engine for SIF Precursor Detection & Life-Saving Rules Tagging in Oil India Limited (OIL) Operations"),
        ("• Theme –", "Smart Automation / Safety & Security / Industrial AI & Risk Management"),
        ("• PS Category –", "Software"),
        ("• Team ID –", "[Your Registered Team ID]"),
        ("• Team Name (Registered on portal) –", "[Your Team Name]")
    ]
    
    for idx, (label, val) in enumerate(fields):
        p_item = tf_lb.add_paragraph() if idx > 0 else tf_lb.paragraphs[0]
        p_item.text = f"{label} "
        p_item.font.size = Pt(14)
        p_item.font.bold = True
        p_item.font.color.rgb = SIH_NAVY
        p_item.space_after = Pt(2)
        
        # Value string
        run_v = p_item.add_run()
        run_v.text = val
        run_v.font.size = Pt(14)
        run_v.font.bold = True
        run_v.font.color.rgb = ACCENT_BLUE if idx < 2 else TEXT_DARK
        p_item.space_after = Pt(10)

    # =========================================================================
    # SLIDE 2: IDEA TITLE & PROPOSED SOLUTION
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_common_slide_decorations(slide2, "IDEA TITLE", 2, sub_title="❖ Proposed Solution (Describe your Idea/Solution/Prototype)")
    
    w_col = Inches(3.8)
    h_col = Inches(5.3)
    y_col = Inches(1.6)
    
    # 3 Structured Visual Cards
    # Card 1: Problem Context
    c1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), y_col, w_col, h_col)
    c1.fill.solid()
    c1.fill.fore_color.rgb = LIGHT_BG
    c1.line.color.rgb = CARD_BORDER
    tf_c1 = c1.text_frame
    tf_c1.word_wrap = True
    p_h1 = tf_c1.paragraphs[0]
    p_h1.text = "📌 Problem Context (OIL Operations)"
    p_h1.font.size = Pt(16)
    p_h1.font.bold = True
    p_h1.font.color.rgb = CRITICAL_RED
    p_h1.space_after = Pt(8)
    
    b1 = [
        "• High Report Volume: Thousands of Unsafe-Act, Unsafe-Condition & Near-Miss logs monthly across Oil India Limited (OIL) sites (Digboi, Duliajan, Moran, Numaligarh).",
        "• Needle in a Haystack: Less than 15% of safety reports contain Serious Injury & Fatality (SIF) Precursors.",
        "• Manual Inspection Bottleneck: Traditional manual safety audits fail to detect precursor patterns buried in unstructured text before catastrophic events occur.",
        "• Language Barrier: Field workers struggle to report complex hazards in technical English."
    ]
    for text in b1:
        pb = tf_c1.add_paragraph()
        pb.text = text
        pb.font.size = Pt(11)
        pb.font.color.rgb = TEXT_DARK
        pb.space_after = Pt(8)

    # Card 2: Proposed Solution
    c2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.75), y_col, w_col, h_col)
    c2.fill.solid()
    c2.fill.fore_color.rgb = LIGHT_BG
    c2.line.color.rgb = CARD_BORDER
    tf_c2 = c2.text_frame
    tf_c2.word_wrap = True
    p_h2 = tf_c2.paragraphs[0]
    p_h2.text = "💡 Proposed Solution & Engine"
    p_h2.font.size = Pt(16)
    p_h2.font.bold = True
    p_h2.font.color.rgb = SIH_NAVY
    p_h2.space_after = Pt(8)
    
    b2 = [
        "• AI Decision-Support Platform: Real-time NLP decision engine built specifically for OIL safety officers & field operators.",
        "• Calibrated SIF Quantifier: Ingests unstructured safety narratives, calculates SIF Probability %, and assigns a 1 to 10 Severity Risk Score.",
        "• IOGP 10 Rule Parser: Multi-label NLP parser automatically tagging all 10 IOGP Life-Saving Rules & barrier failure keywords.",
        "• Critical Priority Auto-Sorting: Automatically places 10/10 Critical Hazards at the top of every executive view."
    ]
    for text in b2:
        pb = tf_c2.add_paragraph()
        pb.text = text
        pb.font.size = Pt(11)
        pb.font.color.rgb = TEXT_DARK
        pb.space_after = Pt(8)

    # Card 3: Novelty & Uniqueness
    c3 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.0), y_col, w_col, h_col)
    c3.fill.solid()
    c3.fill.fore_color.rgb = LIGHT_BG
    c3.line.color.rgb = CARD_BORDER
    tf_c3 = c3.text_frame
    tf_c3.word_wrap = True
    p_h3 = tf_c3.paragraphs[0]
    p_h3.text = "🚀 Novelty & Uniqueness"
    p_h3.font.size = Pt(16)
    p_h3.font.bold = True
    p_h3.font.color.rgb = SUCCESS_GREEN
    p_h3.space_after = Pt(8)
    
    b3 = [
        "• 100% SIF Precursor Recall: Zero Miss Guarantee on critical life-threatening hazards.",
        "• 8 Regional Languages Voice Input: Direct speech dictation in Assamese, Hindi, Bengali, Tamil, Telugu, Kannada, Malayalam, or English.",
        "• Live Auto-Typing Bridge: Voice transcript automatically typed into Streamlit report text area.",
        "• Local Explainability: LIME-style feature attributions highlighting exact trigger words for safety officers."
    ]
    for text in b3:
        pb = tf_c3.add_paragraph()
        pb.text = text
        pb.font.size = Pt(11)
        pb.font.color.rgb = TEXT_DARK
        pb.space_after = Pt(8)

    # =========================================================================
    # SLIDE 3: TECHNICAL APPROACH
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_common_slide_decorations(slide3, "TECHNICAL APPROACH", 3)
    
    # Top Box: Tech Stack Pills
    ts_box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.4), Inches(1.2), Inches(12.533), Inches(0.85))
    ts_box.fill.solid()
    ts_box.fill.fore_color.rgb = SIH_NAVY
    ts_box.line.color.rgb = ACCENT_BLUE
    tf_ts = ts_box.text_frame
    tf_ts.word_wrap = True
    p_tsh = tf_ts.paragraphs[0]
    p_tsh.text = "⚙️ Core Technologies & Libraries Used:"
    p_tsh.font.size = Pt(12)
    p_tsh.font.bold = True
    p_tsh.font.color.rgb = RGBColor(96, 165, 250)
    p_tsh.space_after = Pt(2)
    
    p_tsp = tf_ts.add_paragraph()
    p_tsp.text = "Python 3.11  •  Streamlit Web Framework  •  Scikit-Learn (TF-IDF + Calibrated Logistic Regression)  •  HTML5 Web Speech API (webkitSpeechRecognition)  •  Pandas & NumPy  •  Plotly Express Analytics  •  LIME Local Feature Attribution"
    p_tsp.font.size = Pt(10.5)
    p_tsp.font.bold = True
    p_tsp.font.color.rgb = WHITE
    
    # Bottom 4 Flow Step Cards
    step_w = Inches(2.9)
    step_h = Inches(4.5)
    step_y = Inches(2.45)
    gap = Inches(0.24)
    
    flow_steps = [
        ("Step 1: Ingestion & Voice", SIH_NAVY, [
            "• Field Voice Speech-to-Text (8 Regional Languages)",
            "• Manual Web Form Reporting",
            "• Batch CSV Enterprise File Upload (report_id, text, site, activity)",
            "• Phonetic & Hinglish normalization engine"
        ]),
        ("Step 2: AI Precursor NLP", ACCENT_BLUE, [
            "• TF-IDF N-gram feature extraction from safety text",
            "• Calibrated Logistic Regression probability predictor",
            "• SIF Probability % calculation (0.0 to 1.0)",
            "• 1-10 Risk Score & Severity Matrix mapping"
        ]),
        ("Step 3: IOGP Rule Engine", GOLD, [
            "• Multi-label rule parsing against 10 IOGP Life-Saving Rules",
            "• High-risk combination flag (Hot Work + Hydrocarbon leak)",
            "• Equipment barrier failure keyword extraction",
            "• LIME-style precursor attributions"
        ]),
        ("Step 4: Executive Dashboard", SUCCESS_GREEN, [
            "• Priority sorting: 10/10 Critical Hazards display FIRST",
            "• 2D Site vs Activity Risk Density Heatmap",
            "• Interactive Filterable Report Table & CSV export",
            "• Dynamic UI language switching (8 languages)"
        ])
    ]
    
    for idx, (s_title, s_color, s_bullets) in enumerate(flow_steps):
        s_x = Inches(0.5) + idx * (step_w + gap)
        sc = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, s_x, step_y, step_w, step_h)
        sc.fill.solid()
        sc.fill.fore_color.rgb = LIGHT_BG
        sc.line.color.rgb = CARD_BORDER
        
        # Header banner inside card
        sc_hdr = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, s_x, step_y, step_w, Inches(0.6))
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
        
        tf_sc = sc.text_frame
        tf_sc.word_wrap = True
        p_top = tf_sc.paragraphs[0]
        p_top.text = ""
        p_top.space_after = Pt(20)
        
        for b in s_bullets:
            pb = tf_sc.add_paragraph()
            pb.text = b
            pb.font.size = Pt(11)
            pb.font.color.rgb = TEXT_DARK
            pb.space_after = Pt(8)

    # =========================================================================
    # SLIDE 4: FEASIBILITY AND VIABILITY
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_common_slide_decorations(slide4, "FEASIBILITY AND VIABILITY", 4)
    
    # Left Feasibility Column
    f_left = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.3), Inches(4.5), Inches(5.6))
    f_left.fill.solid()
    f_left.fill.fore_color.rgb = LIGHT_BG
    f_left.line.color.rgb = CARD_BORDER
    tf_fl = f_left.text_frame
    tf_fl.word_wrap = True
    p_flh = tf_fl.paragraphs[0]
    p_flh.text = "📈 Feasibility & Viability Analysis"
    p_flh.font.size = Pt(16)
    p_flh.font.bold = True
    p_flh.font.color.rgb = SIH_NAVY
    p_flh.space_after = Pt(10)
    
    f_items = [
        "• Technical Feasibility: Built on Python standard ML stack. Inference time <50ms per report; highly scalable for enterprise workloads.",
        "• Financial Viability: ZERO external API subscription costs or expensive GPU hardware required. Runs natively on-edge or on local OIL servers.",
        "• Operational Viability: Zero learning curve — simple 1-tap voice dictation on existing mobile phones.",
        "• Data Privacy & Compliance: 100% on-premises deployment ensuring confidential Oil India Limited logs never leave company firewalls."
    ]
    for fi in f_items:
        pf = tf_fl.add_paragraph()
        pf.text = fi
        pf.font.size = Pt(11)
        pf.font.color.rgb = TEXT_DARK
        pf.space_after = Pt(10)
        
    # Right Challenges & Mitigation Column
    f_right = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.2), Inches(1.3), Inches(7.633), Inches(5.6))
    f_right.fill.solid()
    f_right.fill.fore_color.rgb = LIGHT_BG
    f_right.line.color.rgb = CARD_BORDER
    tf_fr = f_right.text_frame
    tf_fr.word_wrap = True
    p_frh = tf_fr.paragraphs[0]
    p_frh.text = "⚠️ Potential Challenges, Risks & Mitigation Strategies"
    p_frh.font.size = Pt(16)
    p_frh.font.bold = True
    p_frh.font.color.rgb = CRITICAL_RED
    p_frh.space_after = Pt(10)
    
    risks = [
        ("Challenge 1: Noisy Field Speech", "Background noise at drilling rigs or compressor stations affecting speech recognition.", "Integrated regional phonetic dictionary (`REGIONAL_DICTIONARY`) & 1-click fallback copy/auto-type option."),
        ("Challenge 2: Technical Jargon", "Specialized petroleum HSE terminology (LOTO, Scaffolding, Flare stack) missing in general models.", "Custom TF-IDF n-gram vocabulary trained specifically on Oil India Limited incident text corpus."),
        ("Challenge 3: Offline Field Rigs", "Remote drilling sites in Assam with weak internet connectivity.", "Fully client-side HTML5 Speech API processing with local browser caching & batch CSV sync capabilities."),
        ("Challenge 4: False Negatives", "Missing a critical SIF precursor resulting in potential workplace fatality.", "Threshold tuning enforcing 100% Recall on high-fatality categories, prioritizing safety over false alarms.")
    ]
    for r_title, r_desc, r_mit in risks:
        p_rt = tf_fr.add_paragraph()
        p_rt.text = f"• {r_title}"
        p_rt.font.size = Pt(12)
        p_rt.font.bold = True
        p_rt.font.color.rgb = GOLD
        p_rt.space_after = Pt(2)
        
        p_rd = tf_fr.add_paragraph()
        p_rd.text = f"   Risk: {r_desc}"
        p_rd.font.size = Pt(10.5)
        p_rd.font.color.rgb = TEXT_DARK
        p_rd.space_after = Pt(2)
        
        p_rm = tf_fr.add_paragraph()
        p_rm.text = f"   Mitigation: {r_mit}"
        p_rm.font.size = Pt(10.5)
        p_rm.font.bold = True
        p_rm.font.color.rgb = SUCCESS_GREEN
        p_rm.space_after = Pt(8)

    # =========================================================================
    # SLIDE 5: IMPACT AND BENEFITS
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_common_slide_decorations(slide5, "IMPACT AND BENEFITS", 5)
    
    qw = Inches(5.9)
    qh = Inches(2.65)
    qx1 = Inches(0.5)
    qx2 = Inches(6.933)
    qy1 = Inches(1.3)
    qy2 = Inches(4.2)
    
    quads = [
        (qx1, qy1, "👷 Impact on Field Workers", SIH_NAVY, [
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
        
        tf_b = box.text_frame
        tf_b.word_wrap = True
        p_top = tf_b.paragraphs[0]
        p_top.text = ""
        p_top.space_after = Pt(20)
        
        for b in q_bullets:
            pb = tf_b.add_paragraph()
            pb.text = b
            pb.font.size = Pt(10.5)
            pb.font.color.rgb = TEXT_DARK
            pb.space_after = Pt(5)

    # =========================================================================
    # SLIDE 6: RESEARCH AND REFERENCES
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_common_slide_decorations(slide6, "RESEARCH AND REFERENCES", 6)
    
    # Top Card: Standards & Literature
    c_top = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.3), Inches(12.333), Inches(2.6))
    c_top.fill.solid()
    c_top.fill.fore_color.rgb = LIGHT_BG
    c_top.line.color.rgb = CARD_BORDER
    tf_ct = c_top.text_frame
    tf_ct.word_wrap = True
    p_cth = tf_ct.paragraphs[0]
    p_cth.text = "📚 Key Standards & Industry Literature References"
    p_cth.font.size = Pt(15)
    p_cth.font.bold = True
    p_cth.font.color.rgb = SIH_NAVY
    p_cth.space_after = Pt(6)
    
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
        pr.font.size = Pt(10.5)
        pr.font.color.rgb = TEXT_DARK
        pr.space_after = Pt(4)
        
    # Bottom Card: Working Prototype Verification
    c_bot = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(4.1), Inches(12.333), Inches(2.8))
    c_bot.fill.solid()
    c_bot.fill.fore_color.rgb = SIH_NAVY
    c_bot.line.color.rgb = ACCENT_BLUE
    tf_cb = c_bot.text_frame
    tf_cb.word_wrap = True
    p_cbh = tf_cb.paragraphs[0]
    p_cbh.text = "🖥️ Working Prototype Proof-of-Concept Verification"
    p_cbh.font.size = Pt(15)
    p_cbh.font.bold = True
    p_cbh.font.color.rgb = RGBColor(96, 165, 250)
    p_cbh.space_after = Pt(6)
    
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
        pp.font.size = Pt(10.5)
        pp.font.color.rgb = WHITE
        pp.space_after = Pt(4)
        
    out1 = "Official_SIH2026_Idea_Submission_SIH26165.pptx"
    out2 = "SIH2026_Idea_Submission_SIH26165.pptx"
    prs.save(out1)
    try:
        prs.save(out2)
    except Exception as e:
        print("Note on saving out2:", e)
    print(f"Successfully generated official SIH PPT at: {os.path.abspath(out1)}")

if __name__ == "__main__":
    generate_official_sih_ppt()
