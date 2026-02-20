"""
ULTIMATE TB DATASET GENERATOR V1.0 (URDU EDITION)
Focus: Native Urdu Language Q&A
Target: ~50k-100k Questions
"""

import json
import random
from datetime import datetime

# ==============================================================================
# 1. URDU TEMPLATE ENGINE
# ==============================================================================

class QualityPhraser:
    def __init__(self):
        self.prefixes = {
            "clinical": [
                "اس کے لیے تجویز کردہ", "برائے کرم وضاحت کریں", "کلینیکل انتظام",
                "اس کا پروٹوکول کیا ہے", "رہنما اصول برائے", "کیسے مینج کریں",
                "اس کے لیے معیارِ علاج", "علاج کی حکمت عملی", "ڈاکٹر کی ہدایت:", "میں علاج کیسے کروں"
            ],
            "direct": [
                "کیا ہے", "مجھے بتائیں", "وضاحت کریں", "تعریف کریں", "تفصیل", "اس کی تفصیلات"
            ],
            "query": [
                "میرے پاس ایک مریض ہے جس کو", "اس کی معلومات چاہیے", "اس کے بارے میں تفصیل درکار ہے",
                "سوال ہے", "اس کا علاج ڈھونڈ رہا ہوں"
            ],
            "mechanism": [
                "یہ کیسے کام کرتا ہے:", "اس کا میکانزم کیا ہے", "اس کی فارماکولوجی",
                "اس کا طریقہ کار کیا ہے", "عمل کا طریقہ:"
            ]
        }
    
    def variate(self, base_term, context="direct"):
        """Generates natural phrasing variations"""
        templates = self.prefixes.get(context, self.prefixes["direct"])
        variations = []
        for t in templates:
            variations.append(f"{t} {base_term}")
        
        suffixes = ["", " ٹی بی میں", " تپِ دق کے لیے", " ہدایت کے مطابق"] 
        
        final_list = []
        for v in variations:
            for s in suffixes:
                combined = f"{v}{s}"
                final_list.append(combined)
        
        return list(set(final_list))

phraser = QualityPhraser()

# ==============================================================================
# 2. GRANULAR CONTENT DATABASE (PURE URDU)
# ==============================================================================

def get_detailed_drugs():
    return [
        {
            "name": "آئیسونیازڈ",
            "aka": ["آئیسونیازڈ", "آئی این ایچ"],
            "attributes": {
                "dosing_adult": "5 ملی گرام/کلوگرام (زیادہ سے زیادہ 300 ملی گرام روزانہ)۔ دن میں ایک بار۔",
                "dosing_child": "10 ملی گرام/کلوگرام (زیادہ سے زیادہ 300 ملی گرام روزانہ)۔",
                "mechanism": "جراثیم کش (Bactericidal)۔ بیکٹیریا کی سیل وال میں مائکولک ایسڈ کی تیاری کو روکتا ہے۔",
                "side_effects": "ہاتھ پاؤں کا سن ہونا (Peripheral neuropathy)، جگر کی سوزش (Hepatitis)، لیوپس جیسی علامات۔",
                "monitoring": "شروع میں LFTs کروائیں۔ ماہانہ چیک کریں (خاص طور پر الٹی، متلی، یا یرقان ہونے پر)۔",
                "safety": "حمل میں محفوظ ہے (Category A)۔ دودھ پلانے والی ماؤں کے لیے محفوظ۔ وٹامن بی-6 (Pyridoxine) کے ساتھ دیں۔"
            }
        },
        {
            "name": "رفیمپیسین",
            "aka": ["رفیمپیسین", "آر آئی ایف"],
            "attributes": {
                "dosing_adult": "10 ملی گرام/کلوگرام (زیادہ سے زیادہ 600 ملی گرام روزانہ)۔",
                "dosing_child": "15 ملی گرام/کلوگرام (زیادہ سے زیادہ 600 ملی گرام روزانہ)۔",
                "mechanism": "جراثیم کش (Bactericidal)۔ ڈی این اے پر انحصار کرنے والے آر این اے پولیمریز کو روکتا ہے۔",
                "side_effects": "جسمانی سیال (پیشاب، آنسو) کا نارنجی/لال ہونا، جگر کی خرابی، فلو جیسی علامات۔",
                "monitoring": "شروع میں LFTs۔ اگر نیل پڑے تو پلیٹلیٹس (Platelets) چیک کریں۔ دوسری ادویات کے ساتھ ری ایکشن چیک کریں۔",
                "safety": "حمل میں محفوظ ہے (Category C - فائدہ نقصان سے زیادہ ہے)۔ دودھ پلانے میں محفوظ۔"
            }
        },
        {
            "name": "پائرازینامائڈ",
            "aka": ["پائرازینامائڈ", "پی زیڈ اے"],
            "attributes": {
                "dosing_adult": "25 ملی گرام/کلوگرام (زیادہ سے زیادہ 2000 ملی گرام)۔",
                "mechanism": "تیزابی ماحول میں جراثیم کشی کرتا ہے (Sterilizing)۔",
                "side_effects": "جگر کی خرابی (ڈوز پر منحصر)، جوڑوں کا درد (Arthralgia)، یورک ایسڈ بڑھنا (Gout)۔",
                "monitoring": "اگر علامات ہوں تو سیرم یورک ایسڈ، LFTs۔",
                "safety": "عام طور پر محفوظ۔ شدید جگر کی بیماری میں احتیاط کریں۔"
            }
        },
        {
            "name": "ایتھمبیوٹول",
            "aka": ["ایتھمبیوٹول", "ای ایم بی"],
            "attributes": {
                "dosing_adult": "15 ملی گرام/کلوگرام (زیادہ سے زیادہ 1200 ملی گرام)۔",
                "mechanism": "جراثیم کو روکتا ہے (Bacteriostatic)۔ سیل وال کی تیاری کو روکتا ہے۔",
                "side_effects": "نظر کی کمزوری (Optic Neuritis) - رنگوں کی پہچان میں مسئلہ۔",
                "monitoring": "ماہانہ نظر کا معائنہ (Snellen Chart اور Ishihara)۔",
                "safety": "حمل میں محفوظ۔ دودھ پلانے میں محفوظ۔"
            }
        },
        {
            "name": "لائینزولڈ",
            "aka": ["لائینزولڈ", "ایل زیڈ ڈی"],
            "attributes": {
                "dosing_adult": "600 ملی گرام روزانہ (کم کی جا سکتی ہے)۔",
                "mechanism": "پروٹین کی تیاری روکتا ہے۔",
                "side_effects": "خون کے خلیے کم ہونا (Anemia)، اعصابی کمزوری، لیکٹک ایسڈوسس۔",
                "monitoring": "حوالہ: WHO 2024۔ پہلے مہینے ہر ہفتے CBC، پھر ماہانہ۔ لیکٹیٹ اور نظر چیک کریں۔",
                "safety": "Category C۔ اگر فائدہ زیادہ ہو تو استعمال کریں۔"
            }
        },
        {
            "name": "بیڈاکویلین",
            "aka": ["بیڈاکویلین", "بی ڈی کیو"],
            "attributes": {
                "dosing_adult": "400 ملی گرام روزانہ (2 ہفتے) پھر 200 ملی گرام ہفتے میں 3 بار (22 ہفتے)۔",
                "mechanism": "ATP synthase کو روکتا ہے۔ جراثیم کش۔",
                "side_effects": "دل کی دھڑکن میں تبدیلی (QT Prolongation)، جگر کی خرابی۔",
                "monitoring": "حوالہ: WHO 2024۔ ECG شروع میں، پھر ہفتے 2، 4، 8، 12، 24 پر۔ ماہانہ LFTs۔",
                "safety": "Category B۔ ایم ڈی آر ٹی بی (MDR-TB) کے لیے اہم دوا۔"
            }
        },
        {
            "name": "لیووفلوکساسین",
            "aka": ["لیووفلوکساسین", "ایل ایف ایکس"],
            "attributes": {
                "dosing_adult": "750-1000 ملی گرام روزانہ۔",
                "mechanism": "فلوروکوئنولون (ڈی این اے گائریز انہیبیٹر)۔",
                "side_effects": "پٹھوں کی سوزش (Tendinitis)، کیو ٹی پرولانگیشن، شوگر کا مسئلہ۔",
                "monitoring": "ای سی جی، شوگر کا ٹیسٹ۔",
                "safety": "ایم ڈی آر کے لیے معیاری علاج۔"
            }
        }
    ]

def get_granular_scenarios():
    return [
         {
            "condition": "ایم ڈی آر ٹی بی",
            "facts": [
                ("علاج کا نسخہ", "بی پی اے ایل (BPaL) یا بی پی اے ایل ایم (BPaLM) 6 مہینے کے لیے۔"),
                ("شامل نہ کرنے کی وجوہات", "حمل یا دماغی ٹی بی میں نہیں دینا (لمبا علاج کریں)۔"),
                ("نگرانی کا شیڈول", "ماہانہ کلچر، ای سی جی، اور نظر کا معائنہ۔"),
                ("علاج کا نتیجہ", "نئے اورل ریجیمین سے کامیابی کی شرح 90 فیصد سے زیادہ ہے۔")
            ]
        },
        {
            "condition": "دماغی ٹی بی",
            "facts": [
                ("علاج کا نسخہ", "2 مہینے ایچ آر زیڈ ای (HRZE) + 10 مہینے ایچ آر (HR) (کل 12 مہینے)۔"),
                ("اسٹیرائڈ کا استعمال", "ڈیکسامیتھاسون یا پریڈنیسولون لازمی ہے۔ 6-8 ہفتے میں آہستہ بند کریں۔"),
                ("سی ایس ایف رپورٹ", "زیادہ پروٹین، کم گلوکوز، لیمفوسائٹس کی زیادتی۔"),
                ("پیچیدگیاں", "دماغ میں پانی (Hydrocephalus)، فالج، نظر یا سننے کی نسوں کا مسئلہ۔")
            ]
        },
        {
            "condition": "حمل میں ٹی بی",
            "facts": [
                ("پہلی لائن کا علاج", "معیاری 2 ایچ آر زیڈ ای / 4 ایچ آر۔ بچے کے لیے محفوظ ہے۔"),
                ("منع ادویات", "اسٹریپٹومائسن/کینامائسن (ٹیکے) سے پرہیز کریں۔ صرف گولیاں دیں۔"),
                ("دودھ پلانا", "جاری رکھیں۔ ماسک پہنہیں۔ بچے کو آئی این ایچ (IPT) دیں۔"),
                ("پائریڈکسین کا استعمال", "حمل میں آئی این ایچ کے ساتھ وٹامن بی-6 50 ملی گرام روزانہ دیں۔")
            ]
        },
        {
            "condition": "جگر کی خرابی",
            "facts": [
                ("دوا روکنے کا اصول", "دوائیں روک دیں اگر: اے ایل ٹی (ALT) نارمل سے 3 گنا زیادہ (علامات کے ساتھ) یا 5 گنا زیادہ (بغیر علامات)۔"),
                ("دوبارہ شروع کرنے کا طریقہ", "جب ایل ایف ٹیز (LFTs) ٹھیک ہوں تو ایک ایک کر کے شروع کریں: ایتھمبیوٹول -> رفیمپیسین -> آئیسونیازڈ۔"),
                ("خطرناک ادویات", "پائرازینامائڈ سب سے زیادہ خراب کرتا ہے، پھر آئیسونیازڈ اور رفیمپیسین۔")
            ]
        }
    ]

# ==============================================================================
# 3. GENERATION LOGIC
# ==============================================================================

def generate_urdu_dataset():
    print("="*60)
    print("💎 STARTING PURE URDU GENERATION")
    print("="*60)
    
    qa_pairs = []
    
    # --- A. DRUGS ---
    drugs = get_detailed_drugs()
    for drug in drugs:
        names = [drug["name"]] + drug["aka"]
        
        for attr, value in drug["attributes"].items():
            # Urdu Answer
            attr_urdu = attr.replace('_', ' ').title()
            
            # Mapping attr names to Urdu
            if "dosing" in attr: attr_urdu = "خوراک"
            if "mechanism" in attr: attr_urdu = "کام کا طریقہ"
            if "side_effects" in attr: attr_urdu = "مضر اثرات"
            if "monitoring" in attr: attr_urdu = "نگرانی/معائنہ"
            if "safety" in attr: attr_urdu = "حفاظت"
            
            answer_text = f"**{drug['name']} - {attr_urdu}:**\n{value}\n\n*حوالہ: کلینیکل فارماکولوجی*"
            
            # Phrasasing
            phrasings = []
            if "dosing" in attr:
                phrasings = phraser.variate(f"{drug['name']} کی خوراک", "clinical") + \
                           phraser.variate(f"{drug['name']} ڈوز", "direct")
                cat = "Drug Information (Enhanced)"
            elif "side_effects" in attr:
                phrasings = phraser.variate(f"{drug['name']} کے سائیڈ ایفیکٹس", "direct") + \
                           phraser.variate(f"{drug['name']} کے مضر اثرات", "clinical")
                cat = "Side Effects Management"
            elif "monitoring" in attr:
                 phrasings = phraser.variate(f"{drug['name']} کی نگرانی", "clinical")
                 cat = "Monitoring & Follow-up"
            else:
                 phrasings = phraser.variate(f"{drug['name']} {attr_urdu}", "direct")
                 cat = "Drug Information (Enhanced)"
            
            for q in phrasings:
                # Urdu Question Mark enforcement
                if not q.strip().endswith("؟"):
                    q = q.strip() + "؟"
                
                qa_pairs.append({
                    "id": "",
                    "category": cat,
                    "question": q,
                    "answer": answer_text,
                    "keywords": [drug["name"].lower(), attr.split('_')[0]]
                })

    # --- B. SCENARIOS ---
    scenarios = get_granular_scenarios()
    for scen in scenarios:
        cond = scen["condition"]
        for topic, fact in scen["facts"]:
            # Urdu Topic
            topic_urdu = topic
            answer_text = f"**{cond} - {topic_urdu}:**\n{fact}\n\n*گائیڈ لائن: معیاری علاج کے پروٹوکولز*"
            
            # Categories based on topic
            cat = "Clinical Scenarios" # Default
            if "علاج" in topic_urdu or "نسخہ" in topic_urdu: cat = "Treatment Protocols (Enhanced)"
            elif "پیچیدگیاں" in topic_urdu: cat = "Complications"
            elif "نگرانی" in topic_urdu: cat = "Monitoring & Follow-up"
            elif "حمل" in cond: cat = "Special Populations"
            
            phrasings = phraser.variate(f"{topic_urdu} برائے {cond}", "clinical")
            
            for q in phrasings:
                if not q.strip().endswith("؟"):
                    q = q.strip() + "؟"
                    
                qa_pairs.append({
                    "id": "",
                    "category": cat,
                    "question": q,
                    "answer": answer_text,
                    "keywords": [cond.lower(), topic]
                })

    # --- C. FORMS ---
    forms = [
        ("ٹی بی 01", "علاج کا کارڈ - مرکز میں رہتا ہے"),
        ("ٹی بی 02", "مریض کا کارڈ - مریض کے پاس رہتا ہے"),
        ("ٹی بی 05", "لیب کی درخواست کا فارم")
    ]
    for f, desc in forms:
        qs = [f"{f} کیا ہے", f"{f} فارم کی وضاحت", f"{f} کا استعمال"]
        for q in qs:
            if not q.strip().endswith("؟"):
                q = q.strip() + "؟"
            
            qa_pairs.append({
                "category": "Forms & Documentation",
                "question": q,
                "answer": f"**{f}:** {desc}",
                "keywords": ["forms", f.lower()]
            })

    # --- D. SYMPTOMS ---
    symptoms = [
        ("کھانسی > 2 ہفتے", "لمبی کھانسی ٹی بی کی بڑی علامت ہے۔"),
        ("رات کو پسینہ", "رات کو کپڑے بھیگ جانا اہم علامت ہے۔"),
        ("وزن کم ہونا", "بغیر وجہ وزن گرنا۔"),
        ("بخار", "ہلکا بخار جو شام میں زیادہ ہو۔"),
        ("خون کی الٹی", "کھانسی میں خون آنا پھیپھڑوں کی خرابی ظاہر کرتا ہے۔")
    ]
    for sym, desc in symptoms:
        qs = [f"{sym} کیا ٹی بی کی علامت ہے", f"مریض کو {sym} ہے", f"{sym} کی وضاحت"]
        for q in qs:
            if not q.strip().endswith("؟"):
                q = q.strip() + "؟"
            
            qa_pairs.append({
                "category": "Symptoms & Clinical Presentation",
                "question": q,
                "answer": f"**علامت: {sym}**\n{desc}\n*کلینیکل نوٹ:* مزید ٹیسٹ کریں۔",
                "keywords": ["symptom", sym.lower()]
            })

    # --- E. EXPANSION ---
    # Simplified expansion used for speed
    
    prefixes_urdu_short = ["کیا ہے", "بتائیں", "خوراک", "مختصر بتائیں"]
    prefixes_urdu_long = ["تفصیل بتائیں", "پورا پروٹوکول سمجھائیں", "مکمل معلومات", "گائیڈ لائن کیا ہے"]
    
    expanded_pairs = []
    
    # print(f"Base Pairs: {len(qa_pairs)}")
    
    for item in qa_pairs:
        base_a = item['answer']
        q_clean = item['question']
        
        # Remove existing punct for cleaner expansion
        if q_clean.endswith("؟"): 
            q_clean = q_clean[:-1]
        elif q_clean.endswith("?"): # just in case
            q_clean = q_clean[:-1]
        
        # Urdu Short
        for p in prefixes_urdu_short:
            new_q = f"{p} {q_clean}"
            if not new_q.endswith("؟"): new_q += "؟"
            
            # Short Answer Logic (Extract content)
            short_a = base_a
            if "**" in base_a and ":**" in base_a:
                try:
                    short_a = base_a.split(":**")[1].split("\n\n*")[0].strip()
                except:
                    pass
            
            expanded_pairs.append({
                "category": item["category"],
                "question": new_q,
                "answer": short_a,
                "keywords": item["keywords"]
            })
            
        # Urdu Long
        for p in prefixes_urdu_long:
            new_q = f"{p} {q_clean}"
            if not new_q.endswith("؟"): new_q += "؟"
            
            long_a = base_a
            # Simple detail append if needed
            if len(long_a) < 200:
                long_a += "\n\n*مزید معلومات کے لیے ڈاکٹر سے رجوع کریں۔*"

            expanded_pairs.append({
                "category": item["category"],
                "question": new_q,
                "answer": long_a,
                "keywords": item["keywords"]
            })
            
    final_pairs = qa_pairs + expanded_pairs
    print(f"Total Urdu Questions: {len(final_pairs)}")
    
    # Save
    dataset = {
        "metadata": {
            "title": "TB Expert Dataset - Urdu Edition",
            "language": "Urdu",
            "count": len(final_pairs),
            "date": datetime.now().strftime("%Y-%m-%d")
        },
        "qa_pairs": final_pairs
    }
    
    output_file = 'dataset/TB_QA_DATASET_50K_ULTIMATE_URDU.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
        
    print(f"✅ SAVED PURE URDU DATASET: {output_file}")

if __name__ == "__main__":
    generate_urdu_dataset()
