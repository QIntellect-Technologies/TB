import pdfplumber

pdf_path = r"E:\Imran Projects\QIntellect Projects\TB\PDF Data\Training Module Para Medical 2024.pdf"
output_path = r"E:\Imran Projects\QIntellect Projects\TB\extracted_content.txt"

with pdfplumber.open(pdf_path) as pdf:
    full_text = ""
    for page_num, page in enumerate(pdf.pages, 1):
        text = page.extract_text()
        if text:
            full_text += f"\n\n--- Page {page_num} ---\n\n"
            full_text += text
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)

print(f"PDF extracted successfully! Total pages: {len(pdf.pages)}")
print(f"Content saved to: {output_path}")
