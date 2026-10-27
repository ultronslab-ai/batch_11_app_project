import os
import subprocess

def convert_pptx_to_pdf(pptx_path, pdf_path):
    abs_pptx = os.path.abspath(pptx_path)
    abs_pdf = os.path.abspath(pdf_path)
    
    ps_script = f"""
    $pptxPath = '{abs_pptx}'
    $pdfPath = '{abs_pdf}'
    $ppt = New-Object -ComObject PowerPoint.Application
    $pres = $ppt.Presentations.Open($pptxPath, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
    $pres.SaveAs($pdfPath, 32) # 32 = ppSaveAsPDF
    $pres.Close()
    $ppt.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
    """
    
    ps_file = "convert_script.ps1"
    with open(ps_file, "w", encoding="utf-8") as f:
        f.write(ps_script)
        
    cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(ps_file):
        os.remove(ps_file)
        
    if os.path.exists(abs_pdf):
        print(f"Successfully converted to PDF at: {abs_pdf}")
    else:
        print("PowerPoint PDF export output:", res.stdout, res.stderr)

if __name__ == "__main__":
    convert_pptx_to_pdf("Official_SIH2026_Idea_Submission_SIH26165.pptx", "Official_SIH2026_Idea_Submission_SIH26165.pdf")
    convert_pptx_to_pdf("Official_SIH2026_Idea_Submission_SIH26165.pptx", "SIH2026_Idea_Submission_SIH26165.pdf")
