import win32com.client as win32
import os
import json

doc_path = r"C:\Users\srigo\Downloads\SafePulse_AI_APP_Project_Report_Final.docx"

word = win32.Dispatch("Word.Application")
word.Visible = False

doc = word.Documents.Open(doc_path)

# Let's inspect headings in Section 3 (the chapters)
print("Sections count:", doc.Sections.Count)

results = []
for p in doc.Paragraphs:
    style = p.Style.NameLocal
    text = p.Range.Text.strip()
    if not text:
        continue
    
    # We only care about real headings, table captions, and figure captions
    is_heading = style in ["Heading 1", "Heading 2", "Heading 3", "Front Heading"]
    is_caption = style == "Caption" or text.startswith("Table ") or text.startswith("Figure ")
    
    # Exclude paragraphs that are inside the TOC itself
    if is_heading or is_caption:
        sec_num = p.Range.Information(2) # wdActiveEndSectionNumber
        sec_page = p.Range.Information(1) # wdActiveEndAdjustedPageNumber
        abs_page = p.Range.Information(3) # wdActiveEndPageNumber
        results.append({
            "text": text[:70],
            "style": style,
            "sec": sec_num,
            "page": sec_page,
            "abs_page": abs_page
        })

doc.Close(False)
word.Quit()

for r in results:
    print(f"Sec {r['sec']} | Page {r['page']:2d} (Abs {r['abs_page']:2d}) | [{r['style']}] {r['text']}")
