import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io
import sys
import os

# Set Tesseract path (common Windows installation paths)
tesseract_paths = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"C:\Users\mimra\AppData\Local\Programs\Tesseract-OCR\tesseract.exe",
]

for path in tesseract_paths:
    if os.path.exists(path):
        pytesseract.pytesseract.tesseract_cmd = path
        print(f"✓ Found Tesseract at: {path}\n")
        break

pdf_path = r"E:\Imran Projects\QIntellect Projects\TB\PDF Data\Training Module Para Medical 2024.pdf"
output_path = r"E:\Imran Projects\QIntellect Projects\TB\extracted_content.txt"

print("="*80)
print("OCR EXTRACTION - Training Module Para Medical 2024")
print("="*80)
print("This will take several minutes (72 pages)...")
print("="*80 + "\n")

try:
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    full_text = ""
    
    for page_num in range(total_pages):
        print(f"[{page_num + 1}/{total_pages}] Processing page {page_num + 1}...", end=" ", flush=True)
        
        page = doc[page_num]
        
        # Convert page to image at higher resolution for better OCR
        mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better quality
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to PIL Image
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        
        # Perform OCR
        try:
            text = pytesseract.image_to_string(img, lang='eng', config='--psm 6')
            
            if text and text.strip():
                char_count = len(text.strip())
                print(f"✓ ({char_count:,} chars)")
                
                full_text += f"\n\n{'='*80}\n"
                full_text += f"PAGE {page_num + 1}\n"
                full_text += f"{'='*80}\n\n"
                full_text += text
            else:
                print("✗ (no text found)")
                
        except Exception as e:
            print(f"✗ Error: {str(e)[:50]}")
    
    doc.close()
    
    # Save to file
    print(f"\nSaving to file...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    # Summary
    print("\n" + "="*80)
    print("EXTRACTION COMPLETE!")
    print("="*80)
    print(f"Total pages processed: {total_pages}")
    print(f"Total characters extracted: {len(full_text):,}")
    print(f"Output file: {output_path}")
    print(f"File size: {os.path.getsize(output_path):,} bytes")
    print("="*80)
    
    if len(full_text) > 500:
        print("\nFirst 800 characters preview:")
        print("-"*80)
        print(full_text[:800])
        print("-"*80)
        print("\n✓ SUCCESS! PDF content extracted with OCR.")
    else:
        print("\n⚠ WARNING: Very little text extracted. Check if PDF is readable.")
        
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
