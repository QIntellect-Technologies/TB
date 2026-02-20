import pdfplumber
import sys

pdf_path = r"E:\Imran Projects\QIntellect Projects\TB\PDF Data\Training Module Para Medical 2024.pdf"
output_path = r"E:\Imran Projects\QIntellect Projects\TB\extracted_content.txt"

try:
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        
        for page_num, page in enumerate(pdf.pages, 1):
            print(f"Processing page {page_num}...", file=sys.stderr)
            text = page.extract_text(x_tolerance=2, y_tolerance=2)
            
            if text and text.strip():
                full_text += f"\n\n{'='*80}\n"
                full_text += f"PAGE {page_num}\n"
                full_text += f"{'='*80}\n\n"
                full_text += text
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
    
    print(f"\nPDF extracted successfully!")
    print(f"Total pages: {len(pdf.pages)}")
    print(f"Total characters extracted: {len(full_text)}")
    print(f"Content saved to: {output_path}")
    
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    raise
