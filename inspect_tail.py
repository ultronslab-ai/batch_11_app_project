import docx

doc = docx.Document(r'C:\Users\srigo\Downloads\SafePulse_AI_APP_Project_Report_Final.docx')
body = doc.element.body
print('Total body elements:', len(body))
for idx in range(180, len(body)):
    el = body[idx]
    txt = el.xpath('string()').strip().replace('\n', ' ')
    print(f'[{idx:3d}] {txt[:80]}')
