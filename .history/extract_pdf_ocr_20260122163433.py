import pdfplumber
from PIL import Image
import pytesseract
import io

pdf_path = r"E:\Imran Projects\QIntellect Projects\TB\PDF Data\Training Module Para Medical 2024.pdf"
output_path = r"E:\Imran Projects\QIntellect Projects\TB\extracted_content.txt"

print("Starting OCR extraction... This may take a while.")

with pdfplumber.open(pdf_path) as pdf:
    full_text = ""
    
    for page_num, page in enumerate(pdf.pages, 1):
        print(f"Processing page {page_num}/{len(pdf.pages)}...")
        
        # Convert page to image
        img = page.to_image(resolution=300)
        pil_img = img.original
        
        # Perform OCR
        try:
            text = pytesseract.image_to_string(pil_img, lang='eng')
            if text and text.strip():
                full_text += f"\n\n{'='*80}\n"
                full_text += f"PAGE {page_num}\n"
                full_text += f"{'='*80}\n\n"
                full_text += text
        except Exception as e:
            print(f"Error on page {page_num}: {e}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)

print(f"\nOCR extraction complete!")
print(f"Total pages: {len(pdf.pages)}")
print(f"Total characters extracted: {len(full_text)}")
print(f"Content saved to: {output_path}")
