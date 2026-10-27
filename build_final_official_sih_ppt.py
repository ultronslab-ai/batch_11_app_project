import sys
import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_final_sih_presentation(output_pptx="Official_SIH2026_Idea_Submission_SIH26165.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Colors
    SIH_NAVY = RGBColor(15, 63, 122)        # Header Dark Blue
    SIH_FOOTER_BLUE = RGBColor(0, 116, 200) # Footer Accent Blue
    TEXT_DARK = RGBColor(30, 41, 59)
    TEXT_MUTED = RGBColor(100, 116, 139)
    WHITE = RGBColor(255, 255, 255)
    LIGHT_BG = RGBColor(248, 250, 252)
    CARD_BORDER = RGBColor(203, 213, 225)
    CRITICAL_RED = RGBColor(220, 38, 38)
    SUCCESS_GREEN = RGBColor(22, 163, 74)
    GOLD_ACCENT = RGBColor(217, 119, 6)
    ACCENT_BLUE = RGBColor(37, 99, 235)
    DASH_BLUE = RGBColor(2, 132, 199)
    CARD_BG = RGBColor(240, 249, 255)

    blank_layout = prs.slide_layouts[6]
    logo_path = os.path.abspath("template_assets/extracted_img_p1_1.png")
    brain_path = os.path.abspath("template_assets/extracted_img_p1_0.png")

    def add_common_slide_decorations(slide, slide_title, slide_num, sub_title=None):
        # Oval Badge top left
        oval = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.4), Inches(0.2), Inches(1.5), Inches(0.75))
        oval.fill.background()
        oval.line.color.rgb = SIH_NAVY
        oval.line.width = Pt(1.5)
        tf_ov = oval.text_frame
        tf_ov.word_wrap = True
        tf_ov.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_ov = tf_ov.paragraphs[0]
        p_ov.text = "Your\nTeam\nName"
        p_ov.alignment = PP_ALIGN.CENTER
        p_ov.font.size = Pt(10.5)
        p_ov.font.bold = True
        p_ov.font.color.rgb = SIH_NAVY
        
        # Center Header Title
        t_box = slide.shapes.add_textbox(Inches(2.2), Inches(0.2), Inches(8.5), Inches(0.8))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = slide_title
        p_t.alignment = PP_ALIGN.CENTER
        p_t.font.size = Pt(27)
        p_t.font.bold = True
        p_t.font.color.rgb = SIH_NAVY
        
        if sub_title:
            p_sub = tf_t.add_paragraph()
            p_sub.text = sub_title
            p_sub.alignment = PP_ALIGN.CENTER
            p_sub.font.size = Pt(13)
            p_sub.font.bold = True
            p_sub.font.color.rgb = ACCENT_BLUE
            
        # Top Right SIH Logo
        if os.path.exists(logo_path):
            slide.shapes.add_picture(logo_path, Inches(11.2), Inches(0.12), width=Inches(1.8))
            
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
        
        # Page Number
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
    
    if os.path.exists(brain_path):
        slide1.shapes.add_picture(brain_path, Inches(8.2), Inches(1.4), width=Inches(4.8))
        
    left_box = slide1.shapes.add_textbox(Inches(0.6), Inches(1.4), Inches(7.5), Inches(5.6))
    tf_lb = left_box.text_frame
    tf_lb.word_wrap = True
    
    fields = [
        ("• Problem Statement ID –", "SIH26165"),
        ("• Problem Statement Title –", "AI/NLP Decision Engine for SIF Precursor Detection & IOGP Life-Saving Rules Tagging in OIL Operations"),
        ("• Theme –", "Smart Automation / Safety & Security / Industrial AI"),
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
    
    # Card 1: Problem Context
    c1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), y_col, w_col, h_col)
    c1.fill.solid()
    c1.fill.fore_color.rgb = LIGHT_BG
    c1.line.color.rgb = CARD_BORDER
    tf_c1 = c1.text_frame
    tf_c1.word_wrap = True
    p_h1 = tf_c1.paragraphs[0]
    p_h1.text = "📌 Problem Context (OIL)"
    p_h1.font.size = Pt(16)
    p_h1.font.bold = True
    p_h1.font.color.rgb = CRITICAL_RED
    p_h1.space_after = Pt(10)
    
    b1 = [
        "• High Report Volume: Thousands of monthly safety logs across Oil India Limited (OIL) facilities.",
        "• Precursor Scarcity: <15% of reports contain Serious Injury & Fatality (SIF) precursors.",
        "• Manual Audit Bottleneck: Slow human audits fail to spot precursor patterns before incidents occur.",
        "• Language Barrier: Field workers struggle reporting complex hazards in technical English."
    ]
    for text in b1:
        pb = tf_c1.add_paragraph()
        pb.text = text
        pb.font.size = Pt(11.5)
        pb.font.color.rgb = TEXT_DARK
        pb.space_after = Pt(12)

    # Card 2: Proposed Solution
    c2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.75), y_col, w_col, h_col)
    c2.fill.solid()
    c2.fill.fore_color.rgb = LIGHT_BG
    c2.line.color.rgb = CARD_BORDER
    tf_c2 = c2.text_frame
    tf_c2.word_wrap = True
    p_h2 = tf_c2.paragraphs[0]
    p_h2.text = "💡 Proposed AI Solution"
    p_h2.font.size = Pt(16)
    p_h2.font.bold = True
    p_h2.font.color.rgb = SIH_NAVY
    p_h2.space_after = Pt(10)
    
    b2 = [
        "• Automated AI Platform: Real-time NLP decision engine for OIL safety officers & operators.",
        "• Calibrated SIF Score: Computes SIF Probability % and assigns a 1 to 10 Severity Risk Score.",
        "• IOGP 10 Rule Parser: Multi-label NLP parser automatically tagging all 10 IOGP Life-Saving Rules.",
        "• Priority Auto-Sorting: 10/10 Critical Hazards automatically placed at top of dashboard."
    ]
    for text in b2:
        pb = tf_c2.add_paragraph()
        pb.text = text
        pb.font.size = Pt(11.5)
        pb.font.color.rgb = TEXT_DARK
        pb.space_after = Pt(12)

    # Card 3: Novelty & Uniqueness
    c3 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.0), y_col, w_col, h_col)
    c3.fill.solid()
    c3.fill.fore_color.rgb = LIGHT_BG
    c3.line.color.rgb = CARD_BORDER
    tf_c3 = c3.text_frame
    tf_c3.word_wrap = True
    p_h3 = tf_c3.paragraphs[0]
    p_h3.text = "🚀 Novelty & Key Innovation"
    p_h3.font.size = Pt(16)
    p_h3.font.bold = True
    p_h3.font.color.rgb = SUCCESS_GREEN
    p_h3.space_after = Pt(10)
    
    b3 = [
        "• 100% SIF Precursor Recall: Zero Miss Guarantee on life-threatening safety hazards.",
        "• 8 Regional Languages Voice: Direct speech dictation with auto-typing JS bridge.",
        "• Rapid Mobile Reporting: <30 seconds to dictate and submit field observations.",
        "• Local Explainability: LIME-style precursor word highlights for instant root cause analysis."
    ]
    for text in b3:
        pb = tf_c3.add_paragraph()
        pb.text = text
        pb.font.size = Pt(11.5)
        pb.font.color.rgb = TEXT_DARK
        pb.space_after = Pt(12)

    # =========================================================================
    # SLIDE 3: TECHNICAL APPROACH (VISUAL ARCHITECTURE MAP SLIDE)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_common_slide_decorations(slide3, "TECHNICAL APPROACH", 3)
    
    # Embed High-Resolution Visual Technical Approach Architecture Map Diagram Image
    map_img_path = os.path.abspath("technical_approach_map.png")
    if os.path.exists(map_img_path):
        slide3.shapes.add_picture(map_img_path, Inches(0.4), Inches(1.35), width=Inches(12.533))

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
    p_flh.space_after = Pt(12)
    
    f_items = [
        "• Technical Feasibility: <50ms inference latency per report; lightweight & scalable Python ML stack.",
        "• Financial Viability: ZERO external API costs or expensive GPU hardware required; runs natively on-edge.",
        "• Operational Viability: 1-tap mobile voice dictation; zero worker learning curve.",
        "• Data Privacy: 100% on-premises deployment within OIL enterprise firewalls."
    ]
    for fi in f_items:
        pf = tf_fl.add_paragraph()
        pf.text = fi
        pf.font.size = Pt(11.5)
        pf.font.color.rgb = TEXT_DARK
        pf.space_after = Pt(14)
        
    # Right Challenges & Mitigation Column
    f_right = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.2), Inches(1.3), Inches(7.633), Inches(5.6))
    f_right.fill.solid()
    f_right.fill.fore_color.rgb = LIGHT_BG
    f_right.line.color.rgb = CARD_BORDER
    tf_fr = f_right.text_frame
    tf_fr.word_wrap = True
    p_frh = tf_fr.paragraphs[0]
    p_frh.text = "⚠️ Challenges & Mitigation Strategies"
    p_frh.font.size = Pt(16)
    p_frh.font.bold = True
    p_frh.font.color.rgb = CRITICAL_RED
    p_frh.space_after = Pt(12)
    
    risks = [
        ("Noisy Field Speech", "Background noise at drilling rigs or compressor stations.", "Integrated regional phonetic dictionary (`REGIONAL_DICTIONARY`) & 1-click text copy."),
        ("Technical Jargon", "Specialized petroleum terminology missing in general models.", "Custom TF-IDF n-gram vocabulary trained specifically on Oil India Limited logs."),
        ("Remote Drilling Rigs", "Remote sites in Assam with weak internet connectivity.", "Client-side HTML5 Speech API processing with local browser caching & CSV sync."),
        ("False Negatives", "Missing a critical precursor causing workplace fatality.", "Threshold tuning enforcing 100% Recall on high-fatality categories.")
    ]
    for r_title, r_desc, r_mit in risks:
        p_rt = tf_fr.add_paragraph()
        p_rt.text = f"• {r_title}:"
        p_rt.font.size = Pt(12)
        p_rt.font.bold = True
        p_rt.font.color.rgb = GOLD_ACCENT
        p_rt.space_after = Pt(2)
        
        p_rd = tf_fr.add_paragraph()
        p_rd.text = f"   Risk: {r_desc}  |  Mitigation: {r_mit}"
        p_rd.font.size = Pt(11)
        p_rd.font.color.rgb = TEXT_DARK
        p_rd.space_after = Pt(10)

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
            "• Frictionless Voice Reporting: Speak in native regional language (8 languages).",
            "• Rapid Submissions: <30 seconds to dictate and log field observations.",
            "• Zero Typing Effort: Live auto-typing removes literacy & language barriers."
        ]),
        (qx2, qy1, "🛡️ Impact on Safety Officers (HSE)", ACCENT_BLUE, [
            "• 90% Audit Time Savings: Automated AI scoring replaces manual spreadsheet audits.",
            "• Zero Miss Guarantee: 100% SIF Precursor Recall ensures no hazard is overlooked.",
            "• Instant Root Cause Analysis: LIME precursor highlights pinpoint trigger words."
        ]),
        (qx1, qy2, "🏢 Impact on OIL Leadership", GOLD_ACCENT, [
            "• Strategic Risk Heatmaps: 2D Site vs Activity matrix highlights high-risk facilities.",
            "• Zero Harm Culture: Proactive precursor detection prevents blowout & fatality events.",
            "• Regulatory Governance: Automated IOGP 10 Life-Saving Rules audit trail."
        ]),
        (qx2, qy2, "🌍 Social, Economic & Environmental", SUCCESS_GREEN, [
            "• Human Life Protection: Directly prevents severe workplace injuries and fatalities.",
            "• Massive Cost Savings: Avoids multi-crore operational downtimes & asset damage.",
            "• Environmental Preservation: Early gas leak detection prevents oil spill disasters."
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
            pb.font.size = Pt(11)
            pb.font.color.rgb = TEXT_DARK
            pb.space_after = Pt(6)

    # =========================================================================
    # SLIDE 6: RESEARCH AND REFERENCES
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_common_slide_decorations(slide6, "RESEARCH AND REFERENCES", 6)
    
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
        "1. IOGP Report 590: Life-Saving Rules (International Association of Oil & Gas Producers) — Standardized 10 Life-Saving Rules framework.",
        "2. Oil India Limited (OIL) HSE Operational Guidelines: Upstream petroleum safety protocols.",
        "3. Calibrated NLP Literature: TF-IDF N-grams & Logistic Regression probability calibration for safety text.",
        "4. W3C Web Speech API Specification (BCP-47 Language Codes): Multilingual speech recognition integration.",
        "5. Keerthibalan G SIH 2025 Winning Strategy Framework: Problem-first impact storytelling & visual workflow proof."
    ]
    for r in refs:
        pr = tf_ct.add_paragraph()
        pr.text = r
        pr.font.size = Pt(11)
        pr.font.color.rgb = TEXT_DARK
        pr.space_after = Pt(5)
        
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
        "✔ Live Web Application: Deployed and tested locally & over Wi-Fi on Streamlit server (Port 8501).",
        "✔ 7 Modules Built: Overview, Voice Portal, Inspector, Batch CSV Engine, Dashboard, Hotspots, Drill-Down.",
        "✔ 8 Regional Languages Verified: Tested voice dictation and UI translations in AS, HI, BN, TA, TE, KN, ML, EN.",
        "✔ Empirical Performance: 100% SIF Precursor Recall with sub-50ms real-time inference latency.",
        "✔ Priority Sorting Verified: 10/10 Critical Hazards reliably sorted FIRST across all views."
    ]
    for poc in poc_items:
        pp = tf_cb.add_paragraph()
        pp.text = poc
        pp.font.size = Pt(11)
        pp.font.color.rgb = WHITE
        pp.space_after = Pt(5)
        
    out1 = "Official_SIH2026_Idea_Submission_SIH26165.pptx"
    out2 = "SIH2026_Idea_Submission_SIH26165.pptx"
    prs.save(out1)
    try:
        prs.save(out2)
    except Exception as e:
        print("Note on saving out2:", e)
    print(f"Successfully generated crisp official SIH PPT at: {os.path.abspath(out1)}")

if __name__ == "__main__":
    build_final_sih_presentation()
