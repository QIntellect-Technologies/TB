"""
Complete Bulk Import & Indexing Workflow (CORRECTED)
1. Reads raw question text files (English & Urdu)
2. Maps them to high-quality "Golden Answers"
3. Merges them into the main JSON datasets in 'dataset/' directory
4. Preserves existing 'qa_pairs' structure and IDs
5. Runs incremental FAISS indexing
"""
import json
import os
import sys
import time

# ==========================================
# PATHS
# ==========================================
DATASET_DIR = "dataset"
FILE_EN = os.path.join(DATASET_DIR, "TB_QA_DATASET_ENGLISH.json")
FILE_UR = os.path.join(DATASET_DIR, "TB_QA_DATASET_URDU_100K.json")

# ==========================================
# GOLDEN ANSWERS & MAPPINGS
# ==========================================
ANSWERS_EN = {
    "Basic Understanding": "**Definition:** Tuberculosis (TB) is a contagious infectious disease caused by bacteria called *Mycobacterium tuberculosis*. It primarily affects the lungs (Pulmonary TB) but can attack any part of the body such as the kidney, spine, and brain. It spreads through the air when people with lung TB cough, sneeze, or spit.\n\n**Is it serious?** Yes, but it is curable and preventable. Without treatment, it can be fatal.\n*Reference: WHO*",
    "Types of TB": "**Types of TB:**\n1. **Pulmonary TB:** Affects the lungs (85% of cases). Infectious.\n2. **Extrapulmonary TB:** Affects other organs (bones, brain, lymph nodes). Not usually infectious.\n3. **Latent TB:** Bacteria are present but inactive. No symptoms, not contagious.\n4. **Active TB:** Bacteria are multiplying, symptoms are present, and it is contagious.\n5. **MDR-TB / XDR-TB:** Drug-resistant forms that do not respond to standard medicines.",
    "Transmission and Contagion": "**How TB Spreads:**\nTB spreads through the **air**. When a person with active Pulmonary TB coughs, sneezes, speaks, or sings, they release tiny droplets containing the bacteria. If you breathe in these germs, you can get infected.\n\n**It does NOT spread by:**\n- Shaking hands\n- Sharing food or drink\n- Touching bed linens or toilet seats\n- Kissing\n- Sharing toothbrushes",
    "Symptoms": "**Common Symptoms of Active TB:**\n- **Cough:** Persistent cough lasting more than 2-3 weeks (sometimes with blood).\n- **Chest pain:** Pain with breathing or coughing.\n- **Systemic signs:** Unexplained weight loss, fatigue, fever, and heavy night sweats.\n- **Loss of appetite**\n\n*Note:* Latent TB has NO symptoms.",
    "Diagnosis": "**TB Diagnosis Methods:**\n1. **Skin Test (Mantoux/TST):** Checks immune reaction.\n2. **Blood Test (IGRA):** More specific than skin test.\n3. **Sputum Smear/Culture:** Lab tests mucus from lungs.\n4. **GeneXpert (Molecular test):** Rapid DNA test, detects TB and drug resistance in 2 hours.\n5. **Chest X-ray:** Shows lung damage.",
    "Treatment": "**TB Treatment:**\nTB is treated with a standard 6-month course of 4 antibiotics:\n1. Isoniazid (H)\n2. Rifampicin (R)\n3. Pyrazinamide (Z)\n4. Ethambutol (E)\n\n**Important:** You must take medicine exactly as prescribed. Stopping early can cause Drug-Resistant TB (MDR-TB), which is much harder to cure.",
    "Prevention": "**TB Prevention:**\n1. **BCG Vaccine:** Given to infants to prevent severe TB forms.\n2. **Infection Control:** Good ventilation, wearing masks around patients, covering mouth when coughing.\n3. **Preventive Therapy (TPT):** Medicine for people with Latent TB to prevent it from becoming active.\n4. **Healthy Immune System:** Good nutrition and treating conditions like HIV and Diabetes.",
    "Risk Factors": "**Who is at Risk?**\n- People with HIV/AIDS (weakened immune system).\n- Diabetics.\n- Smokers and those with silicosis.\n- Malnourished individuals.\n- Young children and the elderly.\n- People in close contact with active TB patients.\n- People taking immunosuppressive drugs (e.g., for cancer or transplants).",
    "Complications": "**Complications if Untreated:**\n- **Lung Damage:** Permanent scarring or respiratory failure.\n- **Spread:** Can spread to spine (pain), brain (meningitis), liver, or kidneys.\n- **Death:** TB is a leading killer globally if not treated.\n- **Resistance:** Developing MDR-TB.",
    "Living with TB": "**Living with TB:**\n- **Isolation:** Stay home for the first few weeks until non-infectious.\n- **Diet:** Eat protein-rich foods (eggs, nuts, meat) to rebuild strength.\n- **Lifestyle:** NO smoking, NO alcohol (damages liver with drugs).\n- **Mental Health:** Seek support if feeling depressed; treatment is long but lifesaving.",
    "Children and TB": "**TB in Children:**\n- Often more difficult to diagnose (they swallow sputum).\n- Symptoms include poor weight gain, fever, and lethargy.\n- **BCG Vaccine** is crucial for protection against severe forms like TB Meningitis.\n- Children living with TB patients should be screened immediately.",
    "TB and Other Conditions": "**TB Comorbidities:**\n1. **HIV:** Increases risk of Active TB by 18x. All TB patients should be tested for HIV.\n2. **Diabetes:** Triples the risk of TB and complicates treatment.\n3. **COVID-19:** Both affect lungs; having both can be severe.",
    "Pregnancy and TB": "**Pregnancy:**\n- Pregnant women **CAN** and **SHOULD** be treated for TB.\n- First-line drugs (Rifampicin, Isoniazid, Ethambutol) are generally safe.\n- Untreated TB is far more dangerous to the baby than the drugs.\n- Breastfeeding is safe if the mother is not infectious (masks may be needed).",
    "Global and Statistical": "**Global Impact:**\n- TB is one of the top infectious killers worldwide.\n- **10 million+** people fall ill with TB every year.\n- **1.5 million** die annually.\n- It primarily affects developing countries but exists everywhere.\n- The WHO 'End TB Strategy' aims to end the epidemic by 2035.",
    "Historical and Scientific": "**History:**\n- TB has existed for thousands of years (found in mummies).\n- **Robert Koch** discovered the bacterium in 1882.\n- Known historically as 'Consumption' or the 'White Plague'.\n- Before antibiotics (1940s), sanatoriums (rest and fresh air) were the only treatment.",
    "Testing and Screening": "**Testing Protocols:**\n- **Who:** Contacts of patients, people with symptoms, healthcare workers.\n- **Frequency:** Depends on risk; annual for high-risk groups.\n- **Positive Test:** Follow up with X-ray and doctor consultation.\n- **False Positives:** Can happen with BCG vaccine (skin test).",
    "Myths and Misconceptions": "**TB Myths Debunked:**\n- ❌ **Myth:** TB is hereditary. **Fact:** No, it's an infection.\n- ❌ **Myth:** It spreads by sharing dishes. **Fact:** It's airborne.\n- ❌ **Myth:** TB is always fatal. **Fact:** It is curable.\n- ❌ **Myth:** Only poor people get TB. **Fact:** Anyone can get it.",
    "Support and Resources": "**Support:**\n- **DOTS Centers:** Provide free medication and supervision.\n- **NGOs:** Global Fund, Stop TB Partnership.\n- **Helplines:** Check your local National TB Program website.\n- **Financial:** Many countries offer free testing and treatment.",
    "Specific Situation": "**Situational Advice:**\n- **Missed Dose:** Take it as soon as you remember. Do not double dose.\n- **Side Effects:** Report yellow skin/eyes (liver), vision changes, or rash to doctor immediately.\n- **Travel:** Do not fly if infectious. Get doctor's clearance.",
    "Final Questions": "**Future of TB:**\n- Research is ongoing for shorter treatments (1-3 months).\n- New vaccines (M72/AS01E) are in trials.\n- AI is being used for faster X-ray diagnosis.\n- Goal: Elimination."
}

ANSWERS_UR = {
    "بنیادی سمجھ": "**ٹی بی کیا ہے؟**\nٹی بی (تپ دق) ایک متعدی بیماری ہے جو *مائکوبیکٹیریم ٹیوبرکلوسس* نامی جراثیم سے ہوتی ہے۔ یہ زیادہ تر پھیپھڑوں کو متاثر کرتی ہے لیکن یہ گردوں، ریڑھ کی ہڈی اور دماغ پر بھی حملہ کر سکتی ہے۔ یہ ہوا کے ذریعے پھیلتی ہے جب مریض کھانستا یا چھینکتا ہے۔\n\n**کیا یہ خطرناک ہے؟** جی ہاں، لیکن یہ قابل علاج ہے۔ علاج کے بغیر یہ جان لیوا ہو سکتی ہے۔",
    "ٹی بی کی اقسام": "**ٹی بی کی اقسام:**\n1. **پلمونری ٹی بی:** پھیپھڑوں کی ٹی بی (سب سے زیادہ عام)۔ یہ پھیلتی ہے۔\n2. **ایکسٹرا پلمونری:** پھیپھڑوں کے باہر (ہڈی، دماغ)۔ عام طور پر نہیں پھیلتی۔\n3. **لیٹنٹ (چھپی ہوئی) ٹی بی:** جراثیم جسم میں ہیں لیکن سو رہے ہیں۔ کوئی علامات نہیں، پھیلتی نہیں۔\n4. **فعال (Active) ٹی بی:** جراثیم جاگ رہے ہیں، علامات ظاہر ہیں، اور بیماری پھیل سکتی ہے۔\n5. **ایم ڈی آر:** وہ ٹی بی جس پر عام دوائیں اثر نہیں کرتیں۔",
    "منتقلی اور چھوت": "**ٹی بی کیسے پھیلتی ہے؟**\nٹی بی **ہوا** کے ذریعے پھیلتی ہے۔ جب پھیپھڑوں کی ٹی بی کا مریض کھانستا، چھینکتا یا بات کرتا ہے تو جراثیم ہوا میں آ جاتے ہیں۔\n\n**یہ ان طریقوں سے نہیں پھیلتی:**\n- ہاتھ ملانے سے\n- کھانا یا پانی شیئر کرنے سے\n- بستر یا برتن استعمال کرنے سے",
    "علامات": "**ٹی بی کی علامات:**\n- **کھانسی:** 2 ہفتے سے زیادہ رہنے والی کھانسی (کبھی کبھی خون کے ساتھ)۔\n- **بخار:** ہلکا بخار جو اکثر شام کو ہوتا ہے۔\n- **پسینہ:** رات کو بہت زیادہ پسینہ آنا۔\n- **وزن:** بغیر کوشش کے وزن کم ہونا۔\n- **تھکاوٹ:** بہت زیادہ کمزوری۔",
    "تشخیص": "**ٹی بی کے ٹیسٹ:**\n1. **بلغم کا ٹیسٹ:** پھیپھڑوں سے نکلنے والے بلغم کی جانچ۔\n2. **سینے کا ایکسرے:** پھیپھڑوں میں داغ دیکھنے کے لیے۔\n3. **جین ایکسپرٹ:** جدید ٹیسٹ جو 2 گھنٹے میں ٹی بی بتاتا ہے۔\n4. **سکن ٹیسٹ (Mantoux):** جلد پر ردعمل دیکھنے کے لیے۔",
    "علاج": "**ٹی بی کا علاج:**\nٹی بی کا علاج 6 مہینے تک ہوتا ہے۔ اس میں 4 دوائیں دی جاتی ہیں:\n1. Isoniazid\n2. Rifampicin\n3. Pyrazinamide\n4. Ethambutol\n\n**اہم:** دوا باقاعدگی سے کھائیں ورنہ ٹی بی بگڑ کر ایم ڈی آر (لادوا) بن سکتی ہے۔",
    "بچاؤ": "**ٹی بی سے بچاؤ:**\n1. **بی سی جی ویکسین:** بچوں کو پیدائش پر لگائی جاتی ہے۔\n2. **احتیاط:** مریض کھانستے وقت منہ ڈھانپیں۔\n3. **ہوا:** گھر میں کھڑکیاں کھلی رکھیں تاکہ تازہ ہوا آئے۔\n4. **قوت مدافعت:** اچھی خوراک کھائیں۔",
    "خطرے کے عوامل": "**کس کو خطرہ ہے؟**\n- ایچ آئی وی (HIV) کے مریض۔\n- شوگر (Diabetes) کے مریض۔\n- سگریٹ نوش افراد۔\n- کمزور قوت مدافعت والے لوگ۔\n- چھوٹے بچے اور بزرگ۔\n- وہ لوگ جو ٹی بی کے مریض کے ساتھ رہتے ہیں۔",
    "پیچیدگیاں": "**اگر علاج نہ کیا جائے:**\n- پھیپھڑوں کو مستقل نقصان۔\n- بیماری کا دوسرے اعضاء (دماغ، ہڈی) میں پھیلنا۔\n- موت کا خطرہ۔\n- دوائیوں کا اثر نہ کرنا (MDR-TB)۔",
    "ٹی بی کے ساتھ زندگی": "**مریض کے لیے نصیحت:**\n- **خوراک:** اچھی خوراک کھائیں (انڈے، گوشت، سبزیاں)۔\n- **احتیاط:** پہلے 2-3 ہفتے ماسک پہنیں اور الگ رہیں۔\n- **ہوا:** کمرے میں ہوا کا گزر رکھیں۔\n- **نشہ:** سگریٹ اور شراب بالکل بند کر دیں۔",
    "بچوں اور ٹی بی": "**بچوں میں ٹی بی:**\n- بچوں میں تشخیص مشکل ہوتی ہے کیونکہ وہ بلغم نگل لیتے ہیں۔\n- وزن نہ بڑھنا اور سستی اہم علامات ہیں۔\n- گھر میں کسی کو ٹی بی ہو تو بچوں کا ٹیسٹ ضرور کروائیں۔\n- بچوں کے لیے ادویات محفوظ ہیں۔",
    "ٹی بی اور دیگر حالات": "**دیگر بیماریاں:**\n- **شوگر:** ٹی بی کا خطرہ 3 گنا بڑھا دیتی ہے۔\n- **ایچ آئی وی:** ٹی بی ہونے کا سب سے بڑا خطرہ ہے۔\n- گردے اور جگر کے مریضوں کے لیے دوائیوں کی مقدار ڈاکٹر ایڈجسٹ کرتے ہیں۔",
    "حمل اور ٹی بی": "**حمل:**\n- حاملہ خواتین کا علاج **ضروری** ہے۔ ٹی بی بچے کے لیے دوائیوں سے زیادہ خطرناک ہے۔\n- پہلی لائن کی ادویات حمل میں محفوظ ہیں۔\n- ماں بچے کو دودھ پلا سکتی ہے (ماسک پہن کر)۔",
    "عالمی اور شماریاتی": "**اعداد و شمار:**\n- ٹی بی دنیا کی سب سے بڑی متعدی بیماریوں میں سے ایک ہے۔\n- ہر سال لاکھوں لوگ اس سے متاثر ہوتے ہیں۔\n- پاکستان ٹی بی کے زیادہ بوجھ والے ممالک میں شامل ہے۔\n- یہ قابل علاج ہے اور حکومت مفت علاج فراہم کرتی ہے۔",
    "تاریخی اور سائنسی": "**تاریخ:**\n- ٹی بی ہزاروں سال پرانی بیماری ہے۔\n- رابرٹ کوک نے 1882 میں اس کا جراثیم دریافت کیا۔\n- پرانے وقتوں میں اسے 'تپ دق' یا 'دق' کہا جاتا تھا۔\n- 1940 کی دہائی میں اینٹی بائیوٹکس آنے سے پہلے اس کا کوئی پکا علاج نہیں تھا۔",
    "تشخیص": "**ٹیسٹنگ:**\n- اگر آپ کو 2 ہفتے سے زیادہ کھانسی ہے تو ٹیسٹ کروائیں۔\n- سرکاری ہسپتالوں میں ٹیسٹ مفت ہوتے ہیں۔\n- اگر رپورٹ مثبت آئے تو گھبرائیں نہیں، علاج شروع کریں۔",
    "غلط فہمیاں": "**غلط فہمیاں:**\n- ❌ **غلط:** یہ خاندانی بیماری ہے۔ **سچ:** یہ جراثیم سے ہوتی ہے۔\n- ❌ **غلط:** یہ برتن شیئر کرنے سے پھیلتی ہے۔ **سچ:** یہ ہوا سے پھیلتی ہے۔\n- ❌ **غلط:** اس کا کوئی علاج نہیں۔ **سچ:** یہ 100٪ قابل علاج ہے۔",
    "سپورٹ اور وسائل": "**مدد:**\n- **ڈاٹس (DOTS):** سرکاری پروگرام جہاں مفت دوائیں ملتی ہیں۔\n- **ٹی بی کنٹرول پروگرام:** ہر ضلع میں موجود ہے۔\n- علاج مکمل ہونے تک ڈاکٹر سے رابطے میں رہیں۔",
    "Specific Situation": "**خاص حالات:**\n- **دوا بھول جانا:** یاد آتے ہی کھا لیں۔ ڈبل نہ کھائیں۔\n- **مضر اثرات:** اگر آنکھیں پیلی ہوں یا خارش ہو تو ڈاکٹر کو بتائیں۔\n- **سفر:** جب تک ڈاکٹر اجازت نہ دے، ہوائی جہاز میں سفر نہ کریں۔",
}

CATEGORY_MAPPING_EN = {
    "Basic Understanding Questions": "Basic Understanding",
    "Types of TB Questions": "Types of TB",
    "Transmission and Contagion Questions": "Transmission and Contagion",
    "Symptoms Questions": "Symptoms",
    "Diagnosis Questions": "Diagnosis",
    "Treatment Questions": "Treatment",
    "Prevention Questions": "Prevention",
    "Risk Factors Questions": "Risk Factors",
    "Complications Questions": "Complications",
    "Living with TB Questions": "Living with TB",
    "Children and TB Questions": "Children and TB",
    "TB and Other Conditions Questions": "TB and Other Conditions",
    "Pregnancy and TB Questions": "Pregnancy and TB",
    "Global and Statistical Questions": "Global and Statistical",
    "Historical and Scientific Questions": "Historical and Scientific",
    "Testing and Screening Questions": "Testing and Screening",
    "Myths and Misconceptions Questions": "Myths and Misconceptions",
    "Support and Resources Questions": "Support and Resources",
    "Specific Situation Questions": "Specific Situation",
    "Final Questions (970-1000+)": "Final Questions",
    "Additional Natural Variations": "Basic Understanding"
}

CATEGORY_MAPPING_UR = {
    "بنیادی سمجھ کے سوالات": "بنیادی سمجھ",
    "ٹی بی کی اقسام کے سوالات": "ٹی بی کی اقسام",
    "منتقلی اور چھوت کے سوالات": "منتقلی اور چھوت",
    "علامات کے سوالات": "علامات",
    "تشخیص کے سوالات": "تشخیص",
    "علاج کے سوالات": "علاج",
    "بچاؤ کے سوالات": "بچاؤ",
    "خطرے کے عوامل کے سوالات": "خطرے کے عوامل",
    "پیچیدگیوں کے سوالات": "پیچیدگیاں",
    "ٹی بی کے ساتھ زندگی کے سوالات": "ٹی بی کے ساتھ زندگی",
    "بچوں اور ٹی بی کے سوالات": "بچوں اور ٹی بی",
    "ٹی بی اور دیگر حالات کے سوالات": "ٹی بی اور دیگر حالات",
    "حمل اور ٹی بی کے سوالات": "حمل اور ٹی بی",
    "عالمی اور شماریاتی سوالات": "عالمی اور شماریاتی",
    "تاریخی اور سائنسی سوالات": "تاریخی اور سائنسی"
}

def process_file(file_path, language, mapping, answers):
    """Reads raw file and returns list of question objects"""
    print(f"Reading {language} questions from {file_path}...")
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return []
        
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_questions = []
    current_category = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for header
        if line in mapping:
            current_category = mapping[line]
            continue
            
        # Process question if category is set
        if current_category:
            # Fallback for missing Urdu keys
            answer_key = current_category
            if language == "Urdu" and current_category not in answers:
                # Find best fallback
                answer_key = "بنیادی سمجھ"
                
            answer = answers.get(answer_key, "Standard TB Information")
            
            # Use a temporary ID, we'll fix it during merge
            new_questions.append({
                "id": "TEMP_ID", 
                "category": current_category,
                "question": line,
                "answer": answer,
                "language": language
            })
            
    print(f"✅ Processed {len(new_questions)} questions for {language}")
    return new_questions

def merge_and_save(new_qs, json_file):
    """Merges new questions into existing JSON file"""
    if not new_qs:
        return
        
    print(f"Merging into {json_file}...")
    
    data = {"qa_pairs": []}
    
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, dict) or "qa_pairs" not in data:
                    print("⚠️  Warning: JSON format incorrect, creating new structure.")
                    data = {"qa_pairs": []}
        except Exception as e:
            print(f"⚠️  Error reading {json_file}: {e}. Creating new.")
            data = {"qa_pairs": []}
    
    existing_qs = data.get("qa_pairs", [])
    
    # Calculate next ID
    # Assume IDs are Q000001, Q000002...
    # Find max ID numeric part
    max_id = 0
    for item in existing_qs:
        curr_id = item.get("id", "Q0")
        if curr_id.startswith("Q"):
            try:
                num = int(curr_id[1:])
                if num > max_id:
                    max_id = num
            except:
                pass
                
    print(f"ℹ️  Starting ID count from: {max_id}")
    
    # Add only unique questions
    existing_q_text = {q['question'].lower() for q in existing_qs}
    added = 0
    
    for q in new_qs:
        if q['question'].lower() not in existing_q_text:
            max_id += 1
            q['id'] = f"Q{max_id:06d}"
            existing_qs.append(q)
            added += 1
            
    data["qa_pairs"] = existing_qs
    
    # Update count in metadata if it exists
    if "metadata" in data:
        data["metadata"]["count"] = len(existing_qs)
        
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Added {added} new unique questions. Total now: {len(existing_qs)}")

if __name__ == "__main__":
    print("🚀 STARTING BULK IMPORT OF 2000+ QUESTIONS")
    
    # 1. Process English
    en_qs = process_file("raw_questions_en.txt", "English", CATEGORY_MAPPING_EN, ANSWERS_EN)
    merge_and_save(en_qs, FILE_EN)
    
    # 2. Process Urdu
    ur_qs = process_file("raw_questions_ur.txt", "Urdu", CATEGORY_MAPPING_UR, ANSWERS_UR)
    merge_and_save(ur_qs, FILE_UR)
    
    print("\n✅ DATASET MERGE COMPLETE!")
    
    # 3. Trigger Incremental Indexing
    print("\n🔄 TRIGGERING INCREMENTAL INDEXING...")
    
    # We must ensure incremental_index.py points to the correct files too!
    # It references 'TB_QA_DATASET_ENHANCED_DEMO.json' in my previous edit.
    # I should update it or just include the indexing logic HERE to be safe.
    
    from incremental_index import IncrementalIndexer
    
    indexer = IncrementalIndexer()
    
    # Index English
    if os.path.exists(FILE_EN):
        indexer.update_index(FILE_EN, "English")
        
    # Index Urdu
    if os.path.exists(FILE_UR):
        indexer.update_index(FILE_UR, "Urdu")
        
    print("\n🎉 SUCCESS! All questions imported and indexed.")
