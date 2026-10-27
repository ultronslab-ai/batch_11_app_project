$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open("C:\Users\srigo\Downloads\SafePulse_AI_APP_Project_Report_Final.docx")

Write-Output "=== EXACT HEADINGS AND CAPTIONS ==="
foreach ($p in $doc.Paragraphs) {
    $text = $p.Range.Text.Trim()
    $style = $p.Style.NameLocal
    if (-not $text) { continue }
    
    $isHeading = ($style -eq "Heading 1" -or $style -eq "Heading 2" -or $style -eq "Heading 3" -or $style -eq "Front Heading")
    $isCaption = ($style -eq "Caption" -or $text -like "Table *" -or $text -like "Figure *")
    
    # Ignore the TOC entries themselves
    if ($text -like "*`t*") { continue }
    
    if ($isHeading -or $isCaption) {
        $secNum = $p.Range.Information(2)
        $secPage = $p.Range.Information(1)
        $absPage = $p.Range.Information(3)
        Write-Output "Sec $secNum | Page $secPage (Abs $absPage) | [$style] $text"
    }
}

$doc.Close($false)
$word.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
