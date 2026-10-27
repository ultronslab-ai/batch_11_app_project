import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement

doc = docx.Document(r'C:\Users\srigo\Downloads\APP_Project Report Template Final_BACKUP.docx')

p_lot = [p for p in doc.paragraphs if p.text == "LIST OF TABLES"][0]._p
p_lof = [p for p in doc.paragraphs if p.text == "LIST OF FIGURES"][0]._p
p_abbr = [p for p in doc.paragraphs if p.text == "ABBREVIATIONS"][0]._p

def add_line_before(target_oxml, title, page_str, bold=False, indent=0):
    p_oxml = OxmlElement('w:p')
    target_oxml.addprevious(p_oxml)
    p = docx.text.paragraph.Paragraph(p_oxml, doc)
    p.paragraph_format.tab_stops.add_tab_stop(Inches(6.25), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if indent > 0:
        p.paragraph_format.left_indent = Inches(indent)
    
    r1 = p.add_run(title)
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(11)
    r1.font.bold = bold
    
    p.add_run("\t")
    
    r2 = p.add_run(page_str)
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(11)
    r2.font.bold = bold
    return p

# Add 2 TOC lines before p_lot
add_line_before(p_lot, "1. INTRODUCTION", "1", bold=True)
add_line_before(p_lot, "    1.1 Background", "1", bold=False)

# Add 1 LOT line before p_lof
add_line_before(p_lof, "Table 1. Test Table", "5", bold=False)

# Add 1 LOF line before p_abbr
add_line_before(p_abbr, "Figure 1. Test Figure", "11", bold=False)

print("--- Paragraphs around TOC/LOT/LOF ---")
for i, p in enumerate(doc.paragraphs):
    if any(k in p.text for k in ["TABLE OF CONTENTS", "INTRODUCTION", "LIST OF TABLES", "Test Table", "LIST OF FIGURES", "Test Figure", "ABBREVIATIONS"]):
        print(f"{i:2d}: {repr(p.text)}")
