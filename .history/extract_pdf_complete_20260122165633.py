import fitz  # PyMuPDF
import sys
import os

pdf_path = r"E:\Imran Projects\QIntellect Projects\TB\PDF Data\Training Module Para Medical 2024.pdf"
output_path = r"E:\Imran Projects\QIntellect Projects\TB\extracted_content.txt"

print("="*80)
print("PDF CONTENT EXTRACTION - Training Module Para Medical 2024")
print("="*80)

try:
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"\nTotal pages in PDF: {total_pages}")
    print("Starting extraction...\n")
    
    full_text = ""
    pages_with_text = 0
    pages_without_text = 0
    
    for page_num in range(total_pages):
        page = doc[page_num]
        print(f"Processing page {page_num + 1}/{total_pages}...", end=" ")
        
        # Extract text
        text = page.get_text("text")
        
        if text and text.strip() and len(text.strip()) > 50:
            pages_with_text += 1
            print(f"✓ ({len(text)} chars)")
            full_text += f"\n\n{'='*80}\n"
            full_text += f"PAGE {page_num + 1}\n"
            full_text += f"{'='*80}\n\n"
            full_text += text
        else:
            pages_without_text += 1
            print("✗ (no text/image-based)")
            
            # Try to extract with layout preservation
            text_blocks = page.get_text("blocks")
            if text_blocks:
                for block in text_blocks:
                    if len(block) >= 5 and isinstance(block[4], str):
                        full_text += block[4] + "\n"
    
    doc.close()
    
    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    # Summary
    print("\n" + "="*80)
    print("EXTRACTION SUMMARY")
    print("="*80)
    print(f"Total pages: {total_pages}")
    print(f"Pages with text: {pages_with_text}")
    print(f"Pages without text (images): {pages_without_text}")
    print(f"Total characters extracted: {len(full_text):,}")
    print(f"Output file: {output_path}")
    print(f"File size: {os.path.getsize(output_path):,} bytes")
    print("="*80)
    
    if len(full_text) > 0:
        print("\n✓ SUCCESS! Content extracted.")
        print("\nFirst 500 characters preview:")
        print("-"*80)
        print(full_text[:500])
        print("-"*80)
    else:
        print("\n✗ WARNING: PDF appears to be image-based (scanned document)")
        print("   OCR (Optical Character Recognition) is required.")
        print("   Install Tesseract OCR to extract text from images.")
        
except Exception as e:
    print(f"\n✗ ERROR: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    raise
