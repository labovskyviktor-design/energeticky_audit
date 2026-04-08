"""Extract text from PDF page by page into separate text files."""
from pdfminer.high_level import extract_text
import os

PDF_PATH = r"C:\Users\42191\.gemini\antigravity\scratch\energy-audit\docs\skripta\Krajcik_M._a_kol._-_ENERGETICKE_HODNOTENIE_BUDOV-38-64.pdf"
OUT_DIR = r"C:\Users\42191\.gemini\antigravity\scratch\energy-audit\docs\skripta"

# Extract text from entire PDF first to see total pages
full_text = extract_text(PDF_PATH)
# Split by form feeds (page breaks)
pages = full_text.split('\x0c')
print(f"Total pages (by form feed): {len(pages)}")

for i, page_text in enumerate(pages):
    if page_text.strip():
        filename = os.path.join(OUT_DIR, f"ch3_page_{i+1}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(page_text.strip())
        # Show first 100 chars of each page
        preview = page_text.strip()[:120].replace('\n', ' | ')
        print(f"Page {i+1}: {preview}")
    else:
        print(f"Page {i+1}: (empty)")
