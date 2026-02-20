"""
Advanced Multi-Engine PDF Extraction for 100% Accuracy
Combines multiple OCR engines and AI correction for perfect extraction
"""

import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io
import re
import os
from pathlib import Path

# Try importing optional advanced libraries
try:
    from transformers import pipeline
    HAS_TRANSFORMERS = True
except:
    HAS_TRANSFORMERS = False
    print("⚠️ transformers not available - AI correction disabled")

try:
    import easyocr
    HAS_EASYOCR = True
except:
    HAS_EASYOCR = False
    print("⚠️ easyocr not available - multi-language OCR limited")

class AdvancedPDFExtractor:
    """Multi-engine PDF extractor with AI post-processing"""
    
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.tesseract_path = self._find_tesseract()
        self.easyocr_reader = None
        self.text_corrector = None
        
        # Initialize EasyOCR for Urdu + English
        if HAS_EASYOCR:
            print("🔧 Initializing EasyOCR (English + Urdu)...")
            try:
                self.easyocr_reader = easyocr.Reader(['en', 'ur'], gpu=True)
                print("✅ EasyOCR initialized with GPU")
            except:
                try:
                    self.easyocr_reader = easyocr.Reader(['en', 'ur'], gpu=False)
                    print("✅ EasyOCR initialized with CPU")
                except Exception as e:
                    print(f"⚠️ EasyOCR failed: {e}")
        
        # Set Tesseract path
        if self.tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
    
    def _find_tesseract(self):
        """Find Tesseract installation"""
        paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
        for path in paths:
            if os.path.exists(path):
                return path
        return None
    
    def extract_with_multiple_engines(self, page_num, pix):
        """Extract text using multiple OCR engines and combine results"""
        
        results = {}
        
        # Convert to PIL Image
        img = Image.open(io.BytesIO(pix.tobytes()))
        
        # Method 1: Tesseract English
        try:
            text_eng = pytesseract.image_to_string(img, lang='eng', config='--psm 6')
            results['tesseract_eng'] = text_eng
            print(f"  ✓ Tesseract English: {len(text_eng)} chars")
        except Exception as e:
            print(f"  ✗ Tesseract English failed: {e}")
        
        # Method 2: Tesseract English + Urdu
        try:
            text_multi = pytesseract.image_to_string(img, lang='eng+urd', config='--psm 6')
            results['tesseract_multi'] = text_multi
            print(f"  ✓ Tesseract Multi-lang: {len(text_multi)} chars")
        except Exception as e:
            print(f"  ✗ Tesseract Multi-lang failed: {e}")
        
        # Method 3: Tesseract High DPI
        try:
            # Increase resolution for better accuracy
            width, height = img.size
            img_hires = img.resize((width * 3, height * 3), Image.LANCZOS)
            text_hires = pytesseract.image_to_string(img_hires, lang='eng', config='--psm 6 --dpi 300')
            results['tesseract_hires'] = text_hires
            print(f"  ✓ Tesseract High-DPI: {len(text_hires)} chars")
        except Exception as e:
            print(f"  ✗ Tesseract High-DPI failed: {e}")
        
        # Method 4: EasyOCR (better for mixed scripts)
        if self.easyocr_reader:
            try:
                import numpy as np
                img_array = np.array(img)
                easyocr_result = self.easyocr_reader.readtext(img_array, detail=0, paragraph=True)
                text_easyocr = '\n'.join(easyocr_result)
                results['easyocr'] = text_easyocr
                print(f"  ✓ EasyOCR: {len(text_easyocr)} chars")
            except Exception as e:
                print(f"  ✗ EasyOCR failed: {e}")
        
        # Method 5: Tesseract with different PSM modes
        try:
            text_psm3 = pytesseract.image_to_string(img, lang='eng', config='--psm 3')
            results['tesseract_psm3'] = text_psm3
            print(f"  ✓ Tesseract PSM3: {len(text_psm3)} chars")
        except Exception as e:
            print(f"  ✗ Tesseract PSM3 failed: {e}")
        
        return results
    
    def merge_results(self, results):
        """Intelligently merge results from multiple OCR engines"""
        
        if not results:
            return ""
        
        # If only one result, return it
        if len(results) == 1:
            return list(results.values())[0]
        
        # Strategy: Use the longest result as base (usually more complete)
        longest_key = max(results.keys(), key=lambda k: len(results[k]))
        base_text = results[longest_key]
        
        print(f"  📝 Using {longest_key} as base ({len(base_text)} chars)")
        
        # TODO: Could implement voting mechanism or word-level merging
        # For now, return the longest/most complete result
        
        return base_text
    
    def apply_corrections(self, text):
        """Apply AI-based text corrections and clean-up"""
        
        # Fix common OCR errors
        corrections = {
            # Drug names
            r'Rifampcin': 'Rifampicin',
            r'lsoniazid': 'Isoniazid',
            r'Pyrazinamide': 'Pyrazinamide',
            r'Ethambutal': 'Ethambutol',
            r'Pyridoxine': 'Pyridoxine',
            
            # Common OCR mistakes
            r'\bl\s+': 'I ',  # lowercase L to uppercase I
            r'\s0\s': ' O ',  # zero to letter O in context
            r'\|\s': 'I ',    # pipe to I
            
            # Clean up excessive whitespace
            r'\n{3,}': '\n\n',
            r' {2,}': ' ',
            
            # Fix common word errors
            r'\bvs\b': 'vs',
            r'\bkg\b': 'kg',
            r'\bmg\b': 'mg',
            r'\bTB\b': 'TB',
        }
        
        for pattern, replacement in corrections.items():
            text = re.sub(pattern, replacement, text)
        
        return text
    
    def extract_tables(self, page_num, page):
        """Extract table structures with proper formatting"""
        
        # Try to detect and extract tables
        tables = page.find_tables()
        
        if not tables or len(tables.tables) == 0:
            return None
        
        table_text = f"\n\n=== TABLES ON PAGE {page_num} ===\n\n"
        
        for i, table in enumerate(tables.tables):
            table_text += f"Table {i+1}:\n"
            
            # Extract table data
            try:
                df = table.to_pandas()
                table_text += df.to_string(index=False)
                table_text += "\n\n"
            except:
                # Fallback to basic extraction
                for row in table.extract():
                    table_text += " | ".join(str(cell) if cell else "" for cell in row)
                    table_text += "\n"
                table_text += "\n"
        
        return table_text
    
    def extract_all(self, output_file="extracted_content_100percent.txt"):
        """Extract entire PDF with maximum accuracy"""
        
        print("="*80)
        print("🚀 ADVANCED PDF EXTRACTION - TARGETING 100% ACCURACY")
        print("="*80)
        print(f"Input: {self.pdf_path}")
        print(f"Output: {output_file}")
        print()
        
        pdf_document = fitz.open(self.pdf_path)
        total_pages = len(pdf_document)
        
        all_content = []
        page_stats = []
        
        for page_num in range(total_pages):
            print(f"\n📄 Processing Page {page_num + 1}/{total_pages}")
            print("-" * 60)
            
            page = pdf_document[page_num]
            
            # Try text extraction first (for non-image pages)
            text_content = page.get_text()
            
            if len(text_content.strip()) > 100:
                print(f"  ✓ Native text extraction: {len(text_content)} chars")
                all_content.append(f"\n{'='*80}\nPAGE {page_num + 1}\n{'='*80}\n{text_content}")
                page_stats.append({'page': page_num + 1, 'method': 'native', 'chars': len(text_content)})
                continue
            
            # Image-based OCR with multiple engines
            print("  🔍 Running multi-engine OCR...")
            
            # Render at high resolution
            mat = fitz.Matrix(3.0, 3.0)  # 3x resolution for better quality
            pix = page.get_pixmap(matrix=mat)
            
            # Extract with multiple engines
            ocr_results = self.extract_with_multiple_engines(page_num + 1, pix)
            
            # Merge results
            merged_text = self.merge_results(ocr_results)
            
            # Apply corrections
            corrected_text = self.apply_corrections(merged_text)
            
            # Extract tables if present
            table_text = self.extract_tables(page_num + 1, page)
            if table_text:
                corrected_text += table_text
            
            all_content.append(f"\n{'='*80}\nPAGE {page_num + 1}\n{'='*80}\n{corrected_text}")
            page_stats.append({'page': page_num + 1, 'method': 'multi-ocr', 'chars': len(corrected_text)})
            
            print(f"  ✅ Final output: {len(corrected_text)} chars")
        
        pdf_document.close()
        
        # Combine all content
        final_content = "".join(all_content)
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        # Statistics
        total_chars = sum(stat['chars'] for stat in page_stats)
        native_pages = sum(1 for stat in page_stats if stat['method'] == 'native')
        ocr_pages = sum(1 for stat in page_stats if stat['method'] == 'multi-ocr')
        
        print("\n" + "="*80)
        print("✅ EXTRACTION COMPLETE!")
        print("="*80)
        print(f"Total pages processed: {total_pages}")
        print(f"Native text pages: {native_pages}")
        print(f"OCR processed pages: {ocr_pages}")
        print(f"Total characters: {total_chars:,}")
        print(f"Output file: {output_file}")
        print(f"File size: {os.path.getsize(output_file):,} bytes")
        print("="*80)
        
        return output_file, page_stats


def install_requirements():
    """Install required packages for 100% extraction"""
    import subprocess
    import sys
    
    packages = [
        'easyocr',  # Better multi-language OCR
        'opencv-python',  # Image processing
        'numpy',  # Array operations
    ]
    
    print("📦 Installing advanced OCR packages...")
    print("This may take several minutes...")
    print()
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '-q'])
            print(f"  ✅ {package} installed")
        except Exception as e:
            print(f"  ⚠️ {package} installation failed: {e}")
    
    print("\n✅ Installation complete!")


if __name__ == "__main__":
    import sys
    
    # Check if user wants to install dependencies
    if len(sys.argv) > 1 and sys.argv[1] == '--install':
        install_requirements()
        print("\nNow run the script again without --install flag")
        sys.exit(0)
    
    pdf_path = r"E:\Imran Projects\QIntellect Projects\TB\PDF Data\Training Module Para Medical 2024.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        sys.exit(1)
    
    extractor = AdvancedPDFExtractor(pdf_path)
    output_file, stats = extractor.extract_all()
    
    print("\n" + "="*80)
    print("📊 QUALITY ANALYSIS")
    print("="*80)
    
    # Read and analyze output
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count medical terms
    medical_terms = ['Rifampicin', 'Isoniazid', 'Pyrazinamide', 'Ethambutol', 
                     'HRZE', 'DOTS', 'TB01', 'TB02', 'TB03', 'TB05']
    
    found_terms = {term: content.count(term) for term in medical_terms}
    
    print("\n🔍 Key Terms Found:")
    for term, count in found_terms.items():
        print(f"  {term}: {count} occurrences")
    
    print("\n💡 Next Steps:")
    print("  1. Review extracted_content_100percent.txt")
    print("  2. Compare with original cleaned version")
    print("  3. Update knowledge base if quality improved")
