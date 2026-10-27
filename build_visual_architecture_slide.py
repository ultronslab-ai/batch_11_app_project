import sys
import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_custom_technical_approach_slide(output_pptx="SIH26165_Technical_Approach_Slide.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Theme Colors
    SIH_NAVY = RGBColor(15, 63, 122)        # #0f3f7a Header Blue
    SIH_BLUE = RGBColor(0, 116, 200)       # Accent Blue
    CARD_BG = RGBColor(240, 249, 255)       # Light Ice Blue
    DASH_BLUE = RGBColor(2, 132, 199)      # Border Blue
    DARK_TEXT = RGBColor(30, 41, 59)
    RED_ACCENT = RGBColor(220, 38, 38)
    GREEN_ACCENT = RGBColor(22, 163, 74)
    GOLD_ACCENT = RGBColor(217, 119, 6)
    WHITE = RGBColor(255, 255, 255)
    
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    # -------------------------------------------------------------------------
    # 1. HEADER BAR
    # -------------------------------------------------------------------------
    # Top Left Team Badge / Logo text
    team_box = slide.shapes.add_textbox(Inches(0.4), Inches(0.15), Inches(2.2), Inches(0.6))
    tf_team = team_box.text_frame
    p_team = tf_team.paragraphs[0]
    p_team.text = "🛡️ Mindsmiths"
    p_team.font.size = Pt(16)
    p_team.font.bold = True
    p_team.font.color.rgb = SIH_NAVY
    
    # Center Title: TECHNICAL APPROACH
    title_box = slide.shapes.add_textbox(Inches(2.8), Inches(0.15), Inches(7.7), Inches(0.7))
    tf_t = title_box.text_frame
    p_t = tf_t.paragraphs[0]
    p_t.text = "TECHNICAL APPROACH"
    p_t.alignment = PP_ALIGN.CENTER
    p_t.font.size = Pt(30)
    p_t.font.bold = True
    p_t.font.color.rgb = SIH_NAVY
    
    # Top Right SIH Logo if extracted
    logo_path = os.path.abspath("template_assets/extracted_img_p1_1.png")
    if os.path.exists(logo_path):
        slide.shapes.add_picture(logo_path, Inches(11.2), Inches(0.1), width=Inches(1.8))
        
    # Dashed separator line under header
    sep_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.85), Inches(12.533), Inches(0.02))
    sep_line.fill.solid()
    sep_line.fill.fore_color.rgb = RGBColor(148, 163, 184)
    sep_line.line.fill.background()

    # -------------------------------------------------------------------------
    # 2. HELPER TO CREATE DASHED ROUNDED CONTAINER BOXES
    # -------------------------------------------------------------------------
    def add_dashed_card(left, top, width, height, title, items, title_color=SIH_NAVY, border_color=DASH_BLUE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(2)
        card.line.dash_style = pptx.enum.dml.MSO_LINE.DASH
        
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP
        
        # Title
        p_hdr = tf.paragraphs[0]
        p_hdr.text = title
        p_hdr.alignment = PP_ALIGN.CENTER
        p_hdr.font.size = Pt(11)
        p_hdr.font.bold = True
        p_hdr.font.color.rgb = title_color
        p_hdr.space_after = Pt(6)
        
        for item in items:
            p_i = tf.add_paragraph()
            p_i.text = item
            p_i.font.size = Pt(9.5)
            p_i.font.color.rgb = DARK_TEXT
            p_i.space_after = Pt(4)
        return card

    # -------------------------------------------------------------------------
    # 3. LEFT INPUT SENSORS / DATA SOURCES (3 DASHED BOXES)
    # -------------------------------------------------------------------------
    # Top Left: Multilingual Voice Input
    add_dashed_card(
        Inches(0.4), Inches(1.1), Inches(3.0), Inches(1.7),
        "🎙️ Multilingual Voice Input",
        [
            "• Native Web Speech API Engine",
            "• 8 Languages (AS, HI, BN, TA, TE, KN, ML, EN)",
            "• Live JS Auto-Typing Bridge"
        ]
    )
    
    # Middle Left: Mobile Worker Portal
    add_dashed_card(
        Inches(0.4), Inches(3.0), Inches(3.0), Inches(1.7),
        "📱 Mobile Worker Portal",
        [
            "• Field Operator Incident Log",
            "• Regional Phonetic Normalizer",
            "• <30s Rapid Mobile Submission"
        ]
    )

    # Bottom Left: Batch CSV Ingestion
    add_dashed_card(
        Inches(0.4), Inches(4.9), Inches(3.0), Inches(1.7),
        "📁 Batch CSV Ingestion",
        [
            "• OIL Enterprise Incident Logs",
            "• Digboi, Duliajan, Moran, Numaligarh",
            "• Automated Text Preprocessing"
        ]
    )

    # -------------------------------------------------------------------------
    # 4. CENTRAL PROCESSOR HUB (HARDWARE BOARD CONTAINER)
    # -------------------------------------------------------------------------
    core_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.7), Inches(1.8), Inches(4.3), Inches(4.8))
    core_box.fill.solid()
    core_box.fill.fore_color.rgb = WHITE
    core_box.line.color.rgb = SIH_NAVY
    core_box.line.width = Pt(2.5)
    
    # Board Title Banner
    board_hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(3.7), Inches(1.8), Inches(4.3), Inches(0.55))
    board_hdr.fill.solid()
    board_hdr.fill.fore_color.rgb = SIH_NAVY
    board_hdr.line.fill.background()
    tf_bh = board_hdr.text_frame
    tf_bh.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_bh = tf_bh.paragraphs[0]
    p_bh.text = "🧠 Runs Core AI/NLP Models"
    p_bh.alignment = PP_ALIGN.CENTER
    p_bh.font.size = Pt(13)
    p_bh.font.bold = True
    p_bh.font.color.rgb = WHITE

    # Sub-Model 1: SIF Classifier
    m1 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.85), Inches(2.5), Inches(4.0), Inches(1.2))
    m1.fill.solid()
    m1.fill.fore_color.rgb = RGBColor(239, 246, 255)
    m1.line.color.rgb = SIH_BLUE
    tf_m1 = m1.text_frame
    tf_m1.word_wrap = True
    p_m1 = tf_m1.paragraphs[0]
    p_m1.text = "⚡ SIF Classifier Model"
    p_m1.font.size = Pt(11)
    p_m1.font.bold = True
    p_m1.font.color.rgb = SIH_NAVY
    p_m1_b = tf_m1.add_paragraph()
    p_m1_b.text = "• TF-IDF N-gram + Calibrated LogReg\n• SIF Probability % & 1-10 Risk Score"
    p_m1_b.font.size = Pt(9)
    p_m1_b.font.color.rgb = DARK_TEXT

    # Sub-Model 2: IOGP 10 Rules
    m2 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.85), Inches(3.8), Inches(4.0), Inches(1.2))
    m2.fill.solid()
    m2.fill.fore_color.rgb = RGBColor(240, 253, 244)
    m2.line.color.rgb = GREEN_ACCENT
    tf_m2 = m2.text_frame
    tf_m2.word_wrap = True
    p_m2 = tf_m2.paragraphs[0]
    p_m2.text = "🛡️ IOGP 10 Rules Assessment Model"
    p_m2.font.size = Pt(11)
    p_m2.font.bold = True
    p_m2.font.color.rgb = GREEN_ACCENT
    p_m2_b = tf_m2.add_paragraph()
    p_m2_b.text = "• Multi-label NLP Pattern Parser\n• Energy Isolation, Hot Work, Line of Fire..."
    p_m2_b.font.size = Pt(9)
    p_m2_b.font.color.rgb = DARK_TEXT

    # Sub-Model 3: LIME & Barrier Analysis
    m3 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.85), Inches(5.1), Inches(4.0), Inches(1.2))
    m3.fill.solid()
    m3.fill.fore_color.rgb = RGBColor(254, 243, 199)
    m3.line.color.rgb = GOLD_ACCENT
    tf_m3 = m3.text_frame
    tf_m3.word_wrap = True
    p_m3 = tf_m3.paragraphs[0]
    p_m3.text = "📍 Barrier Failure & LIME Attribution"
    p_m3.font.size = Pt(11)
    p_m3.font.bold = True
    p_m3.font.color.rgb = GOLD_ACCENT
    p_m3_b = tf_m3.add_paragraph()
    p_m3_b.text = "• Equipment barrier breakdown extractor\n• LIME precursor word highlights for HSE"
    p_m3_b.font.size = Pt(9)
    p_m3_b.font.color.rgb = DARK_TEXT

    # -------------------------------------------------------------------------
    # 5. TOP TRANSMISSION & POWER UNIT
    # -------------------------------------------------------------------------
    top_unit = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.3), Inches(1.0), Inches(3.1), Inches(0.65))
    top_unit.fill.solid()
    top_unit.fill.fore_color.rgb = CARD_BG
    top_unit.line.color.rgb = DASH_BLUE
    top_unit.line.dash_style = pptx.enum.dml.MSO_LINE.DASH
    tf_tu = top_unit.text_frame
    tf_tu.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_tu = tf_tu.paragraphs[0]
    p_tu.text = "☀️ Local Edge Server & API Bridge 📡"
    p_tu.alignment = PP_ALIGN.CENTER
    p_tu.font.size = Pt(10)
    p_tu.font.bold = True
    p_tu.font.color.rgb = SIH_NAVY

    # -------------------------------------------------------------------------
    # 6. RIGHT OUTPUT ACTUATORS (3 DASHED BOXES)
    # -------------------------------------------------------------------------
    # Top Right: Priority Hazard Alert Unit
    add_dashed_card(
        Inches(8.3), Inches(1.1), Inches(2.7), Inches(1.7),
        "🚨 Priority Hazard Alert",
        [
            "• 10/10 Critical Risks Sorted FIRST",
            "• 100% SIF Precursor Recall",
            "• Instant HSE Officer Notification"
        ],
        title_color=RED_ACCENT, border_color=RED_ACCENT
    )

    # Middle Right: Risk Density Heatmap Engine
    add_dashed_card(
        Inches(8.3), Inches(3.0), Inches(2.7), Inches(1.7),
        "🗺️ Risk Density Heatmap",
        [
            "• 2D Site vs Activity Risk Matrix",
            "• Operational Risk Hotspots",
            "• Monthly SIF Trend Forecast"
        ],
        title_color=GOLD_ACCENT, border_color=GOLD_ACCENT
    )

    # Bottom Right: Executive HSE Compliance Unit
    add_dashed_card(
        Inches(8.3), Inches(4.9), Inches(2.7), Inches(1.7),
        "📊 HSE Audit Controller",
        [
            "• Interactive Filterable Table",
            "• Exportable CSV Audit Logs",
            "• Dynamic 8-Language Switcher"
        ],
        title_color=SIH_NAVY, border_color=DASH_BLUE
    )

    # -------------------------------------------------------------------------
    # 7. FAR RIGHT MOBILE & DISPLAY UI MOCKUPS
    # -------------------------------------------------------------------------
    # Mobile Phone Frame Mockup
    phone_bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(11.2), Inches(1.1), Inches(1.733), Inches(4.1))
    phone_bg.fill.solid()
    phone_bg.fill.fore_color.rgb = RGBColor(15, 23, 42) # Dark phone casing
    phone_bg.line.fill.background()
    
    # Phone Screen
    screen = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(11.28), Inches(1.25), Inches(1.573), Inches(3.8))
    screen.fill.solid()
    screen.fill.fore_color.rgb = WHITE
    screen.line.fill.background()
    tf_sc = screen.text_frame
    tf_sc.word_wrap = True
    
    p_s1 = tf_sc.paragraphs[0]
    p_s1.text = "📱 OIL Safety Intelligence"
    p_s1.alignment = PP_ALIGN.CENTER
    p_s1.font.size = Pt(8.5)
    p_s1.font.bold = True
    p_s1.font.color.rgb = SIH_NAVY
    p_s1.space_after = Pt(4)
    
    p_s2 = tf_sc.add_paragraph()
    p_s2.text = "Real-Time System Monitoring"
    p_s2.alignment = PP_ALIGN.CENTER
    p_s2.font.size = Pt(7.5)
    p_s2.font.bold = True
    p_s2.font.color.rgb = SIH_BLUE
    p_s2.space_after = Pt(6)
    
    p_s3 = tf_sc.add_paragraph()
    p_s3.text = "🎙️ Voice Status:\nTranscribed & Typed"
    p_s3.font.size = Pt(7)
    p_s3.font.color.rgb = GREEN_ACCENT
    p_s3.space_after = Pt(6)
    
    p_s4 = tf_sc.add_paragraph()
    p_s4.text = "SIF Recall Level:\n100.0% Perfect"
    p_s4.font.size = Pt(7)
    p_s4.font.bold = True
    p_s4.font.color.rgb = DARK_TEXT
    p_s4.space_after = Pt(6)

    p_s5 = tf_sc.add_paragraph()
    p_s5.text = "Active Hazard:\n10/10 CRITICAL"
    p_s5.font.size = Pt(7)
    p_s5.font.bold = True
    p_s5.font.color.rgb = RED_ACCENT

    # Bottom Right LCD Screen Mockup
    lcd = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(11.2), Inches(5.35), Inches(1.733), Inches(1.25))
    lcd.fill.solid()
    lcd.fill.fore_color.rgb = RGBColor(15, 23, 42)
    lcd.line.color.rgb = GREEN_ACCENT
    lcd.line.width = Pt(1.5)
    tf_lcd = lcd.text_frame
    tf_lcd.word_wrap = True
    
    p_l1 = tf_lcd.paragraphs[0]
    p_l1.text = "LATENCY: <50 ms"
    p_l1.font.size = Pt(7.5)
    p_l1.font.bold = True
    p_l1.font.color.rgb = RGBColor(74, 222, 128)
    
    p_l2 = tf_lcd.add_paragraph()
    p_l2.text = "TOTAL LOGS: 1,420"
    p_l2.font.size = Pt(7.5)
    p_l2.font.bold = True
    p_l2.font.color.rgb = WHITE
    
    p_l3 = tf_lcd.add_paragraph()
    p_l3.text = "STATUS: SAFE ENGINE"
    p_l3.font.size = Pt(7.5)
    p_l3.font.bold = True
    p_l3.font.color.rgb = RGBColor(96, 165, 250)

    prs.save(output_pptx)
    print(f"Successfully generated custom technical approach slide at: {os.path.abspath(output_pptx)}")

if __name__ == "__main__":
    build_custom_technical_approach_slide()
