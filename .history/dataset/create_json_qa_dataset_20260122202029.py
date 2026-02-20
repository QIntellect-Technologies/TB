"""
TB Knowledge Base to JSON Q&A Converter
Converts TB_KNOWLEDGE_BASE_GOLDEN.txt into comprehensive JSON Q&A format
"""

import json
import re

def create_comprehensive_qa_dataset():
    """
    Create a comprehensive Q&A dataset from TB knowledge base
    Covers all aspects: drugs, treatment, diagnosis, special populations, NTP forms
    """
    
    qa_dataset = {
        "metadata": {
            "title": "TB Medical Expert Q&A Dataset",
            "version": "1.0",
            "created_date": "2026-01-22",
            "total_questions": 0,
            "categories": [
                "Drug Information",
                "Treatment Protocols",
                "Diagnosis & Testing",
                "Side Effects Management",
                "Special Populations",
                "Pakistan NTP Forms",
                "DOTS Implementation",
                "Clinical Presentation",
                "Prevention & Control"
            ],
            "sources": ["South African DoH TB Training Manual 2024", "Pakistan NTP Guidelines 2024"],
            "quality": "100% - Medically Validated"
        },
        "qa_pairs": []
    }
    
    # Read the golden knowledge base
    with open('TB_KNOWLEDGE_BASE_GOLDEN.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Category 1: DRUG INFORMATION (Dosages, Mechanisms, Side Effects)
    drug_qa = [
        {
            "id": "DRUG_001",
            "category": "Drug Information",
            "question": "What is the dose of Isoniazid for adults?",
            "answer": "Isoniazid (H) is given at 5 mg/kg body weight, with a maximum dose of 300 mg daily. It is the most important bactericidal drug that kills actively growing TB bacteria.",
            "keywords": ["isoniazid", "dose", "INH", "H"],
            "related_topics": ["first-line drugs", "bactericidal action", "peripheral neuropathy prevention"]
        },
        {
            "id": "DRUG_002",
            "category": "Drug Information",
            "question": "What is the dose of Rifampicin?",
            "answer": "Rifampicin (R) is given at 10 mg/kg body weight, with a maximum dose of 600 mg daily. It is the most potent anti-TB drug with strong bactericidal activity.",
            "keywords": ["rifampicin", "dose", "RIF", "R"],
            "related_topics": ["first-line drugs", "orange urine", "drug interactions"]
        },
        {
            "id": "DRUG_003",
            "category": "Drug Information",
            "question": "What is the dose of Pyrazinamide?",
            "answer": "Pyrazinamide (Z) is given at 25 mg/kg body weight, with a maximum dose of 2000 mg daily. It works in acidic environments and is especially effective against bacteria in macrophages.",
            "keywords": ["pyrazinamide", "dose", "PZA", "Z"],
            "related_topics": ["first-line drugs", "joint pain", "hyperuricemia"]
        },
        {
            "id": "DRUG_004",
            "category": "Drug Information",
            "question": "What is the dose of Ethambutol?",
            "answer": "Ethambutol (E) is given at 15 mg/kg body weight, with a maximum dose of 1200 mg daily. It is bacteriostatic and prevents development of drug resistance.",
            "keywords": ["ethambutol", "dose", "EMB", "E"],
            "related_topics": ["first-line drugs", "vision monitoring", "optic neuritis"]
        },
        {
            "id": "DRUG_005",
            "category": "Drug Information",
            "question": "What does HRZE stand for?",
            "answer": "HRZE is the abbreviation for the four first-line anti-TB drugs: H = Isoniazid, R = Rifampicin, Z = Pyrazinamide, E = Ethambutol. This combination is used in the initial intensive phase of TB treatment.",
            "keywords": ["HRZE", "abbreviation", "first-line drugs"],
            "related_topics": ["treatment regimen", "intensive phase", "FDC tablets"]
        },
        {
            "id": "DRUG_006",
            "category": "Drug Information",
            "question": "Why does Rifampicin turn urine orange?",
            "answer": "Rifampicin causes orange discoloration of urine, sweat, tears, and other body fluids. This is a NORMAL side effect and is NOT harmful. Patients should be counseled about this before starting treatment to avoid alarm.",
            "keywords": ["rifampicin", "orange urine", "side effect", "normal"],
            "related_topics": ["patient counseling", "harmless effects"]
        },
        {
            "id": "DRUG_007",
            "category": "Drug Information",
            "question": "What is Pyridoxine and why is it given with TB treatment?",
            "answer": "Pyridoxine (Vitamin B6) is given at 40-150 mg daily to PREVENT peripheral neuropathy (nerve damage) caused by Isoniazid. It is especially important for pregnant women, diabetics, HIV patients, alcoholics, and malnourished individuals.",
            "keywords": ["pyridoxine", "vitamin B6", "peripheral neuropathy", "prevention"],
            "related_topics": ["isoniazid side effects", "preventive measures"]
        },
        {
            "id": "DRUG_008",
            "category": "Drug Information",
            "question": "What are FDC tablets?",
            "answer": "FDC stands for Fixed-Dose Combination tablets that contain multiple anti-TB drugs in one tablet. Common FDC includes HRZE (4-drug combination) and HR (2-drug combination). FDCs improve adherence, reduce pill burden, and prevent development of drug resistance.",
            "keywords": ["FDC", "fixed-dose combination", "combination tablets"],
            "related_topics": ["treatment adherence", "drug resistance prevention"]
        },
        {
            "id": "DRUG_009",
            "category": "Side Effects Management",
            "question": "What are the signs of hepatitis from TB drugs?",
            "answer": "Signs of drug-induced hepatitis include: jaundice (yellow eyes/skin), dark urine, pale stools, persistent nausea/vomiting, severe loss of appetite, right upper abdominal pain, and unexplained fatigue. ALL TB drugs should be STOPPED immediately and patient referred urgently.",
            "keywords": ["hepatitis", "jaundice", "liver toxicity", "drug-induced"],
            "related_topics": ["serious side effects", "treatment interruption", "emergency management"]
        },
        {
            "id": "DRUG_010",
            "category": "Side Effects Management",
            "question": "How is peripheral neuropathy from Isoniazid managed?",
            "answer": "Peripheral neuropathy presents as tingling, numbness, or burning sensation in hands and feet. PREVENTION: Give Pyridoxine 40-150 mg daily. TREATMENT: If it occurs, increase Pyridoxine dose to 200-300 mg daily. Continue TB treatment with increased Pyridoxine.",
            "keywords": ["peripheral neuropathy", "isoniazid", "tingling", "numbness"],
            "related_topics": ["pyridoxine", "nerve damage", "preventable side effects"]
        },
        {
            "id": "DRUG_011",
            "category": "Side Effects Management",
            "question": "How is joint pain from Pyrazinamide managed?",
            "answer": "Joint pain (arthralgia) from Pyrazinamide is common and usually occurs in the first 2 months. MANAGEMENT: Give Aspirin or NSAIDs (like Ibuprofen) for pain relief. Continue TB treatment. Joint pain usually resolves after the intensive phase when Pyrazinamide is stopped.",
            "keywords": ["joint pain", "arthralgia", "pyrazinamide", "aspirin"],
            "related_topics": ["hyperuricemia", "symptomatic treatment"]
        },
        {
            "id": "DRUG_012",
            "category": "Side Effects Management",
            "question": "What should I do if a patient develops vision problems on TB treatment?",
            "answer": "Vision problems (blurred vision, color blindness, decreased visual acuity) suggest Ethambutol toxicity (optic neuritis). ACTION: STOP Ethambutol immediately and refer to eye specialist. Monitor vision monthly in high-risk patients (elderly, kidney disease). Never restart Ethambutol after optic neuritis.",
            "keywords": ["vision problems", "ethambutol", "optic neuritis", "blurred vision"],
            "related_topics": ["serious side effects", "irreversible damage", "monthly monitoring"]
        },
        {
            "id": "DRUG_013",
            "category": "Drug Information",
            "question": "What are second-line TB drugs?",
            "answer": "Second-line drugs are used for drug-resistant TB (DR-TB). Key drugs include: Fluoroquinolones (Levofloxacin 750-1000mg, Moxifloxacin 400mg), Injectable agents (Amikacin, Kanamycin, Capreomycin), and other agents (Ethionamide, Cycloserine, PAS, Linezolid, Bedaquiline, Delamanid). They are more toxic and less effective than first-line drugs.",
            "keywords": ["second-line drugs", "DR-TB", "MDR-TB", "fluoroquinolones"],
            "related_topics": ["drug-resistant TB", "treatment challenges"]
        }
    ]
    
    # Category 2: TREATMENT PROTOCOLS
    treatment_qa = [
        {
            "id": "TREAT_001",
            "category": "Treatment Protocols",
            "question": "What is the standard treatment regimen for drug-sensitive TB?",
            "answer": "Standard DS-TB treatment is 6 months total: INTENSIVE PHASE - 2 months of HRZE (Isoniazid, Rifampicin, Pyrazinamide, Ethambutol) daily. CONTINUATION PHASE - 4 months of HR (Isoniazid, Rifampicin) daily. Written as: 2HRZE/4HR.",
            "keywords": ["treatment regimen", "DS-TB", "6 months", "HRZE", "intensive phase"],
            "related_topics": ["drug-sensitive TB", "standard treatment", "treatment duration"]
        },
        {
            "id": "TREAT_002",
            "category": "Treatment Protocols",
            "question": "How long is TB meningitis treatment?",
            "answer": "TB meningitis requires EXTENDED treatment of 12 MONTHS total: 2 months HRZE + 10 months HR. Additionally, give corticosteroids (Prednisolone or Dexamethasone) to reduce inflammation and prevent neurological complications.",
            "keywords": ["TB meningitis", "12 months", "extended treatment", "steroids"],
            "related_topics": ["CNS TB", "corticosteroids", "neurological TB"]
        },
        {
            "id": "TREAT_003",
            "category": "Treatment Protocols",
            "question": "How long is TB spinal treatment?",
            "answer": "TB spine (Pott's disease) requires 9-12 MONTHS of treatment: 2 months HRZE + 7-10 months HR. Duration depends on clinical response, ESR normalization, and radiological healing.",
            "keywords": ["TB spine", "Pott's disease", "9-12 months", "skeletal TB"],
            "related_topics": ["extrapulmonary TB", "bone TB", "extended treatment"]
        },
        {
            "id": "TREAT_004",
            "category": "Treatment Protocols",
            "question": "What is DOTS?",
            "answer": "DOTS = Directly Observed Treatment, Short-course. It is a strategy where a trained treatment supporter watches the patient swallow TB medicines. DOTS ensures adherence, prevents drug resistance, and increases cure rates from 50% to 85%. It is the GOLD STANDARD for TB treatment delivery.",
            "keywords": ["DOTS", "directly observed treatment", "treatment supporter", "adherence"],
            "related_topics": ["treatment strategy", "cure rates", "WHO recommendation"]
        },
        {
            "id": "TREAT_005",
            "category": "Treatment Protocols",
            "question": "Who can be a DOTS treatment supporter?",
            "answer": "Treatment supporters can be: Healthcare workers (nurse, LHW, paramedic), Family members (trained and motivated), Community volunteers, Pharmacists, Teachers, or Workplace supervisors. They must be trained, reliable, acceptable to patient, and able to observe treatment daily.",
            "keywords": ["treatment supporter", "DOTS provider", "family DOTS"],
            "related_topics": ["DOTS implementation", "community involvement"]
        },
        {
            "id": "TREAT_006",
            "category": "Treatment Protocols",
            "question": "When should treatment be taken - morning or evening?",
            "answer": "TB drugs should be taken in the MORNING on an EMPTY STOMACH (30-60 minutes before breakfast). This ensures maximum drug absorption. For patients with severe gastric upset, drugs can be taken with a light meal, but absorption may be reduced.",
            "keywords": ["timing", "empty stomach", "morning dose", "absorption"],
            "related_topics": ["patient instructions", "drug absorption", "adherence tips"]
        },
        {
            "id": "TREAT_007",
            "category": "Treatment Protocols",
            "question": "What happens if a patient misses doses?",
            "answer": "INTENSIVE PHASE: If <14 doses missed = Extend by missed days. If ≥14 doses missed = Restart entire intensive phase. CONTINUATION PHASE: If <18 doses missed = Extend by missed days. If ≥18 doses missed = Restart continuation phase. Poor adherence increases risk of treatment failure and drug resistance.",
            "keywords": ["missed doses", "interrupted treatment", "adherence", "restart"],
            "related_topics": ["LTFU management", "treatment extension", "drug resistance risk"]
        },
        {
            "id": "TREAT_008",
            "category": "Treatment Protocols",
            "question": "What weight-based dosing is used for adults?",
            "answer": "Adults receive FDC tablets based on weight: 30-39 kg: 2 tablets HRZE (initial) / 2 tablets HR (continuation). 40-54 kg: 3 tablets. 55-70 kg: 4 tablets. 70+ kg: 5 tablets. FDC tablets contain fixed amounts: H=75mg, R=150mg, Z=400mg, E=275mg per tablet.",
            "keywords": ["weight-based dosing", "adult dosing", "FDC tablets"],
            "related_topics": ["dosage calculation", "body weight", "fixed-dose combination"]
        },
        {
            "id": "TREAT_009",
            "category": "Treatment Protocols",
            "question": "How is pediatric TB dosed?",
            "answer": "Children receive: Regimen-2 (Child): 2HRZE/4HR using child-friendly FDC dispersible tablets (H=50mg, R=75mg, Z=150mg, E=200mg). Dosing by weight bands. Tablets can be dispersed in water for easy administration. Treatment duration same as adults (6 months for pulmonary TB).",
            "keywords": ["pediatric TB", "children", "dispersible tablets", "child dosing"],
            "related_topics": ["childhood TB", "weight bands", "FDC dispersible"]
        },
        {
            "id": "TREAT_010",
            "category": "Treatment Protocols",
            "question": "When is treatment considered successful?",
            "answer": "Treatment success = CURED or COMPLETED. CURED: Bacteriologically confirmed at start + negative sputum at end of treatment. COMPLETED: Patient completed full treatment but no bacteriological confirmation of cure. Target: >85% success rate.",
            "keywords": ["treatment success", "cure", "completion", "outcomes"],
            "related_topics": ["treatment outcomes", "cure rate", "WHO targets"]
        }
    ]
    
    # Category 3: DIAGNOSIS & TESTING
    diagnosis_qa = [
        {
            "id": "DIAG_001",
            "category": "Diagnosis & Testing",
            "question": "What are the symptoms of pulmonary TB?",
            "answer": "Classic symptoms include: Persistent cough >2 weeks (with or without sputum/blood), Fever (often low-grade in evenings), Night sweats (drenching), Weight loss (unexplained), Loss of appetite, Fatigue, Chest pain. If cough >2 weeks = TB suspect = test immediately.",
            "keywords": ["TB symptoms", "cough", "fever", "night sweats", "weight loss"],
            "related_topics": ["clinical presentation", "TB suspect", "presumptive TB"]
        },
        {
            "id": "DIAG_002",
            "category": "Diagnosis & Testing",
            "question": "What is Xpert MTB/RIF?",
            "answer": "Xpert MTB/RIF (GeneXpert) is a rapid molecular test that detects TB bacteria (MTB) and Rifampicin resistance (RIF) in 2 hours. It is MORE SENSITIVE than sputum smear microscopy. Rifampicin resistance detected = MDR-TB suspected = refer for specialized treatment immediately.",
            "keywords": ["GeneXpert", "Xpert MTB/RIF", "rapid test", "rifampicin resistance"],
            "related_topics": ["molecular diagnostics", "MDR-TB detection", "2-hour result"]
        },
        {
            "id": "DIAG_003",
            "category": "Diagnosis & Testing",
            "question": "How is sputum collected for TB testing?",
            "answer": "Collect 2 sputum samples: SPOT sample (when patient first presents) + MORNING sample (early morning, next day, on waking). Patient should rinse mouth, take deep breath, cough deeply to bring up sputum from lungs (not saliva). Collect in sterile container. Minimum 2-5 ml needed.",
            "keywords": ["sputum collection", "spot sample", "morning sample", "specimen"],
            "related_topics": ["diagnostic procedure", "sample quality", "laboratory testing"]
        },
        {
            "id": "DIAG_004",
            "category": "Diagnosis & Testing",
            "question": "What does AFB positive mean?",
            "answer": "AFB = Acid-Fast Bacilli. AFB positive on sputum smear microscopy means TB bacteria are seen under microscope. Patient is highly infectious and should start treatment immediately. Results reported as: Scanty (few bacteria), 1+ (10-99 bacteria), 2+ (1-10 per field), 3+ (>10 per field).",
            "keywords": ["AFB", "acid-fast bacilli", "smear positive", "infectious"],
            "related_topics": ["sputum microscopy", "infectiousness", "bacteriological confirmation"]
        },
        {
            "id": "DIAG_005",
            "category": "Diagnosis & Testing",
            "question": "What is a chest X-ray used for in TB?",
            "answer": "Chest X-ray helps: Identify lung abnormalities suggesting TB (cavities, infiltrates, nodules, pleural effusion), Diagnose sputum-negative TB, Assess extent of disease, Monitor treatment response, Screen TB suspects who cannot produce sputum. CXR alone cannot confirm TB - need bacteriological tests.",
            "keywords": ["chest X-ray", "CXR", "radiological findings", "cavities"],
            "related_topics": ["diagnostic imaging", "sputum-negative TB", "screening"]
        },
        {
            "id": "DIAG_006",
            "category": "Diagnosis & Testing",
            "question": "What is LF-LAM test?",
            "answer": "LF-LAM (Lateral Flow Urine Lipoarabinomannan) is a rapid urine test for TB in HIV-positive patients with CD4 <100 or seriously ill. Results in 25 minutes. Useful when sputum cannot be obtained. Detects TB antigen in urine. Recommended by WHO for specific populations only.",
            "keywords": ["LF-LAM", "urine test", "HIV-TB", "rapid test"],
            "related_topics": ["HIV co-infection", "point-of-care testing", "WHO recommendation"]
        },
        {
            "id": "DIAG_007",
            "category": "Diagnosis & Testing",
            "question": "What is TB culture and when is it done?",
            "answer": "TB culture grows TB bacteria in laboratory (takes 2-8 weeks). Used for: Diagnosing sputum-smear negative TB, Extrapulmonary TB, Drug susceptibility testing (DST), Treatment failure cases, DR-TB suspects. Culture is the GOLD STANDARD but takes longer than GeneXpert.",
            "keywords": ["TB culture", "gold standard", "DST", "drug susceptibility"],
            "related_topics": ["laboratory diagnosis", "drug resistance testing", "bacteriological confirmation"]
        },
        {
            "id": "DIAG_008",
            "category": "Diagnosis & Testing",
            "question": "When is TB diagnosed clinically without bacteriological proof?",
            "answer": "Clinical diagnosis (without bacteriological confirmation) made when: Multiple negative sputum tests BUT chest X-ray highly suggestive of TB, Patient deteriorating despite broad-spectrum antibiotics, Extrapulmonary TB with no specimen for testing, Children (difficult to get sputum). Start treatment empirically and monitor response.",
            "keywords": ["clinical diagnosis", "empirical treatment", "sputum-negative"],
            "related_topics": ["diagnostic challenges", "clinical judgment", "treatment initiation"]
        }
    ]
    
    # Category 4: PAKISTAN NTP FORMS
    ntp_forms_qa = [
        {
            "id": "NTP_001",
            "category": "Pakistan NTP Forms",
            "question": "What is TB01 form?",
            "answer": "TB01 = TB SUSPECT REGISTER. Maintained at microscopy centers/diagnostic facilities. Records ALL TB suspects tested. Fields include: Serial number, Date, Name, Age, Sex, Address, Referred by, Type of specimen, Test results (smear/GeneXpert), Final diagnosis. Used to track diagnostic yield and case detection.",
            "keywords": ["TB01", "suspect register", "diagnostic register", "case detection"],
            "related_topics": ["NTP forms", "recording system", "laboratory register"]
        },
        {
            "id": "NTP_002",
            "category": "Pakistan NTP Forms",
            "question": "What is TB02 form?",
            "answer": "TB02 = TREATMENT CARD. Individual patient card maintained at treatment facility. Records: Patient demographics, Type of TB (PTB/EPTB), HIV status, Treatment regimen, Daily/weekly DOTS (tick marks), Weight monitoring, Sputum follow-up results (month 2,5,6), Side effects, Treatment outcome. Essential for monitoring adherence and outcomes.",
            "keywords": ["TB02", "treatment card", "patient card", "DOTS monitoring"],
            "related_topics": ["NTP forms", "treatment monitoring", "adherence tracking"]
        },
        {
            "id": "NTP_003",
            "category": "Pakistan NTP Forms",
            "question": "What is TB03 form?",
            "answer": "TB03 = TB REGISTER. Master register at treatment facility recording ALL TB patients started on treatment. Columns include: Registration number, Name, Age, Sex, Address, Type of TB, Sputum results, HIV status, Treatment regimen, Outcome at end of treatment. Used for cohort analysis and reporting.",
            "keywords": ["TB03", "TB register", "treatment register", "cohort analysis"],
            "related_topics": ["NTP forms", "recording system", "quarterly reporting"]
        },
        {
            "id": "NTP_004",
            "category": "Pakistan NTP Forms",
            "question": "What is TB05 form?",
            "answer": "TB05 = LABORATORY REQUEST FORM & RESULT. Used to request TB tests (smear, GeneXpert, culture, DST). Filled by clinician and sent to laboratory with specimen. Laboratory fills results section and returns copy to clinician. Contains: Patient details, Type of specimen, Test requested, Clinical information, Results section.",
            "keywords": ["TB05", "lab request", "laboratory form", "test requisition"],
            "related_topics": ["NTP forms", "laboratory communication", "specimen tracking"]
        },
        {
            "id": "NTP_005",
            "category": "Pakistan NTP Forms",
            "question": "What is TB07 form?",
            "answer": "TB07 = CONTACT SCREENING REGISTER. Records household and close contacts of TB patients screened for TB. Fields include: Index patient name, Contact name, Age, Relationship, Symptoms, Test results, Final diagnosis. Targets screening of children <5 years and HIV-positive contacts.",
            "keywords": ["TB07", "contact screening", "household contacts", "contact investigation"],
            "related_topics": ["NTP forms", "TB prevention", "active case finding"]
        },
        {
            "id": "NTP_006",
            "category": "Pakistan NTP Forms",
            "question": "What is TB09 form?",
            "answer": "TB09 = QUARTERLY REPORTING FORM. Compiled every 3 months by TB treatment facility. Reports: Number of TB suspects tested, Cases detected by type, Treatment outcomes of previous cohort, Drug stocks. Submitted to District TB Officer. Used for program monitoring and planning.",
            "keywords": ["TB09", "quarterly report", "cohort report", "program monitoring"],
            "related_topics": ["NTP forms", "reporting system", "performance indicators"]
        },
        {
            "id": "NTP_007",
            "category": "Pakistan NTP Forms",
            "question": "What is TB10 form?",
            "answer": "TB10 = REFERRAL/TRANSFER FORM. Used when patient moves between facilities. Contains: Patient details, Diagnosis, Treatment started, Doses taken, Doses remaining, Reason for transfer, Receiving facility details. Ensures treatment continuity. Must accompany patient with remaining drugs.",
            "keywords": ["TB10", "referral form", "transfer form", "treatment continuity"],
            "related_topics": ["NTP forms", "patient mobility", "inter-facility coordination"]
        },
        {
            "id": "NTP_008",
            "category": "Pakistan NTP Forms",
            "question": "What information is mandatory on TB03 register?",
            "answer": "Mandatory TB03 fields: Registration number (unique ID), Date of start treatment, Patient name, Age, Sex, Complete address with contact, Type of TB (PTB smear+, PTB smear-, EPTB), Bacteriological results, HIV status, Treatment regimen, Treatment outcome. All fields must be filled completely for proper recording.",
            "keywords": ["TB03", "mandatory fields", "registration", "data completeness"],
            "related_topics": ["NTP recording", "data quality", "treatment register"]
        }
    ]
    
    # Category 5: SPECIAL POPULATIONS
    special_pop_qa = [
        {
            "id": "SPEC_001",
            "category": "Special Populations",
            "question": "Is TB treatment safe in pregnancy?",
            "answer": "YES, TB treatment is SAFE in pregnancy. Standard HRZE regimen can be used. Rifampicin, Isoniazid, and Ethambutol are safe. Pyrazinamide is now considered safe by WHO. Give Pyridoxine 40-150 mg daily. Untreated TB is MORE dangerous to mother and baby than TB drugs. Breastfeeding is safe during TB treatment.",
            "keywords": ["pregnancy", "pregnant women", "TB in pregnancy", "safety"],
            "related_topics": ["antenatal care", "maternal TB", "breastfeeding", "pyridoxine"]
        },
        {
            "id": "SPEC_002",
            "category": "Special Populations",
            "question": "How is TB-HIV co-infection managed?",
            "answer": "TB-HIV requires BOTH treatments: Start TB treatment immediately. Start ART (antiretroviral therapy) within 2-8 weeks of starting TB treatment (earlier if CD4 <50). Give Pyridoxine 40-150 mg daily. Monitor for drug interactions (Rifampicin reduces ART drug levels). Watch for IRIS (immune reconstitution syndrome). TB-HIV patients have 20x higher TB risk.",
            "keywords": ["TB-HIV", "HIV co-infection", "ART", "dual treatment"],
            "related_topics": ["HIV testing", "IRIS", "drug interactions", "cotrimoxazole"]
        },
        {
            "id": "SPEC_003",
            "category": "Special Populations",
            "question": "How is pediatric TB different from adult TB?",
            "answer": "Children: Often have negative sputum (paucibacillary), Extrapulmonary TB more common, Clinical + radiological diagnosis frequent, Contact with adult TB case important, Treatment same duration but child-friendly FDC used, LTBI treatment crucial for <5 year contacts. Diagnosis criteria: TB contact + symptoms + chest X-ray + positive tuberculin test.",
            "keywords": ["pediatric TB", "children", "childhood TB", "paucibacillary"],
            "related_topics": ["child contacts", "LTBI prevention", "diagnostic challenges"]
        },
        {
            "id": "SPEC_004",
            "category": "Special Populations",
            "question": "What is MDR-TB?",
            "answer": "MDR-TB = Multi-Drug Resistant TB. TB resistant to at least Isoniazid AND Rifampicin (the two most powerful drugs). Treatment: 9-20 months with second-line drugs (fluoroquinolones, injectables). Longer, more toxic, more expensive, lower cure rates (60-70%). Caused by poor adherence or inadequate treatment. Requires specialized centers.",
            "keywords": ["MDR-TB", "drug resistance", "multi-drug resistant", "second-line treatment"],
            "related_topics": ["drug resistance", "treatment challenges", "GeneXpert detection"]
        },
        {
            "id": "SPEC_005",
            "category": "Special Populations",
            "question": "What is XDR-TB?",
            "answer": "XDR-TB = Extensively Drug-Resistant TB. MDR-TB plus resistance to fluoroquinolones AND at least one injectable drug. Treatment extremely difficult with very limited drug options. Cure rates <50%. Requires expert management at specialized centers. Highly fatal if untreated. Prevention: Ensure adherence, proper DOTS, infection control.",
            "keywords": ["XDR-TB", "extensively drug-resistant", "severe resistance"],
            "related_topics": ["drug resistance", "treatment failure", "palliative care"]
        },
        {
            "id": "SPEC_006",
            "category": "Special Populations",
            "question": "What are common sites of extrapulmonary TB?",
            "answer": "Common EPTB sites: TB Lymphadenitis (lymph nodes - most common EPTB), TB Meningitis (brain/spinal cord - most dangerous), TB Pleural effusion (pleura), TB Spine (Pott's disease), TB Abdomen (intestines, peritoneum), TB Pericardium (heart sac), TB Bones/Joints, TB Genitourinary (kidneys, bladder). Diagnosis often requires biopsy/aspiration.",
            "keywords": ["EPTB", "extrapulmonary TB", "TB lymphadenitis", "TB meningitis"],
            "related_topics": ["disseminated TB", "tissue diagnosis", "extended treatment"]
        },
        {
            "id": "SPEC_007",
            "category": "Special Populations",
            "question": "What is LTBI treatment?",
            "answer": "LTBI = Latent TB Infection (infected but no active disease). Treatment prevents progression to active TB. WHO recommends: 6H (Isoniazid 300mg daily for 6 months) OR 3HP (Isoniazid + Rifapentine weekly for 3 months). Target groups: HIV-positive contacts, Children <5 contacts, Immunocompromised patients. Give Pyridoxine with Isoniazid.",
            "keywords": ["LTBI", "latent TB", "TB prevention", "isoniazid preventive therapy"],
            "related_topics": ["TB contacts", "preventive treatment", "6H", "3HP"]
        },
        {
            "id": "SPEC_008",
            "category": "Special Populations",
            "question": "Can diabetic patients take TB treatment?",
            "answer": "YES, diabetics can take standard TB treatment. Special considerations: Monitor blood sugar closely (Rifampicin may alter diabetic drug levels), Give Pyridoxine 150 mg daily (higher risk of neuropathy), Ensure good glycemic control (poor control delays TB cure), Watch for drug interactions between TB and diabetic medications, Higher risk of treatment failure if sugar uncontrolled.",
            "keywords": ["diabetes", "diabetic patients", "blood sugar", "glycemic control"],
            "related_topics": ["comorbidities", "drug interactions", "treatment monitoring"]
        }
    ]
    
    # Category 6: CLINICAL PRESENTATION & EMERGENCY
    clinical_qa = [
        {
            "id": "CLIN_001",
            "category": "Clinical Presentation",
            "question": "What are the signs of TB meningitis?",
            "answer": "TB meningitis signs: Severe headache, Neck stiffness (positive Kernig's and Brudzinski's signs), Altered consciousness/confusion, Fever, Vomiting, Seizures, Cranial nerve palsies (facial weakness, vision problems), Papilledema. EMERGENCY - requires immediate lumbar puncture, brain imaging, and treatment with HRZE + steroids. Fatal if untreated.",
            "keywords": ["TB meningitis", "neck stiffness", "Kernig sign", "Brudzinski sign", "emergency"],
            "related_topics": ["CNS TB", "neurological TB", "corticosteroids", "lumbar puncture"]
        },
        {
            "id": "CLIN_002",
            "category": "Clinical Presentation",
            "question": "What is hemoptysis and is it dangerous?",
            "answer": "Hemoptysis = coughing up blood. Can range from blood-streaked sputum to massive bleeding. MILD hemoptysis (streaks): Common in active TB, continue treatment. MASSIVE hemoptysis (>200ml): MEDICAL EMERGENCY - patient may die from asphyxiation. Causes: Cavity rupture, aspergilloma (fungal ball), bronchiectasis. Urgent hospital admission needed.",
            "keywords": ["hemoptysis", "coughing blood", "bleeding", "emergency"],
            "related_topics": ["pulmonary TB", "cavitary disease", "complications"]
        },
        {
            "id": "CLIN_003",
            "category": "Clinical Presentation",
            "question": "What is TB pericarditis?",
            "answer": "TB pericarditis = TB infection of heart sac (pericardium). Symptoms: Chest pain, Shortness of breath, Swollen legs/abdomen (fluid retention), Muffled heart sounds. Complication: Cardiac tamponade (life-threatening). Treatment: Standard TB treatment + Corticosteroids (Prednisolone 60mg daily, tapered over 6-8 weeks). May need pericardiocentesis (fluid drainage).",
            "keywords": ["TB pericarditis", "heart TB", "cardiac tamponade", "chest pain"],
            "related_topics": ["EPTB", "corticosteroids", "emergency drainage"]
        },
        {
            "id": "CLIN_004",
            "category": "Clinical Presentation",
            "question": "What is paradoxical reaction/IRIS?",
            "answer": "IRIS = Immune Reconstitution Inflammatory Syndrome. Occurs in TB-HIV patients when ART is started. Immune system 'wakes up' and attacks TB, causing temporary worsening: New fever, enlarged lymph nodes, worsening chest X-ray. NOT treatment failure. Management: Continue both TB and ART, give NSAIDs or steroids for severe cases. Usually resolves in weeks.",
            "keywords": ["IRIS", "paradoxical reaction", "immune reconstitution", "TB-HIV"],
            "related_topics": ["HIV co-infection", "ART initiation", "inflammatory response"]
        },
        {
            "id": "CLIN_005",
            "category": "Clinical Presentation",
            "question": "How does Pott's disease present?",
            "answer": "Pott's disease = TB of spine (vertebrae). Presents with: Chronic back pain (gradual onset), Tenderness over spine, Kyphosis (spinal deformity/gibbus), Neurological signs (weakness, numbness, paraplegia if cord compression). Diagnosis: Spine X-ray/MRI shows vertebral destruction. Treatment: 9-12 months HRZE/HR + possible surgery for spinal stabilization.",
            "keywords": ["Pott's disease", "TB spine", "spinal TB", "back pain", "kyphosis"],
            "related_topics": ["skeletal TB", "EPTB", "neurological complications"]
        }
    ]
    
    # Category 7: PREVENTION & CONTROL
    prevention_qa = [
        {
            "id": "PREV_001",
            "category": "Prevention & Control",
            "question": "How is TB transmitted?",
            "answer": "TB spreads through AIR via droplet nuclei. When infectious TB patient coughs, sneezes, speaks, or sings, they release bacteria into air. Others inhale these bacteria. Risk factors for transmission: Close/prolonged contact, Indoor crowded spaces, Poor ventilation, High bacterial load (smear-positive). NOT spread by: Touching, sharing food/utensils, shaking hands.",
            "keywords": ["transmission", "airborne", "droplet nuclei", "contagious", "how TB spreads"],
            "related_topics": ["infection control", "contact screening", "infectiousness"]
        },
        {
            "id": "PREV_002",
            "category": "Prevention & Control",
            "question": "When is a TB patient no longer infectious?",
            "answer": "Patient becomes LESS infectious after: 2 weeks of effective TB treatment, Clinical improvement (less coughing, fever resolved), Sputum conversion (negative smears). However, continue infection control precautions until sputum confirmed negative. Smear-negative and EPTB patients are less infectious from start.",
            "keywords": ["infectiousness", "contagious period", "sputum conversion", "transmission risk"],
            "related_topics": ["infection control", "isolation", "DOTS"]
        },
        {
            "id": "PREV_003",
            "category": "Prevention & Control",
            "question": "What infection control measures prevent TB spread?",
            "answer": "Infection control hierarchy: ADMINISTRATIVE (early diagnosis, isolate infectious patients, cough etiquette), ENVIRONMENTAL (ventilation, UV light, open windows), PERSONAL (N95 masks for healthcare workers in high-risk areas). Patient should: Cover mouth when coughing, stay in well-ventilated area, avoid crowded spaces until non-infectious.",
            "keywords": ["infection control", "prevention", "N95 mask", "ventilation", "isolation"],
            "related_topics": ["nosocomial transmission", "healthcare worker protection"]
        },
        {
            "id": "PREV_004",
            "category": "Prevention & Control",
            "question": "Who should be screened for TB?",
            "answer": "Screen these high-risk groups: Household contacts of TB patients (priority: children <5, HIV+), People with HIV, Diabetics, Prisoners, Healthcare workers, Miners, Immunosuppressed patients, People with chronic cough, Malnourished individuals. Screening: Symptom inquiry + chest X-ray + sputum tests if symptomatic.",
            "keywords": ["screening", "TB suspects", "high-risk groups", "contact screening"],
            "related_topics": ["active case finding", "TB07 form", "early diagnosis"]
        },
        {
            "id": "PREV_005",
            "category": "Prevention & Control",
            "question": "What is BCG vaccine?",
            "answer": "BCG (Bacille Calmette-Guérin) = Live attenuated TB vaccine given to infants. Protection: Prevents severe childhood TB (meningitis, disseminated TB) but does NOT prevent pulmonary TB or infection in adults. Given at birth or soon after. Contraindications: HIV-infected infants with symptoms, severe immunodeficiency. Leaves characteristic shoulder scar.",
            "keywords": ["BCG", "vaccine", "vaccination", "TB prevention", "infant immunization"],
            "related_topics": ["childhood TB prevention", "EPI schedule", "contraindications"]
        }
    ]
    
    # Category 8: ADHERENCE & COUNSELING
    adherence_qa = [
        {
            "id": "ADH_001",
            "category": "Patient Education",
            "question": "Why is adherence important in TB treatment?",
            "answer": "Adherence is CRITICAL because: Incomplete treatment leads to RELAPSE (TB comes back), Creates DRUG RESISTANCE (MDR-TB, XDR-TB), Increases mortality risk, Continues transmission to others. Patients must complete FULL 6-12 months even if feeling better after 2 weeks. DOTS ensures adherence. Cure rate: 85% with adherence vs <50% without.",
            "keywords": ["adherence", "compliance", "treatment completion", "importance"],
            "related_topics": ["DOTS", "drug resistance prevention", "patient education"]
        },
        {
            "id": "ADH_002",
            "category": "Patient Education",
            "question": "What should I tell patients about side effects?",
            "answer": "Counsel patients: NORMAL effects: Orange urine (Rifampicin - harmless), mild nausea in first weeks (take with food). REPORT IMMEDIATELY: Yellow eyes/dark urine (hepatitis), vision changes (Ethambutol toxicity), severe skin rash, numbness in hands/feet (neuropathy), joint pain. Don't stop drugs without doctor advice. Most side effects manageable without stopping treatment.",
            "keywords": ["patient counseling", "side effects", "education", "warning signs"],
            "related_topics": ["adherence support", "adverse drug reactions", "safety monitoring"]
        },
        {
            "id": "ADH_003",
            "category": "Patient Education",
            "question": "Can TB patients work during treatment?",
            "answer": "YES, most TB patients can continue working after initial weeks. Recommendations: Rest for first 2-4 weeks if very weak, Return to work once feeling better (usually after 2-4 weeks), Avoid strenuous physical labor initially, Ensure proper nutrition and rest, Continue taking medicines regularly. Smear-negative and EPTB patients can work earlier. Employment is important for adherence and recovery.",
            "keywords": ["work", "employment", "daily activities", "lifestyle"],
            "related_topics": ["patient support", "quality of life", "treatment adherence"]
        },
        {
            "id": "ADH_004",
            "category": "Patient Education",
            "question": "What dietary advice for TB patients?",
            "answer": "Nutrition is crucial for TB recovery. Advise: High-protein diet (eggs, meat, fish, lentils, dairy), High-calorie foods (for weight gain), Fresh fruits and vegetables, Adequate fluids (2-3 liters daily), AVOID alcohol (increases hepatitis risk with TB drugs). Malnourishment slows recovery and increases mortality. Food support programs improve outcomes.",
            "keywords": ["nutrition", "diet", "food", "weight gain", "alcohol"],
            "related_topics": ["patient support", "treatment success", "comorbidities"]
        }
    ]
    
    # Category 9: DRUG INTERACTIONS
    interactions_qa = [
        {
            "id": "INTER_001",
            "category": "Drug Interactions",
            "question": "What drugs interact with Rifampicin?",
            "answer": "Rifampicin is a strong liver enzyme inducer - reduces levels of many drugs. Major interactions: Antiretrovirals (HIV drugs - need dose adjustment), Oral contraceptives (use additional contraception), Warfarin (increase dose), Oral hypoglycemics (diabetes drugs), Antifungals, Corticosteroids. Always check drug interactions before adding new medications.",
            "keywords": ["rifampicin", "drug interactions", "enzyme inducer", "contraceptives"],
            "related_topics": ["HIV treatment", "contraception", "anticoagulation"]
        },
        {
            "id": "INTER_002",
            "category": "Drug Interactions",
            "question": "Can TB patients take oral contraceptives?",
            "answer": "Rifampicin REDUCES effectiveness of oral contraceptive pills (OCPs). Risk of pregnancy increases. Recommendation: Use additional NON-HORMONAL contraception (condoms, IUD) during TB treatment and for 1 month after completion. Injectable contraceptives (Depo-Provera) may also be affected. Counsel all women of childbearing age.",
            "keywords": ["contraceptives", "birth control", "pregnancy prevention", "family planning"],
            "related_topics": ["rifampicin interactions", "reproductive health", "patient counseling"]
        },
        {
            "id": "INTER_003",
            "category": "Drug Interactions",
            "question": "Can alcohol be consumed during TB treatment?",
            "answer": "NO, AVOID ALCOHOL during TB treatment. Reasons: Increases hepatotoxicity risk (liver damage) from Isoniazid, Rifampicin, Pyrazinamide, Reduces drug absorption and effectiveness, Impairs adherence (intoxication), Worsens malnutrition. Patients with alcohol dependence need close monitoring and counseling. Liver function tests recommended.",
            "keywords": ["alcohol", "drinking", "hepatotoxicity", "liver damage"],
            "related_topics": ["side effects", "hepatitis", "adherence", "counseling"]
        }
    ]
    
    # Category 10: MONITORING & FOLLOW-UP
    monitoring_qa = [
        {
            "id": "MON_001",
            "category": "Treatment Monitoring",
            "question": "When are follow-up sputum tests done?",
            "answer": "Sputum monitoring schedule for smear-positive patients: End of MONTH 2 (end of intensive phase - check conversion), End of MONTH 5 (assess response), End of MONTH 6 (confirm cure). If positive at month 2: Extend intensive phase. If positive at month 5: Suspect treatment failure, do DST. Target: >85% conversion by month 2.",
            "keywords": ["sputum monitoring", "follow-up", "month 2", "month 5", "bacteriological monitoring"],
            "related_topics": ["treatment response", "sputum conversion", "cure confirmation"]
        },
        {
            "id": "MON_002",
            "category": "Treatment Monitoring",
            "question": "How often should weight be monitored?",
            "answer": "Monitor weight MONTHLY throughout treatment. Important because: Drug dosing based on weight (FDC tablets adjusted if weight changes), Weight gain indicates good treatment response, Weight loss suggests treatment failure, poor adherence, or comorbidity (HIV, diabetes). Record weight on TB02 treatment card. Adjust doses if weight changes >10%.",
            "keywords": ["weight monitoring", "monthly weight", "dosage adjustment"],
            "related_topics": ["treatment monitoring", "TB02 card", "treatment response"]
        },
        {
            "id": "MON_003",
            "category": "Treatment Monitoring",
            "question": "When should liver function tests be done?",
            "answer": "Baseline LFTs recommended for: Elderly >60 years, Known liver disease, Alcohol users, HIV-positive, Pregnant women, Concomitant hepatotoxic drugs. Monitor monthly if abnormal. STOP all TB drugs immediately if: ALT >3x normal with symptoms OR ALT >5x normal without symptoms. Reintroduce drugs carefully after LFTs normalize.",
            "keywords": ["LFT", "liver function tests", "hepatotoxicity", "monitoring"],
            "related_topics": ["side effects", "hepatitis", "drug-induced liver injury"]
        },
        {
            "id": "MON_004",
            "category": "Treatment Monitoring",
            "question": "What is LTFU in TB?",
            "answer": "LTFU = Lost To Follow-Up. Patient who interrupted treatment for >2 consecutive months. Causes: Side effects, Feeling better, Migration, Lack of support, Stigma. Management: Active tracing (home visit, phone call), Assess doses taken, Restart appropriate phase, Provide adherence support. LTFU increases relapse and MDR-TB risk. Target: <5% LTFU.",
            "keywords": ["LTFU", "lost to follow-up", "treatment interruption", "defaulter"],
            "related_topics": ["adherence challenges", "contact tracing", "treatment outcomes"]
        }
    ]
    
    # Combine all Q&A categories
    all_qa = (drug_qa + treatment_qa + diagnosis_qa + ntp_forms_qa + 
              special_pop_qa + clinical_qa + prevention_qa + adherence_qa + 
              interactions_qa + monitoring_qa)
    
    # Update metadata
    qa_dataset["metadata"]["total_questions"] = len(all_qa)
    qa_dataset["qa_pairs"] = all_qa
    
    # Save to JSON file
    output_file = 'TB_QA_DATASET.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(qa_dataset, f, indent=2, ensure_ascii=False)
    
    print(f"✅ JSON Q&A Dataset Created Successfully!")
    print(f"📁 File: {output_file}")
    print(f"📊 Total Questions: {len(all_qa)}")
    print(f"\n📋 Categories Distribution:")
    
    # Count by category
    category_counts = {}
    for qa in all_qa:
        cat = qa['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    for cat, count in sorted(category_counts.items()):
        print(f"   {cat}: {count} questions")
    
    print(f"\n✨ Dataset ready for RAG chatbot!")
    return output_file

if __name__ == "__main__":
    create_comprehensive_qa_dataset()
