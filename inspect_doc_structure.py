import docx

doc = docx.Document(r'C:\Users\srigo\Downloads\APP_Project Report Template Final_BACKUP.docx')

print("Total paragraphs:", len(doc.paragraphs))
for i, p in enumerate(doc.paragraphs):
    has_pb = False
    for r in p.runs:
        if 'type="page"' in r._r.xml:
            has_pb = True
    if p.paragraph_format.page_break_before:
        has_pb = True
    if has_pb:
        print(f"Page break before P{i}: {p.text[:40]} [{p.style.name}]")
