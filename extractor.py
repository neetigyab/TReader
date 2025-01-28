import pdfplumber

def extract_pdf_text(pdf_path):
    """Extract all text lines from a PDF."""
    try:
        lines = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                page_lines = text.splitlines()
                lines.extend(page_lines)
        return lines
    except Exception as e:
        return []
    

def check_pdf(lines):
    imad_found = any("IMAD:" in line for line in lines)
    omad_found = any("OMAD:" in line for line in lines)
    return imad_found and omad_found