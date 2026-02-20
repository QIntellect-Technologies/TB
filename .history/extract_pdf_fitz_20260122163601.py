import fitz  # PyMuPDF
import sys

pdf_path = r"E:\Imran Projects\QIntellect Projects\TB\PDF Data\Training Module Para Medical 2024.pdf"
output_path = r"E:\Imran Projects\QIntellect Projects\TB\extracted_content.txt"

print("Extracting PDF with PyMuPDF...")

doc = fitz.open(pdf_path)
full_text = ""

for page_num in range(len(doc)):
    page = doc[page_num]
    print(f"Processing page {page_num + 1}/{len(doc)}...")
    
    text = page.get_text()
    
    if text and text.strip():
        full_text += f"\n\n{'='*80}\n"
        full_text += f"PAGE {page_num + 1}\n"
        full_text += f"{'='*80}\n\n"
        full_text += text

total_pages = len(doc)
doc.close()

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(full_text)

print(f"\nExtraction complete!")
print(f"Total pages: {total_pages}")
print(f"Total characters extracted: {len(full_text)}")
print(f"Content saved to: {output_path}")

# Show first 1000 characters as preview
if full_text:
    print("\n--- PREVIEW (first 1000 chars) ---")
    print(full_text[:1000])
else:
    print("\nWARNING: No text extracted. PDF might be image-based or encrypted.")
