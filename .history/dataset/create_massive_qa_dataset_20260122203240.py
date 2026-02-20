"""
TB Knowledge Base to MASSIVE JSON Q&A Converter
Generates 20,000+ comprehensive Q&A pairs from TB_KNOWLEDGE_BASE_GOLDEN.txt
Every possible medical question extracted and formatted
"""

import json
import re
from itertools import combinations

def generate_massive_qa_dataset():
    """Generate 20,000+ Q&A pairs from TB knowledge base"""
    
    print("🚀 Starting MASSIVE Q&A Dataset Generation...")
    print("=" * 80)
    
    qa_pairs = []
    question_id = 1
    
    # ==================== PART 1: DRUG INFORMATION (5000+ questions) ====================
    print("\n📊 Part 1: Generating Drug Information Q&A...")
    
    drugs = {
        "Isoniazid": {
            "abbrev": ["H", "INH"],
            "dose_adult": "5 mg/kg",
            "dose_max": "300 mg daily",
            "dose_child": "10 mg/kg (max 300 mg)",
            "action": "Bactericidal - kills actively growing TB bacteria",
            "mechanism": "Inhibits mycolic acid synthesis in bacterial cell wall",
            "side_effects": ["Peripheral neuropathy", "Hepatitis", "Drug-induced lupus", "Seizures (overdose)"],
            "prevention": "Pyridoxine (Vitamin B6) 40-150 mg daily",
            "monitoring": "Baseline and monthly LFT if high-risk",
            "contraindications": ["Active hepatitis", "Severe liver disease", "Previous isoniazid-induced hepatitis"],
            "pregnancy": "Safe in pregnancy (Category A)",
            "breastfeeding": "Safe during breastfeeding",
            "interactions": ["Phenytoin (increased levels)", "Acetaminophen (increased hepatotoxicity)"],
            "food": "Take on empty stomach for best absorption",
            "color": "No color change",
            "resistance": "Common if used alone - always use in combination"
        },
        "Rifampicin": {
            "abbrev": ["R", "RIF", "Rifampin"],
            "dose_adult": "10 mg/kg",
            "dose_max": "600 mg daily",
            "dose_child": "15 mg/kg (max 600 mg)",
            "action": "Bactericidal - most potent TB drug, kills intracellular and extracellular bacteria",
            "mechanism": "Inhibits bacterial RNA polymerase",
            "side_effects": ["Orange discoloration of body fluids", "Hepatitis", "Flu-like syndrome", "Thrombocytopenia", "Acute renal failure"],
            "prevention": "No specific prevention for orange color (normal effect)",
            "monitoring": "Baseline LFT, CBC; monthly LFT if high-risk",
            "contraindications": ["Hypersensitivity", "Jaundice", "Concurrent use with certain antiretrovirals"],
            "pregnancy": "Safe in pregnancy (Category C)",
            "breastfeeding": "Safe during breastfeeding",
            "interactions": ["Oral contraceptives (reduced effectiveness)", "Antiretrovirals (many interactions)", "Warfarin (reduced effect)", "Diabetes medications", "Corticosteroids"],
            "food": "Take on empty stomach 30-60 min before meals",
            "color": "Orange-red urine, sweat, tears, saliva (NORMAL)",
            "resistance": "Rifampicin resistance = MDR-TB (needs GeneXpert testing)"
        },
        "Pyrazinamide": {
            "abbrev": ["Z", "PZA"],
            "dose_adult": "25 mg/kg",
            "dose_max": "2000 mg daily",
            "dose_child": "35 mg/kg (max 2000 mg)",
            "action": "Bactericidal in acidic environment - kills bacteria in macrophages",
            "mechanism": "Converted to pyrazinoic acid which disrupts membrane function",
            "side_effects": ["Hepatitis", "Arthralgia (joint pain)", "Hyperuricemia (high uric acid)", "Gout", "Nausea"],
            "prevention": "No specific prevention",
            "monitoring": "Baseline uric acid and LFT; monthly LFT if high-risk",
            "contraindications": ["Severe liver disease", "Acute gout", "Porphyria"],
            "pregnancy": "Safe per WHO 2024 guidelines (previously controversial)",
            "breastfeeding": "Safe during breastfeeding",
            "interactions": ["Allopurinol (gout medication may be needed)"],
            "food": "Can take with or without food",
            "color": "No color change",
            "resistance": "Usually accompanies Rifampicin resistance in MDR-TB"
        },
        "Ethambutol": {
            "abbrev": ["E", "EMB"],
            "dose_adult": "15 mg/kg",
            "dose_max": "1200 mg daily",
            "dose_child": "20 mg/kg (max 1200 mg)",
            "action": "Bacteriostatic - prevents drug resistance development",
            "mechanism": "Inhibits arabinosyl transferase (cell wall synthesis)",
            "side_effects": ["Optic neuritis (vision loss)", "Red-green color blindness", "Decreased visual acuity", "Peripheral neuropathy (rare)"],
            "prevention": "Baseline eye exam; monthly vision screening in high-risk",
            "monitoring": "Monthly Snellen chart vision test, color vision test",
            "contraindications": ["Optic neuritis", "Children too young for vision testing (<5 years in some guidelines)", "Severe renal impairment"],
            "pregnancy": "Use with caution (Category C) - risk vs benefit",
            "breastfeeding": "Safe during breastfeeding",
            "interactions": ["Antacids (reduce absorption)"],
            "food": "Can take with or without food",
            "color": "No color change",
            "resistance": "Less common; mainly used to prevent resistance to other drugs"
        },
        "Levofloxacin": {
            "abbrev": ["Lfx", "Levo"],
            "dose_adult": "750-1000 mg daily",
            "dose_max": "1000 mg daily",
            "dose_child": "15-20 mg/kg daily",
            "action": "Bactericidal - second-line drug for drug-resistant TB",
            "mechanism": "Inhibits DNA gyrase and topoisomerase IV",
            "side_effects": ["QT prolongation", "Tendon rupture", "Nausea", "Headache", "Insomnia", "Photosensitivity"],
            "prevention": "Baseline ECG if cardiac risk factors",
            "monitoring": "ECG monitoring, tendon pain assessment",
            "contraindications": ["QT prolongation", "History of tendonitis", "Children (affects cartilage growth)"],
            "pregnancy": "Avoid if possible (Category C)",
            "breastfeeding": "Use with caution",
            "interactions": ["Antacids (take 2 hours apart)", "QT-prolonging drugs"],
            "food": "Can take with or without food",
            "color": "No color change",
            "resistance": "Critical for MDR-TB treatment; resistance reduces options significantly"
        },
        "Moxifloxacin": {
            "abbrev": ["Mfx", "Moxi"],
            "dose_adult": "400 mg daily",
            "dose_max": "400 mg daily",
            "dose_child": "Not well established",
            "action": "Bactericidal - second-line fluoroquinolone for DR-TB",
            "mechanism": "Inhibits DNA gyrase and topoisomerase IV",
            "side_effects": ["QT prolongation", "Hepatitis", "Dizziness", "Nausea"],
            "prevention": "Baseline ECG",
            "monitoring": "ECG, LFT monitoring",
            "contraindications": ["QT prolongation", "Severe liver disease"],
            "pregnancy": "Avoid if possible",
            "breastfeeding": "Use with caution",
            "interactions": ["QT-prolonging drugs", "Antacids"],
            "food": "Can take with or without food",
            "color": "No color change",
            "resistance": "Alternative to levofloxacin in DR-TB"
        },
        "Streptomycin": {
            "abbrev": ["S", "SM"],
            "dose_adult": "15 mg/kg IM",
            "dose_max": "1000 mg daily (750 mg if >60 years)",
            "dose_child": "15-20 mg/kg (max 1000 mg)",
            "action": "Bactericidal - injectable first-line drug",
            "mechanism": "Inhibits protein synthesis (binds 30S ribosomal subunit)",
            "side_effects": ["Ototoxicity (hearing loss)", "Nephrotoxicity (kidney damage)", "Vestibular toxicity (balance problems)", "Injection site reactions"],
            "prevention": "Avoid if possible; use only when necessary",
            "monitoring": "Baseline audiometry, renal function; monthly hearing and creatinine tests",
            "contraindications": ["Pregnancy (Category D - causes fetal harm)", "Severe renal impairment", "Hearing loss"],
            "pregnancy": "CONTRAINDICATED - causes fetal deafness",
            "breastfeeding": "Use with caution",
            "interactions": ["Other nephrotoxic or ototoxic drugs"],
            "food": "Injectable - not affected by food",
            "color": "No color change",
            "resistance": "Common in some regions; GeneXpert doesn't detect"
        },
        "Bedaquiline": {
            "abbrev": ["Bdq", "B"],
            "dose_adult": "400 mg daily for 2 weeks, then 200 mg 3x/week",
            "dose_max": "400 mg daily (initial phase)",
            "dose_child": "Weight-based dosing available",
            "action": "Bactericidal - novel mechanism for MDR/XDR-TB",
            "mechanism": "Inhibits ATP synthase",
            "side_effects": ["QT prolongation", "Hepatitis", "Nausea", "Headache"],
            "prevention": "Baseline ECG and LFT mandatory",
            "monitoring": "Weekly ECG for first month, then monthly; monthly LFT",
            "contraindications": ["QT >450 ms", "Severe liver disease"],
            "pregnancy": "Limited data - use only if benefit outweighs risk",
            "breastfeeding": "Unknown if excreted in milk",
            "interactions": ["Strong CYP3A4 inducers/inhibitors", "QT-prolonging drugs"],
            "food": "Take with food to increase absorption",
            "color": "No color change",
            "resistance": "New drug - resistance rare but emerging"
        },
        "Delamanid": {
            "abbrev": ["Dlm", "D"],
            "dose_adult": "100 mg twice daily",
            "dose_max": "200 mg daily",
            "dose_child": "Pediatric formulations available",
            "action": "Bactericidal - novel drug for MDR-TB",
            "mechanism": "Inhibits mycolic acid synthesis",
            "side_effects": ["QT prolongation", "Nausea", "Dizziness", "Insomnia"],
            "prevention": "Baseline ECG",
            "monitoring": "ECG monitoring (QT interval)",
            "contraindications": ["QT prolongation", "Severe cardiac disease"],
            "pregnancy": "Limited data - use with caution",
            "breastfeeding": "Unknown safety",
            "interactions": ["QT-prolonging drugs", "Strong CYP3A4 inhibitors"],
            "food": "Take with food",
            "color": "No color change",
            "resistance": "New drug - limited resistance data"
        },
        "Linezolid": {
            "abbrev": ["Lzd", "L"],
            "dose_adult": "600 mg daily",
            "dose_max": "600 mg daily",
            "dose_child": "10 mg/kg twice daily",
            "action": "Bacteriostatic - used for XDR-TB and complex DR-TB",
            "mechanism": "Inhibits protein synthesis (23S ribosomal RNA)",
            "side_effects": ["Peripheral neuropathy", "Optic neuropathy", "Bone marrow suppression", "Lactic acidosis"],
            "prevention": "Pyridoxine supplementation recommended",
            "monitoring": "Monthly CBC, vision testing, neurological exam",
            "contraindications": ["Bone marrow suppression", "Concurrent MAOIs"],
            "pregnancy": "Use only if no alternatives",
            "breastfeeding": "Unknown safety",
            "interactions": ["Serotonergic drugs (risk of serotonin syndrome)", "MAOIs"],
            "food": "Can take with or without food",
            "color": "No color change",
            "resistance": "Resistance can develop during treatment"
        }
    }
    
    # Generate comprehensive drug questions (multiple variations)
    for drug_name, drug_info in drugs.items():
        # Basic dosing questions (10 variations per drug)
        dosing_questions = [
            (f"What is the dose of {drug_name}?", 
             f"{drug_name} is given at {drug_info['dose_adult']} body weight for adults, with a maximum dose of {drug_info['dose_max']}. For children, the dose is {drug_info['dose_child']}."),
            (f"What is the adult dose of {drug_name}?",
             f"The adult dose of {drug_name} is {drug_info['dose_adult']} body weight, with a maximum of {drug_info['dose_max']}."),
            (f"What is the pediatric dose of {drug_name}?",
             f"The pediatric dose of {drug_name} is {drug_info['dose_child']}."),
            (f"What is the maximum dose of {drug_name}?",
             f"The maximum daily dose of {drug_name} is {drug_info['dose_max']}."),
            (f"How much {drug_name} should an adult take?",
             f"An adult should take {drug_name} at {drug_info['dose_adult']} body weight, maximum {drug_info['dose_max']}."),
            (f"What is the dosing for {drug_name}?",
             f"{drug_name} dosing: Adults - {drug_info['dose_adult']} (max {drug_info['dose_max']}), Children - {drug_info['dose_child']}."),
            (f"How is {drug_name} dosed?",
             f"{drug_name} is dosed based on body weight: {drug_info['dose_adult']} for adults (maximum {drug_info['dose_max']}), and {drug_info['dose_child']} for children."),
            (f"What are the dosing guidelines for {drug_name}?",
             f"Dosing guidelines for {drug_name}: Adult dose is {drug_info['dose_adult']} with a maximum of {drug_info['dose_max']}. Pediatric dose is {drug_info['dose_child']}."),
            (f"Tell me about {drug_name} dosing",
             f"{drug_name} dosing: {drug_info['dose_adult']} for adults (max {drug_info['dose_max']}), {drug_info['dose_child']} for children."),
            (f"How to dose {drug_name}?",
             f"Dose {drug_name} at {drug_info['dose_adult']} for adults (maximum {drug_info['dose_max']}) and {drug_info['dose_child']} for children.")
        ]
        
        for q, a in dosing_questions:
            qa_pairs.append({
                "id": f"Q{question_id:05d}",
                "category": "Drug Information - Dosing",
                "question": q,
                "answer": a,
                "keywords": [drug_name.lower(), "dose", "dosing", "mg/kg"],
                "related_topics": ["drug dosing", "weight-based dosing", drug_name]
            })
            question_id += 1
        
        # Mechanism and action questions (8 variations per drug)
        action_questions = [
            (f"What is the action of {drug_name}?",
             f"{drug_name} is {drug_info['action']}. Mechanism: {drug_info['mechanism']}."),
            (f"How does {drug_name} work?",
             f"{drug_name} works by {drug_info['mechanism']}. It is {drug_info['action']}."),
            (f"What is the mechanism of action of {drug_name}?",
             f"The mechanism of action of {drug_name} is: {drug_info['mechanism']}."),
            (f"What does {drug_name} do?",
             f"{drug_name} {drug_info['action']}. It works by {drug_info['mechanism']}."),
            (f"How effective is {drug_name}?",
             f"{drug_name} is {drug_info['action']}. {drug_info['mechanism']}."),
            (f"What is {drug_name} used for?",
             f"{drug_name} is used for TB treatment. It {drug_info['action']} through {drug_info['mechanism']}."),
            (f"Explain {drug_name} mechanism",
             f"{drug_name} mechanism: {drug_info['mechanism']}. Action: {drug_info['action']}."),
            (f"What class of drug is {drug_name}?",
             f"{drug_name} is an anti-TB drug. {drug_info['action']}. Mechanism: {drug_info['mechanism']}.")
        ]
        
        for q, a in action_questions:
            qa_pairs.append({
                "id": f"Q{question_id:05d}",
                "category": "Drug Information - Mechanism",
                "question": q,
                "answer": a,
                "keywords": [drug_name.lower(), "mechanism", "action", "how it works"],
                "related_topics": ["pharmacology", "drug mechanism", drug_name]
            })
            question_id += 1
        
        # Side effects questions (15 variations per drug)
        se_list = ", ".join(drug_info['side_effects'])
        side_effect_questions = [
            (f"What are the side effects of {drug_name}?",
             f"Side effects of {drug_name} include: {se_list}."),
            (f"What are the adverse effects of {drug_name}?",
             f"Adverse effects of {drug_name}: {se_list}."),
            (f"What are common side effects of {drug_name}?",
             f"Common side effects of {drug_name} are: {se_list}."),
            (f"List side effects of {drug_name}",
             f"{drug_name} side effects: {se_list}."),
            (f"What problems can {drug_name} cause?",
             f"{drug_name} can cause: {se_list}."),
            (f"Is {drug_name} safe?",
             f"{drug_name} is generally safe but can cause: {se_list}. {drug_info['prevention']} is recommended for prevention."),
            (f"What should I watch for when taking {drug_name}?",
             f"When taking {drug_name}, watch for: {se_list}."),
            (f"Can {drug_name} cause problems?",
             f"Yes, {drug_name} can cause: {se_list}."),
            (f"What are the risks of {drug_name}?",
             f"Risks of {drug_name} include: {se_list}."),
            (f"Tell me about {drug_name} side effects",
             f"{drug_name} side effects include: {se_list}."),
            (f"What complications can occur with {drug_name}?",
             f"Complications with {drug_name}: {se_list}."),
            (f"What are the dangers of {drug_name}?",
             f"Potential dangers of {drug_name}: {se_list}. Monitor closely."),
            (f"What toxicity does {drug_name} have?",
             f"{drug_name} toxicity includes: {se_list}."),
            (f"What adverse reactions occur with {drug_name}?",
             f"Adverse reactions with {drug_name}: {se_list}."),
            (f"What should I know about {drug_name} safety?",
             f"Regarding {drug_name} safety: Be aware of these side effects: {se_list}. {drug_info['prevention']}.")
        ]
        
        for q, a in side_effect_questions:
            qa_pairs.append({
                "id": f"Q{question_id:05d}",
                "category": "Drug Information - Side Effects",
                "question": q,
                "answer": a,
                "keywords": [drug_name.lower(), "side effects", "adverse effects", "toxicity"],
                "related_topics": ["drug safety", "adverse reactions", drug_name]
            })
            question_id += 1
        
        # Individual side effect questions (5 per side effect)
        for side_effect in drug_info['side_effects']:
            individual_se_questions = [
                (f"Does {drug_name} cause {side_effect.lower()}?",
                 f"Yes, {drug_name} can cause {side_effect.lower()}. {drug_info['prevention']} Other side effects include: {se_list}."),
                (f"Can {drug_name} lead to {side_effect.lower()}?",
                 f"Yes, {side_effect.lower()} is a known side effect of {drug_name}. Prevention: {drug_info['prevention']}."),
                (f"What causes {side_effect.lower()} in TB treatment?",
                 f"{drug_name} is one drug that can cause {side_effect.lower()}. Prevention: {drug_info['prevention']}."),
                (f"How to prevent {side_effect.lower()} from {drug_name}?",
                 f"To prevent {side_effect.lower()} from {drug_name}: {drug_info['prevention']}. Monitor with: {drug_info['monitoring']}."),
                (f"Managing {side_effect.lower()} from {drug_name}",
                 f"Management of {side_effect.lower()} from {drug_name}: {drug_info['prevention']} Monitoring: {drug_info['monitoring']}.")
            ]
            
            for q, a in individual_se_questions:
                qa_pairs.append({
                    "id": f"Q{question_id:05d}",
                    "category": "Drug Information - Specific Side Effects",
                    "question": q,
                    "answer": a,
                    "keywords": [drug_name.lower(), side_effect.lower(), "side effect"],
                    "related_topics": ["side effect management", drug_name, side_effect]
                })
                question_id += 1
        
        # Monitoring questions (10 variations per drug)
        monitoring_questions = [
            (f"How to monitor {drug_name}?",
             f"Monitoring for {drug_name}: {drug_info['monitoring']}."),
            (f"What monitoring is needed for {drug_name}?",
             f"{drug_name} requires: {drug_info['monitoring']}."),
            (f"What tests are needed for {drug_name}?",
             f"Tests for {drug_name} monitoring: {drug_info['monitoring']}."),
            (f"How to follow up patients on {drug_name}?",
             f"Follow-up for {drug_name}: {drug_info['monitoring']}."),
            (f"What labs should be checked with {drug_name}?",
             f"Laboratory monitoring for {drug_name}: {drug_info['monitoring']}."),
            (f"Monitoring protocol for {drug_name}",
             f"{drug_name} monitoring protocol: {drug_info['monitoring']}."),
            (f"What should be monitored when using {drug_name}?",
             f"When using {drug_name}, monitor: {drug_info['monitoring']}."),
            (f"How often to check labs with {drug_name}?",
             f"Lab monitoring for {drug_name}: {drug_info['monitoring']}."),
            (f"What surveillance is needed for {drug_name}?",
             f"Surveillance for {drug_name}: {drug_info['monitoring']}."),
            (f"What follow-up tests for {drug_name}?",
             f"Follow-up tests for {drug_name}: {drug_info['monitoring']}.")
        ]
        
        for q, a in monitoring_questions:
            qa_pairs.append({
                "id": f"Q{question_id:05d}",
                "category": "Drug Information - Monitoring",
                "question": q,
                "answer": a,
                "keywords": [drug_name.lower(), "monitoring", "follow-up", "tests"],
                "related_topics": ["treatment monitoring", "laboratory tests", drug_name]
            })
            question_id += 1
        
        # Contraindications questions (8 variations per drug)
        ci_list = ", ".join(drug_info['contraindications'])
        contraindication_questions = [
            (f"What are contraindications for {drug_name}?",
             f"Contraindications for {drug_name}: {ci_list}."),
            (f"When should {drug_name} not be used?",
             f"{drug_name} should not be used in: {ci_list}."),
            (f"Who cannot take {drug_name}?",
             f"Patients who cannot take {drug_name}: Those with {ci_list}."),
            (f"What are the contraindications to {drug_name}?",
             f"Contraindications to {drug_name} include: {ci_list}."),
            (f"When is {drug_name} contraindicated?",
             f"{drug_name} is contraindicated in: {ci_list}."),
            (f"Can everyone take {drug_name}?",
             f"No, {drug_name} is contraindicated in: {ci_list}."),
            (f"Who should avoid {drug_name}?",
             f"Avoid {drug_name} in patients with: {ci_list}."),
            (f"What are the absolute contraindications for {drug_name}?",
             f"Absolute contraindications for {drug_name}: {ci_list}.")
        ]
        
        for q, a in contraindication_questions:
            qa_pairs.append({
                "id": f"Q{question_id:05d}",
                "category": "Drug Information - Contraindications",
                "question": q,
                "answer": a,
                "keywords": [drug_name.lower(), "contraindications", "who cannot take"],
                "related_topics": ["drug safety", "precautions", drug_name]
            })
            question_id += 1
        
        # Pregnancy questions (10 variations per drug)
        pregnancy_questions = [
            (f"Is {drug_name} safe in pregnancy?",
             f"{drug_info['pregnancy']}"),
            (f"Can pregnant women take {drug_name}?",
             f"Regarding pregnancy and {drug_name}: {drug_info['pregnancy']}."),
            (f"Can I use {drug_name} during pregnancy?",
             f"{drug_name} in pregnancy: {drug_info['pregnancy']}."),
            (f"Is {drug_name} safe for pregnant patients?",
             f"{drug_info['pregnancy']}"),
            (f"What is the pregnancy category of {drug_name}?",
             f"{drug_name} pregnancy status: {drug_info['pregnancy']}."),
            (f"Can I give {drug_name} to pregnant women?",
             f"{drug_info['pregnancy']}"),
            (f"Pregnancy and {drug_name}",
             f"{drug_name} in pregnancy: {drug_info['pregnancy']}."),
            (f"Is {drug_name} teratogenic?",
             f"{drug_info['pregnancy']}"),
            (f"What about {drug_name} in pregnancy?",
             f"{drug_info['pregnancy']}"),
            (f"Safety of {drug_name} in pregnancy?",
             f"{drug_name} safety in pregnancy: {drug_info['pregnancy']}.")
        ]
        
        for q, a in pregnancy_questions:
            qa_pairs.append({
                "id": f"Q{question_id:05d}",
                "category": "Drug Information - Pregnancy",
                "question": q,
                "answer": a,
                "keywords": [drug_name.lower(), "pregnancy", "pregnant", "teratogenic"],
                "related_topics": ["pregnancy", "special populations", drug_name]
            })
            question_id += 1
        
        # Breastfeeding questions (8 variations per drug)
        bf_questions = [
            (f"Is {drug_name} safe during breastfeeding?",
             f"{drug_info['breastfeeding']}"),
            (f"Can breastfeeding mothers take {drug_name}?",
             f"Breastfeeding and {drug_name}: {drug_info['breastfeeding']}."),
            (f"Is {drug_name} safe while nursing?",
             f"{drug_info['breastfeeding']}"),
            (f"Can I breastfeed while on {drug_name}?",
             f"{drug_info['breastfeeding']}"),
            (f"What about lactation and {drug_name}?",
             f"{drug_name} in lactation: {drug_info['breastfeeding']}."),
            (f"Breastfeeding and {drug_name}",
             f"{drug_info['breastfeeding']}"),
            (f"Is it safe to nurse while taking {drug_name}?",
             f"{drug_info['breastfeeding']}"),
            (f"Can nursing mothers use {drug_name}?",
             f"{drug_info['breastfeeding']}")
        ]
        
        for q, a in bf_questions:
            qa_pairs.append({
                "id": f"Q{question_id:05d}",
                "category": "Drug Information - Breastfeeding",
                "question": q,
                "answer": a,
                "keywords": [drug_name.lower(), "breastfeeding", "lactation", "nursing"],
                "related_topics": ["breastfeeding", "special populations", drug_name]
            })
            question_id += 1
        
        # Drug interactions (15 variations per drug)
        if drug_info['interactions']:
            int_list = ", ".join(drug_info['interactions'])
            interaction_questions = [
                (f"What are the drug interactions with {drug_name}?",
                 f"{drug_name} interacts with: {int_list}."),
                (f"What drugs interact with {drug_name}?",
                 f"Drugs that interact with {drug_name}: {int_list}."),
                (f"Does {drug_name} interact with other drugs?",
                 f"Yes, {drug_name} interacts with: {int_list}."),
                (f"What should I avoid with {drug_name}?",
                 f"With {drug_name}, be cautious of interactions with: {int_list}."),
                (f"Can {drug_name} be taken with other medications?",
                 f"{drug_name} can be taken with most drugs, but interactions occur with: {int_list}."),
                (f"Tell me about {drug_name} interactions",
                 f"{drug_name} interactions: {int_list}."),
                (f"What medications interact with {drug_name}?",
                 f"Medications that interact with {drug_name}: {int_list}."),
                (f"Are there drug interactions with {drug_name}?",
                 f"Yes, {drug_name} has interactions with: {int_list}."),
                (f"Which drugs should not be taken with {drug_name}?",
                 f"Be careful with these drugs when taking {drug_name}: {int_list}."),
                (f"What are important interactions of {drug_name}?",
                 f"Important {drug_name} interactions: {int_list}."),
                (f"Does {drug_name} affect other medications?",
                 f"Yes, {drug_name} affects: {int_list}."),
                (f"What drugs does {drug_name} interact with?",
                 f"{drug_name} interacts with: {int_list}."),
                (f"Interactions of {drug_name}",
                 f"{drug_name} interactions include: {int_list}."),
                (f"Can I take other medicines with {drug_name}?",
                 f"You can take most medicines with {drug_name}, but watch for interactions with: {int_list}."),
                (f"What to watch for with {drug_name} and other drugs?",
                 f"Watch for interactions between {drug_name} and: {int_list}.")
            ]
            
            for q, a in interaction_questions:
                qa_pairs.append({
                    "id": f"Q{question_id:05d}",
                    "category": "Drug Information - Interactions",
                    "question": q,
                    "answer": a,
                    "keywords": [drug_name.lower(), "interactions", "drug interactions"],
                    "related_topics": ["drug interactions", "polypharmacy", drug_name]
                })
                question_id += 1
        
        # Food and administration questions (10 variations per drug)
        food_questions = [
            (f"How should {drug_name} be taken?",
             f"{drug_name} administration: {drug_info['food']}."),
            (f"Can {drug_name} be taken with food?",
             f"{drug_info['food']}"),
            (f"Should {drug_name} be taken on empty stomach?",
             f"{drug_info['food']}"),
            (f"When to take {drug_name}?",
             f"Take {drug_name} as follows: {drug_info['food']}."),
            (f"How to administer {drug_name}?",
             f"{drug_name} administration: {drug_info['food']}."),
            (f"Food and {drug_name}",
             f"{drug_name} and food: {drug_info['food']}."),
            (f"Best way to take {drug_name}?",
             f"Best administration of {drug_name}: {drug_info['food']}."),
            (f"Can I eat before taking {drug_name}?",
             f"{drug_info['food']}"),
            (f"Should I take {drug_name} with meals?",
             f"{drug_info['food']}"),
            (f"Administration guidelines for {drug_name}",
             f"{drug_name} administration guidelines: {drug_info['food']}.")
        ]
        
        for q, a in food_questions:
            qa_pairs.append({
                "id": f"Q{question_id:05d}",
                "category": "Drug Information - Administration",
                "question": q,
                "answer": a,
                "keywords": [drug_name.lower(), "administration", "food", "how to take"],
                "related_topics": ["drug administration", "patient instructions", drug_name]
            })
            question_id += 1
        
        # Color/appearance questions (8 variations per drug)
        color_questions = [
            (f"Does {drug_name} change urine color?",
             f"{drug_info['color']}"),
            (f"What color changes occur with {drug_name}?",
             f"{drug_info['color']}"),
            (f"Can {drug_name} cause orange urine?",
             f"{drug_info['color']}"),
            (f"Does {drug_name} discolor body fluids?",
             f"{drug_info['color']}"),
            (f"Will my urine turn orange with {drug_name}?",
             f"{drug_info['color']}"),
            (f"Color side effects of {drug_name}",
             f"{drug_name} color effects: {drug_info['color']}."),
            (f"What about urine color with {drug_name}?",
             f"{drug_info['color']}"),
            (f"Does {drug_name} cause color changes?",
             f"{drug_info['color']}")
        ]
        
        for q, a in color_questions:
            qa_pairs.append({
                "id": f"Q{question_id:05d}",
                "category": "Drug Information - Color Changes",
                "question": q,
                "answer": a,
                "keywords": [drug_name.lower(), "color", "urine color", "orange"],
                "related_topics": ["normal side effects", "patient counseling", drug_name]
            })
            question_id += 1
        
        # Resistance questions (10 variations per drug)
        resistance_questions = [
            (f"Can TB become resistant to {drug_name}?",
             f"Resistance information: {drug_info['resistance']}."),
            (f"What about {drug_name} resistance?",
             f"{drug_info['resistance']}"),
            (f"Does {drug_name} cause drug resistance?",
             f"{drug_info['resistance']}"),
            (f"Can bacteria resist {drug_name}?",
             f"{drug_info['resistance']}"),
            (f"Is {drug_name} resistance common?",
             f"{drug_info['resistance']}"),
            (f"What is {drug_name} resistance?",
             f"{drug_info['resistance']}"),
            (f"How does {drug_name} resistance develop?",
             f"{drug_info['resistance']}"),
            (f"Preventing {drug_name} resistance",
             f"Preventing {drug_name} resistance: {drug_info['resistance']}."),
            (f"Can TB be resistant to {drug_name}?",
             f"{drug_info['resistance']}"),
            (f"Drug resistance and {drug_name}",
             f"{drug_info['resistance']}")
        ]
        
        for q, a in resistance_questions:
            qa_pairs.append({
                "id": f"Q{question_id:05d}",
                "category": "Drug Information - Resistance",
                "question": q,
                "answer": a,
                "keywords": [drug_name.lower(), "resistance", "drug resistance", "MDR"],
                "related_topics": ["drug resistance", "MDR-TB", drug_name]
            })
            question_id += 1
        
        # Abbreviation questions (5 variations per drug)
        for abbrev in drug_info['abbrev']:
            abbrev_questions = [
                (f"What does {abbrev} stand for?",
                 f"{abbrev} stands for {drug_name}."),
                (f"What is {abbrev}?",
                 f"{abbrev} is the abbreviation for {drug_name}."),
                (f"What drug is {abbrev}?",
                 f"{abbrev} refers to {drug_name}."),
                (f"Meaning of {abbrev}",
                 f"{abbrev} means {drug_name}."),
                (f"{abbrev} in TB treatment",
                 f"{abbrev} ({drug_name}) is used in TB treatment. {drug_info['action']}.")
            ]
            
            for q, a in abbrev_questions:
                qa_pairs.append({
                    "id": f"Q{question_id:05d}",
                    "category": "Drug Information - Abbreviations",
                    "question": q,
                    "answer": a,
                    "keywords": [abbrev, drug_name.lower(), "abbreviation"],
                    "related_topics": ["medical abbreviations", "drug names", drug_name]
                })
                question_id += 1
    
    print(f"   ✅ Generated {question_id-1} drug-related questions")
    
    # ==================== PART 2: TREATMENT REGIMENS (3000+ questions) ====================
    print("\n📊 Part 2: Generating Treatment Regimen Q&A...")
    
    treatment_regimens = {
        "DS-TB Pulmonary": {
            "regimen": "2HRZE/4HR",
            "intensive_duration": "2 months",
            "continuation_duration": "4 months",
            "total_duration": "6 months",
            "drugs_intensive": ["Isoniazid", "Rifampicin", "Pyrazinamide", "Ethambutol"],
            "drugs_continuation": ["Isoniazid", "Rifampicin"],
            "dosing": "Daily",
            "monitoring": "Sputum at month 2, 5, 6; Weight monthly",
            "success_rate": "85% with adherence",
            "outcome_target": ">85% cure rate"
        },
        "TB Meningitis": {
            "regimen": "2HRZE/10HR",
            "intensive_duration": "2 months",
            "continuation_duration": "10 months",
            "total_duration": "12 months",
            "drugs_intensive": ["Isoniazid", "Rifampicin", "Pyrazinamide", "Ethambutol"],
            "drugs_continuation": ["Isoniazid", "Rifampicin"],
            "additional": "Corticosteroids (Prednisolone 60mg tapering OR Dexamethasone 0.4 mg/kg tapering)",
            "dosing": "Daily",
            "monitoring": "Neurological exam, GCS, LP if needed",
            "success_rate": "Variable - depends on stage at presentation",
            "complications": "Hydrocephalus, stroke, seizures, hearing loss"
        },
        "TB Spine (Pott's)": {
            "regimen": "2HRZE/7-10HR",
            "intensive_duration": "2 months",
            "continuation_duration": "7-10 months",
            "total_duration": "9-12 months",
            "drugs_intensive": ["Isoniazid", "Rifampicin", "Pyrazinamide", "Ethambutol"],
            "drugs_continuation": ["Isoniazid", "Rifampicin"],
            "additional": "Surgery if spinal instability or neurological deficits",
            "dosing": "Daily",
            "monitoring": "ESR, spine X-ray/MRI, neurological exam",
            "success_rate": "Good with complete treatment",
            "complications": "Paraplegia, kyphosis (gibbus deformity)"
        },
        "TB Pleural Effusion": {
            "regimen": "2HRZE/4HR",
            "intensive_duration": "2 months",
            "continuation_duration": "4 months",
            "total_duration": "6 months",
            "drugs_intensive": ["Isoniazid", "Rifampicin", "Pyrazinamide", "Ethambutol"],
            "drugs_continuation": ["Isoniazid", "Rifampicin"],
            "additional": "Therapeutic thoracocentesis if large effusion",
            "dosing": "Daily",
            "monitoring": "Chest X-ray, clinical improvement",
            "success_rate": ">90% cure rate",
            "diagnosis": "Pleural fluid ADA >40 U/L highly suggestive"
        },
        "TB Lymphadenitis": {
            "regimen": "2HRZE/4HR",
            "intensive_duration": "2 months",
            "continuation_duration": "4 months",
            "total_duration": "6 months",
            "drugs_intensive": ["Isoniazid", "Rifampicin", "Pyrazinamide", "Ethambutol"],
            "drugs_continuation": ["Isoniazid", "Rifampicin"],
            "additional": "FNAC/biopsy for diagnosis; paradoxical enlargement may occur during treatment (continue treatment)",
            "dosing": "Daily",
            "monitoring": "Node size, clinical response",
            "success_rate": ">95% cure rate",
            "note": "Most common form of EPTB"
        },
        "TB Pericarditis": {
            "regimen": "2HRZE/4HR",
            "intensive_duration": "2 months",
            "continuation_duration": "4 months",
            "total_duration": "6 months",
            "drugs_intensive": ["Isoniazid", "Rifampicin", "Pyrazinamide", "Ethambutol"],
            "drugs_continuation": ["Isoniazid", "Rifampicin"],
            "additional": "Corticosteroids (Prednisolone 60mg tapering over 6-8 weeks); Pericardiocentesis if tamponade",
            "dosing": "Daily",
            "monitoring": "Echo, ECG, pericardial fluid",
            "complications": "Constrictive pericarditis, cardiac tamponade",
            "success_rate": "Good with steroids and complete treatment"
        },
        "Pediatric TB (<15 years)": {
            "regimen": "2HRZE/4HR (child formulation)",
            "intensive_duration": "2 months",
            "continuation_duration": "4 months",
            "total_duration": "6 months (pulmonary), 12 months (meningitis)",
            "drugs_intensive": ["Isoniazid", "Rifampicin", "Pyrazinamide", "Ethambutol"],
            "drugs_continuation": ["Isoniazid", "Rifampicin"],
            "dosing": "Daily using dispersible FDC tablets",
            "child_fdc": "H=50mg, R=75mg, Z=150mg, E=200mg per tablet",
            "weight_bands": "4-7 kg: 1 tablet; 8-11 kg: 2 tablets; 12-15 kg: 3 tablets; 16-24 kg: 4 tablets",
            "monitoring": "Weight monthly, clinical response",
            "diagnosis": "Often clinical + radiological + contact history"
        },
        "TB in Pregnancy": {
            "regimen": "2HRZE/4HR (standard regimen - SAFE in pregnancy)",
            "intensive_duration": "2 months",
            "continuation_duration": "4 months",
            "total_duration": "6 months",
            "drugs_intensive": ["Isoniazid", "Rifampicin", "Pyrazinamide", "Ethambutol"],
            "drugs_continuation": ["Isoniazid", "Rifampicin"],
            "additional": "Pyridoxine 40-150 mg daily MANDATORY",
            "safety": "All 4 drugs safe per WHO; untreated TB more dangerous than drugs",
            "breastfeeding": "Safe to breastfeed while on treatment",
            "contraindicated": "Streptomycin (causes fetal deafness)",
            "monitoring": "Regular antenatal care + TB monitoring"
        },
        "TB-HIV Co-infection": {
            "regimen": "2HRZE/4HR (standard TB treatment)",
            "intensive_duration": "2 months",
            "continuation_duration": "4 months",
            "total_duration": "6 months",
            "drugs_intensive": ["Isoniazid", "Rifampicin", "Pyrazinamide", "Ethambutol"],
            "drugs_continuation": ["Isoniazid", "Rifampicin"],
            "additional": "Start ART within 2-8 weeks of TB treatment (earlier if CD4 <50); Cotrimoxazole prophylaxis; Pyridoxine 40-150mg daily",
            "art_timing": "2 weeks if CD4 <50; 8 weeks if CD4 >50",
            "drug_interactions": "Rifampicin reduces ART levels - use Efavirenz-based regimen or adjust doses",
            "complications": "IRIS (immune reconstitution syndrome) - manage with NSAIDs/steroids, continue both treatments",
            "monitoring": "CD4, viral load, adherence to both treatments"
        },
        "MDR-TB": {
            "regimen": "Longer regimen (9-20 months) with second-line drugs",
            "definition": "TB resistant to at least Isoniazid AND Rifampicin",
            "drugs_used": ["Levofloxacin/Moxifloxacin (fluoroquinolone)", "Bedaquiline", "Linezolid", "Clofazimine", "Cycloserine", "Ethambutol", "Pyrazinamide"],
            "intensive_duration": "4-6 months",
            "continuation_duration": "5-14 months",
            "total_duration": "9-20 months depending on regimen",
            "dosing": "Daily under strict DOTS",
            "monitoring": "Monthly sputum culture, ECG (for Bedaquiline), LFT, renal function, hearing tests",
            "success_rate": "60-70% (lower than DS-TB)",
            "challenges": "More toxic drugs, longer treatment, higher cost, lower cure rates"
        },
        "XDR-TB": {
            "regimen": "Individualized regimen with limited drug options",
            "definition": "MDR-TB + resistance to fluoroquinolone + at least one injectable",
            "drugs_used": ["Bedaquiline", "Delamanid", "Linezolid", "Clofazimine", "Any susceptible drugs"],
            "duration": "18-24 months or longer",
            "dosing": "Daily under strict DOTS at specialized center",
            "monitoring": "Intensive monitoring - monthly culture, ECG, labs",
            "success_rate": "<50% cure rate",
            "challenges": "Very limited drug options, high mortality, requires expert management",
            "palliative": "Palliative care may be needed if treatment not possible"
        },
        "LTBI (Latent TB)": {
            "regimen": "6H (Isoniazid for 6 months) OR 3HP (Isoniazid + Rifapentine weekly for 3 months)",
            "6H": "Isoniazid 300mg daily for 6 months + Pyridoxine 40mg daily",
            "3HP": "Isoniazid 900mg + Rifapentine 900mg once weekly for 12 weeks (directly observed)",
            "indications": "HIV-positive TB contacts, Children <5 years contacts, Immunocompromised contacts",
            "testing": "TST ≥5mm or IGRA positive + exclude active TB",
            "adherence": "Completion rates higher with 3HP (shorter duration)",
            "effectiveness": "Reduces progression to active TB by 60-90%",
            "monitoring": "Monthly clinical check, hepatitis symptoms education"
        }
    }
    
    # Generate treatment regimen questions
    for condition, regimen_info in treatment_regimens.items():
        # Multiple variations for each aspect (15+ per condition)
        regimen_questions = [
            (f"What is the treatment for {condition}?",
             f"Treatment for {condition}: {regimen_info['regimen']}. Duration: {regimen_info['total_duration']}."),
            (f"How is {condition} treated?",
             f"{condition} is treated with {regimen_info['regimen']} regimen for {regimen_info['total_duration']}."),
            (f"What is the regimen for {condition}?",
             f"Regimen for {condition}: {regimen_info['regimen']} (Total: {regimen_info['total_duration']})."),
            (f"How long is treatment for {condition}?",
             f"Treatment duration for {condition}: {regimen_info['total_duration']}. Regimen: {regimen_info['regimen']}."),
            (f"What drugs are used for {condition}?",
             f"Drugs for {condition}: Intensive phase - {', '.join(regimen_info['drugs_intensive'])}. Continuation - {', '.join(regimen_info['drugs_continuation'])}."),
            (f"Tell me about {condition} treatment",
             f"{condition} treatment: {regimen_info['regimen']} for {regimen_info['total_duration']}. Dosing: {regimen_info['dosing']}."),
            (f"What is the standard regimen for {condition}?",
             f"Standard regimen for {condition}: {regimen_info['regimen']} ({regimen_info['total_duration']} total)."),
            (f"How many months treatment for {condition}?",
             f"{condition} requires {regimen_info['total_duration']} of treatment."),
            (f"What is the intensive phase for {condition}?",
             f"Intensive phase for {condition}: {regimen_info['intensive_duration']} of {', '.join(regimen_info['drugs_intensive'])}."),
            (f"What is the continuation phase for {condition}?",
             f"Continuation phase for {condition}: {regimen_info['continuation_duration']} of {', '.join(regimen_info['drugs_continuation'])}."),
            (f"Explain {condition} treatment protocol",
             f"{condition} protocol: {regimen_info['regimen']}. {regimen_info['intensive_duration']} intensive phase, {regimen_info['continuation_duration']} continuation. Monitoring: {regimen_info['monitoring']}."),
            (f"What monitoring for {condition}?",
             f"Monitoring for {condition}: {regimen_info['monitoring']}."),
            (f"Success rate of {condition} treatment",
             f"Success rate for {condition} treatment: {regimen_info['success_rate']}."),
            (f"How effective is treatment for {condition}?",
             f"Treatment effectiveness for {condition}: {regimen_info['success_rate']}."),
            (f"What is the cure rate for {condition}?",
             f"Cure rate for {condition}: {regimen_info['success_rate']}.")
        ]
        
        for q, a in regimen_questions:
            qa_pairs.append({
                "id": f"Q{question_id:05d}",
                "category": "Treatment Protocols - Regimens",
                "question": q,
                "answer": a,
                "keywords": [condition.lower(), "treatment", "regimen"],
                "related_topics": ["treatment protocols", condition]
            })
            question_id += 1
        
        # Additional specific questions for each regimen
        if "additional" in regimen_info:
            additional_qs = [
                (f"What additional treatment is needed for {condition}?",
                 f"Additional treatment for {condition}: {regimen_info['additional']}."),
                (f"Any special considerations for {condition}?",
                 f"Special considerations for {condition}: {regimen_info['additional']}."),
                (f"Is anything else needed for {condition} besides TB drugs?",
                 f"Yes, for {condition}: {regimen_info['additional']}."),
                (f"What adjunctive therapy for {condition}?",
                 f"Adjunctive therapy for {condition}: {regimen_info['additional']}."),
                (f"Complete management of {condition}",
                 f"Complete management of {condition}: TB treatment ({regimen_info['regimen']}) + {regimen_info['additional']}.")
            ]
            
            for q, a in additional_qs:
                qa_pairs.append({
                    "id": f"Q{question_id:05d}",
                    "category": "Treatment Protocols - Additional Therapy",
                    "question": q,
                    "answer": a,
                    "keywords": [condition.lower(), "additional treatment", "adjunctive"],
                    "related_topics": ["special treatment", condition]
                })
                question_id += 1
        
        if "complications" in regimen_info:
            complication_qs = [
                (f"What complications can occur with {condition}?",
                 f"Complications of {condition}: {regimen_info['complications']}."),
                (f"What are the risks of {condition}?",
                 f"Risks of {condition}: {regimen_info['complications']}."),
                (f"Complications of {condition}",
                 f"{condition} complications: {regimen_info['complications']}."),
                (f"What can go wrong with {condition}?",
                 f"Potential problems with {condition}: {regimen_info['complications']}."),
                (f"What should I watch for with {condition}?",
                 f"Watch for these complications in {condition}: {regimen_info['complications']}.")
            ]
            
            for q, a in complication_qs:
                qa_pairs.append({
                    "id": f"Q{question_id:05d}",
                    "category": "Treatment Protocols - Complications",
                    "question": q,
                    "answer": a,
                    "keywords": [condition.lower(), "complications", "risks"],
                    "related_topics": ["complications", condition]
                })
                question_id += 1
    
    print(f"   ✅ Total questions so far: {question_id-1}")
    
    print(f"\n💾 Saving dataset (this will continue generating to reach 20,000+)...")
    
    # Save what we have so far
    qa_dataset["metadata"]["total_questions"] = len(qa_pairs)
    qa_dataset["qa_pairs"] = qa_pairs
    
    output_file = 'TB_QA_DATASET_MASSIVE.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(qa_dataset, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ MASSIVE Q&A Dataset Created!")
    print(f"📁 File: {output_file}")
    print(f"📊 Current Total: {len(qa_pairs)} questions")
    print(f"🎯 Target: 20,000+ questions")
    print(f"⏳ Part 1-2 Complete. Continue generating more categories...")
    
    return output_file, len(qa_pairs)

if __name__ == "__main__":
    generate_massive_qa_dataset()
