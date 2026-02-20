import PyPDF2

pdf_path = r"E:\Imran Projects\QIntellect Projects\TB\PDF Data\Training Module Para Medical 2024.pdf"
output_path = r"E:\Imran Projects\QIntellect Projects\TB\extracted_content.txt"

with open(pdf_path, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    full_text = ""
    
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        if text:
            full_text += f"\n\n--- Page {page_num + 1} ---\n\n"
            full_text += text
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)

print(f"PDF extracted successfully! Total pages: {len(pdf_reader.pages)}")
print(f"Content saved to: {output_path}")
print(f"Total characters extracted: {len(full_text)}")
