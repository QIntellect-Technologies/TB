"""
Automated OCR Content Cleanup Script
Cleans up extracted PDF content by removing artifacts and improving readability
"""

import re
import os

def clean_ocr_content(input_file, output_file):
    """Clean and improve OCR extracted content"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into pages
    pages = content.split('=' * 80)
    
    cleaned_pages = []
    medical_terms = []
    forms_data = []
    
    for page in pages:
        if not page.strip():
            continue
            
        # Extract page number
        page_num_match = re.search(r'PAGE (\d+)', page)
        page_num = page_num_match.group(1) if page_num_match else 'Unknown'
        
        # Clean the page content
        cleaned = clean_page(page)
        
        # Extract medical terms and important data
        terms = extract_medical_terms(cleaned)
        forms = extract_form_data(cleaned)
        
        if terms:
            medical_terms.extend([(page_num, term) for term in terms])
        if forms:
            forms_data.extend([(page_num, form) for form in forms])
        
        # Only include pages with meaningful content
        if len(cleaned.strip()) > 100 and has_readable_content(cleaned):
            cleaned_pages.append(f"\n{'=' * 80}\nPAGE {page_num}\n{'=' * 80}\n{cleaned}")
    
    # Create comprehensive cleaned output
    output = create_cleaned_output(cleaned_pages, medical_terms, forms_data)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)
    
    return len(cleaned_pages), len(medical_terms), len(forms_data)

def clean_page(text):
    """Clean individual page content"""
    
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove lines with mostly special characters (OCR artifacts)
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Skip lines that are mostly non-alphanumeric
        if len(line.strip()) > 0:
            alpha_ratio = sum(c.isalnum() or c.isspace() for c in line) / len(line)
            if alpha_ratio > 0.3:  # At least 30% readable characters
                cleaned_lines.append(line)
    
    text = '\n'.join(cleaned_lines)
    
    # Clean up common OCR errors
    text = re.sub(r'[°~\*]{2,}', '', text)  # Remove repeated special chars
    text = re.sub(r'\s+', ' ', text)  # Normalize spaces
    text = re.sub(r'^\s*[-_=]{2,}\s*$', '', text, flags=re.MULTILINE)  # Remove separator lines
    
    return text.strip()

def has_readable_content(text):
    """Check if page has meaningful readable content"""
    
    # Check for English words or medical terms
    english_words = re.findall(r'\b[A-Za-z]{3,}\b', text)
    
    # Check for numbers (dosages, dates, etc.)
    numbers = re.findall(r'\d+', text)
    
    # Check for medical terms
    medical_keywords = [
        'TB', 'Tuberculosis', 'Rifampicin', 'Isoniazid', 'Pyrazinamide', 'Ethambutol',
        'DOTS', 'Treatment', 'Patient', 'Diagnosis', 'HRZE', 'HIV', 'NTP',
        'Sputum', 'Microscopy', 'Xpert', 'Culture', 'Regimen'
    ]
    
    has_medical = any(term in text for term in medical_keywords)
    
    return len(english_words) > 5 or len(numbers) > 3 or has_medical

def extract_medical_terms(text):
    """Extract important medical terms and dosages"""
    
    terms = []
    
    # Extract drug names with dosages
    drug_patterns = [
        r'(Rifampicin|Isoniazid|Pyrazinamide|Ethambutol)\s*[\(\[]?\s*(\d+)\s*mg',
        r'HRZE\s*[\(\[]?\s*(\d+/\d+/\d+/\d+)',
        r'HR\s*[\(\[]?\s*(\d+/\d+)',
    ]
    
    for pattern in drug_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        terms.extend(matches)
    
    # Extract treatment regimens
    regimen_pattern = r'Regimen[-\s]*\d+[:\s]*([^\n]+)'
    regimens = re.findall(regimen_pattern, text, re.IGNORECASE)
    terms.extend([('Regimen', r) for r in regimens])
    
    # Extract weight bands
    weight_pattern = r'(\d+)\s*[-–]\s*(\d+)\s*kg'
    weights = re.findall(weight_pattern, text)
    terms.extend([('Weight band', f'{w[0]}-{w[1]}kg') for w in weights])
    
    return terms

def extract_form_data(text):
    """Extract TB form information (TB01, TB02, etc.)"""
    
    forms = []
    
    # Extract form references
    form_patterns = [
        r'(TB\s*0[1-9])[:\s]*([^\n]{0,100})',
        r'(Treatment\s+Card|Patient\s+Card|Laboratory\s+Request)[:\s]*([^\n]{0,100})',
    ]
    
    for pattern in form_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        forms.extend(matches)
    
    return forms

def create_cleaned_output(pages, medical_terms, forms_data):
    """Create structured output with extracted information"""
    
    output = """# TB TRAINING MODULE - CLEANED CONTENT
# Extracted from: Training Module Para Medical 2024.pdf
# Extraction Date: January 22, 2026
# Total Pages Processed: {}

{}

# EXTRACTED MEDICAL TERMS AND DOSAGES

{}

# IDENTIFIED FORMS

{}

# FULL PAGE CONTENT

{}
""".format(
        len(pages),
        '=' * 80,
        format_medical_terms(medical_terms),
        format_forms(forms_data),
        '\n'.join(pages)
    )
    
    return output

def format_medical_terms(terms):
    """Format medical terms for output"""
    
    if not terms:
        return "No medical terms extracted."
    
    output = []
    seen = set()
    
    for page, term in terms:
        term_str = str(term)
        if term_str not in seen:
            output.append(f"Page {page}: {term_str}")
            seen.add(term_str)
    
    return '\n'.join(output[:100])  # Limit to first 100 unique terms

def format_forms(forms):
    """Format form data for output"""
    
    if not forms:
        return "No forms identified."
    
    output = []
    seen = set()
    
    for page, form_info in forms:
        form_str = str(form_info)
        if form_str not in seen:
            output.append(f"Page {page}: {form_str}")
            seen.add(form_str)
    
    return '\n'.join(output[:50])  # Limit to first 50 unique forms

if __name__ == "__main__":
    input_file = "extracted_content.txt"
    output_file = "extracted_content_cleaned.txt"
    
    print("Starting automated cleanup of OCR content...")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print()
    
    try:
        pages, terms, forms = clean_ocr_content(input_file, output_file)
        
        print(f"✅ Cleanup completed successfully!")
        print(f"   - Pages with readable content: {pages}")
        print(f"   - Medical terms extracted: {terms}")
        print(f"   - Forms identified: {forms}")
        print(f"   - Output saved to: {output_file}")
        print()
        
        # Get file sizes
        input_size = os.path.getsize(input_file)
        output_size = os.path.getsize(output_file)
        
        print(f"File sizes:")
        print(f"   - Original: {input_size:,} bytes")
        print(f"   - Cleaned: {output_size:,} bytes")
        print(f"   - Reduction: {((input_size - output_size) / input_size * 100):.1f}%")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        import traceback
        traceback.print_exc()
