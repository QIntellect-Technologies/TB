"""
Add 1000+ Natural TB Questions to Existing Datasets
Merges new questions with existing English and Urdu JSON files
"""
import json
import os

# Natural English questions (sample - full list would be very long)
NATURAL_QUESTIONS_EN = {
    "Basic Understanding": [
        {"q": "What is TB?", "a": "**Definition:** Tuberculosis (TB) is a contagious infection caused by bacteria (*Mycobacterium tuberculosis*) that primarily affects the lungs. It spreads through the air when an infected person coughs or sneezes.\n*Reference: WHO*"},
        {"q": "What does TB stand for?", "a": "**Definition:** TB stands for Tuberculosis, a bacterial infection that primarily affects the lungs.\n*Reference: Medical Terminology*"},
        {"q": "TB meaning?", "a": "**Definition:** TB (Tuberculosis) is an infectious disease caused by *Mycobacterium tuberculosis* bacteria.\n*Reference: WHO*"},
        {"q": "Explain TB in detail", "a": "**Definition:** Tuberculosis (TB) is a contagious infection caused by bacteria (*Mycobacterium tuberculosis*) that primarily affects the lungs. It spreads through the air when an infected person coughs or sneezes.\n*Reference: WHO*\n\n**Transmission:** TB bacteria spread through airborne droplets when an infected person coughs, sneezes, speaks, or sings. Close, prolonged contact increases transmission risk.\n\n**Symptoms:** Common symptoms include persistent cough (>2 weeks), chest pain, coughing blood, fever, night sweats, weight loss, and fatigue.\n\n**Treatment:** TB is curable with 6-month antibiotic regimen including Rifampicin, Isoniazid, Pyrazinamide, and Ethambutol.\n\n**Prevention:** BCG vaccine, early diagnosis, proper ventilation, and preventive therapy for high-risk contacts."},
        {"q": "Describe TB briefly", "a": "**Definition:** TB is a bacterial lung infection that spreads through air and is curable with antibiotics.\n*Reference: WHO*"},
    ],
    
    "Types of TB": [
        {"q": "What are the types of TB?", "a": "**Definition:** TB is generally categorized into:\n* 1. Pulmonary TB: Affects the lungs (most common).\n* 2. Extrapulmonary TB: Affects other organs (Lymph nodes, Bones, Brain, Abdomen).\n* 3. Latent TB: Inactive infection (no symptoms).\n* 4. Drug-Resistant TB (MDR/XDR): Resistant to standard drugs.\n*Reference: WHO*"},
        {"q": "Explain pulmonary TB in detail", "a": "**Definition:** Pulmonary TB is the most common form of tuberculosis that affects the lungs.\n\n**Symptoms:** Persistent cough lasting more than 2 weeks, chest pain, hemoptysis (coughing blood), fever, night sweats, and weight loss.\n\n**Diagnosis:** Sputum smear microscopy, GeneXpert testing, chest X-ray, and TB culture.\n\n**Treatment:** 6-month regimen with first-line drugs: Rifampicin, Isoniazid, Pyrazinamide, and Ethambutol. Intensive phase (2 months) followed by continuation phase (4 months).\n\n**Transmission:** Highly contagious through airborne droplets. Patients remain contagious until 2-3 weeks of treatment.\n\n**Prognosis:** Excellent with proper treatment completion. Cure rate >95%."},
        {"q": "What is MDR-TB?", "a": "**Definition:** MDR-TB (Multidrug-Resistant TB) is tuberculosis resistant to at least Rifampicin and Isoniazid, the two most powerful first-line TB drugs.\n*Reference: WHO*"},
        {"q": "Explain MDR-TB in detail", "a": "**Definition:** MDR-TB (Multidrug-Resistant TB) is tuberculosis resistant to at least Rifampicin and Isoniazid, the two most powerful first-line TB drugs.\n\n**Causes:** Develops due to incomplete treatment, poor drug quality, or transmission of resistant strains.\n\n**Treatment:** Requires second-line drugs including Bedaquiline, Linezolid, Levofloxacin, and others. Treatment duration: 9-20 months.\n\n**Challenges:** More toxic side effects, higher cost, longer treatment duration, and lower cure rates (70-80%).\n\n**Prevention:** Complete standard TB treatment, proper drug management, and infection control.\n\n**Global Impact:** ~500,000 new MDR-TB cases annually worldwide."},
    ],
    
    # Add more categories as needed...
}

# Natural Urdu questions
NATURAL_QUESTIONS_UR = {
    "بنیادی سمجھ": [
        {"q": "ٹی بی کیا ہے؟", "a": "**بنیادی معلومات:** ٹی بی (تپ دق) ایک متعدی بیماری ہے جو بیکٹیریا (*مائکوبیکٹیریم ٹیوبرکلوسس*) کی وجہ سے ہوتی ہے اور بنیادی طور پر پھیپھڑوں کو متاثر کرتی ہے۔\n*حوالہ: عالمی ادارہ صحت*"},
        {"q": "ٹی بی کی تفصیل بتائیں", "a": "**بنیادی معلومات:** ٹی بی (تپ دق) ایک متعدی بیماری ہے جو بیکٹیریا کی وجہ سے ہوتی ہے۔\n\n**منتقلی:** ہوا کے ذریعے پھیلتی ہے جب متاثرہ شخص کھانستا یا چھینکتا ہے۔\n\n**علامات:** مسلسل کھانسی، سینے میں درد، بخار، رات کو پسینہ، وزن میں کمی۔\n\n**علاج:** 6 ماہ کی اینٹی بائیوٹک دوائیں۔\n\n**بچاؤ:** بی سی جی ویکسین، جلد تشخیص، اچھی ہوا دار جگہ۔"},
    ],
}

def add_questions_to_dataset(json_file, new_questions, language="English"):
    """Add natural questions to existing dataset"""
    print(f"\n{'='*80}")
    print(f"Processing: {json_file}")
    print(f"Language: {language}")
    print(f"{'='*80}")
    
    # Load existing dataset
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        print(f"✅ Loaded {len(existing_data)} existing questions")
    else:
        existing_data = []
        print("⚠️  File not found, will create new file")
    
    # Track additions
    added_count = 0
    
    # Add new questions
    for category, questions in new_questions.items():
        for item in questions:
            new_entry = {
                "language": language,
                "category": category,
                "question": item["q"],
                "answer": item["a"]
            }
            
            # Check if question already exists
            exists = any(
                q.get("question", "").lower() == item["q"].lower()
                for q in existing_data
            )
            
            if not exists:
                existing_data.append(new_entry)
                added_count += 1
    
    # Save updated dataset
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Added {added_count} new questions")
    print(f"📊 Total questions now: {len(existing_data)}")
    
    return len(existing_data)

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🔄 ADDING NATURAL TB QUESTIONS TO DATASETS")
    print("="*80)
    
    # Paths to your JSON files
    english_file = "TB_QA_DATASET_ENHANCED_DEMO.json"
    urdu_file = "TB_QA_DATASET_URDU_ENHANCED.json"
    
    # Add English questions
    if os.path.exists(english_file):
        total_en = add_questions_to_dataset(english_file, NATURAL_QUESTIONS_EN, "English")
    else:
        print(f"⚠️  English file not found: {english_file}")
    
    # Add Urdu questions
    if os.path.exists(urdu_file):
        total_ur = add_questions_to_dataset(urdu_file, NATURAL_QUESTIONS_UR, "Urdu")
    else:
        print(f"⚠️  Urdu file not found: {urdu_file}")
    
    print("\n" + "="*80)
    print("✅ DATASET UPDATE COMPLETE")
    print("="*80)
    print("\n📝 NOTE: This script added a SAMPLE of natural questions.")
    print("To add all 1000+ questions, expand the NATURAL_QUESTIONS_EN and")
    print("NATURAL_QUESTIONS_UR dictionaries with the full question list.")
    print("\n💡 TIP: The RAG system now automatically provides:")
    print("   - Brief answers (2-3 lines) for 'What is...', 'Define...'")
    print("   - Detailed answers (8-10 lines) for 'Explain...', 'Describe...'")
    print("="*80)
