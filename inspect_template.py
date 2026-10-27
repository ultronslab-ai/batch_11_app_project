import pymupdf

pdf_path = r'D:\SIH2026-IDEA-Presentation-Format.pdf'
doc = pymupdf.open(pdf_path)

for idx, page in enumerate(doc):
    print(f"=== PAGE {idx+1} ===")
    blocks = page.get_text('dict')['blocks']
    for b in blocks:
        if 'lines' in b:
            for line in b['lines']:
                for span in line['spans']:
                    bbox = [round(x,1) for x in span['bbox']]
                    print(f"  BBox: {bbox} | Size: {span['size']:.1f} | Text: {repr(span['text'])}")
