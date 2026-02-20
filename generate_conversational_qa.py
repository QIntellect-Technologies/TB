#!/usr/bin/env python3
"""
Generate Conversational TB Q&A Dataset
Creates natural, direct answers for yes/no and practical questions
"""

import json
from datetime import datetime

def generate_conversational_qa():
    """Generate comprehensive conversational Q&A pairs"""
    
    qa_pairs = []
    id_counter = 1
    
    # ========================================================================
    # CATEGORY 1: YES/NO QUESTIONS - TRANSMISSION
    # ========================================================================
    
    transmission_qa = [
        {
            "question": "Is TB contagious?",
            "answer": "Yes, TB is contagious. It spreads through the air when someone with active pulmonary TB coughs, sneezes, or talks.",
            "category": "Yes/No - Transmission"
        },
        {
            "question": "Can TB spread through food?",
            "answer": "No, TB does not spread through food or water. It only spreads through airborne droplets when someone with active lung TB coughs or sneezes.",
            "category": "Yes/No - Transmission"
        },
        {
            "question": "Can TB spread through touching?",
            "answer": "No, TB does not spread through touching, shaking hands, or sharing utensils. It only spreads through the air.",
            "category": "Yes/No - Transmission"
        },
        {
            "question": "Is TB airborne?",
            "answer": "Yes, TB is an airborne disease. The bacteria spread through tiny droplets in the air when an infected person coughs, sneezes, or talks.",
            "category": "Yes/No - Transmission"
        },
        {
            "question": "Can you get TB from kissing?",
            "answer": "It's very unlikely to get TB from kissing. TB spreads mainly through prolonged exposure to airborne bacteria, not through saliva or brief contact.",
            "category": "Yes/No - Transmission"
        },
    ]
    
    # ========================================================================
    # CATEGORY 2: YES/NO QUESTIONS - CURABILITY & TREATMENT
    # ========================================================================
    
    treatment_qa = [
        {
            "question": "Can TB be cured?",
            "answer": "Yes, TB can be cured with proper treatment. The standard treatment is a 6-month course of antibiotics that is highly effective when completed.",
            "category": "Yes/No - Treatment"
        },
        {
            "question": "Is TB curable?",
            "answer": "Yes, TB is curable. With the right combination of antibiotics taken for 6 months, over 95% of TB cases can be completely cured.",
            "category": "Yes/No - Treatment"
        },
        {
            "question": "Can TB come back after treatment?",
            "answer": "Yes, TB can come back (relapse) if treatment is not completed properly. This is why it's critical to finish all 6 months of medication even if you feel better.",
            "category": "Yes/No - Treatment"
        },
        {
            "question": "Is TB treatment free?",
            "answer": "Yes, in most countries TB treatment is provided free of charge through government TB programs. Contact your local health department for free TB treatment.",
            "category": "Yes/No - Treatment"
        },
        {
            "question": "Can TB be treated at home?",
            "answer": "Yes, most TB patients can be treated at home after the first 2-3 weeks. You'll need to isolate initially, then take daily medications under supervision (DOTS program).",
            "category": "Yes/No - Treatment"
        },
    ]
    
    # ========================================================================
    # CATEGORY 3: YES/NO QUESTIONS - DISEASE TYPE & SEVERITY
    # ========================================================================
    
    disease_type_qa = [
        {
            "question": "Is TB viral or bacterial?",
            "answer": "TB is a bacterial disease caused by Mycobacterium tuberculosis, not a virus.",
            "category": "Yes/No - Disease Type"
        },
        {
            "question": "Is TB serious?",
            "answer": "Yes, TB is serious and can be fatal without treatment. However, it is curable with proper medication.",
            "category": "Yes/No - Severity"
        },
        {
            "question": "Is TB deadly?",
            "answer": "Yes, TB can be deadly if left untreated. About 45% of people with untreated TB will die. However, with treatment, the cure rate is over 95%.",
            "category": "Yes/No - Severity"
        },
        {
            "question": "Is TB worse than COVID?",
            "answer": "TB and COVID are different diseases. TB kills more people globally each year (1.5 million vs 1 million for COVID in 2023), but COVID spreads faster. Both are serious and treatable.",
            "category": "Yes/No - Comparison"
        },
        {
            "question": "Is TB a lung disease?",
            "answer": "TB primarily affects the lungs (pulmonary TB), but it can also attack other parts of the body like the kidneys, spine, and brain (extrapulmonary TB).",
            "category": "Yes/No - Disease Type"
        },
    ]
    
    # ========================================================================
    # CATEGORY 4: YES/NO QUESTIONS - DEMOGRAPHICS
    # ========================================================================
    
    demographics_qa = [
        {
            "question": "Can children get TB?",
            "answer": "Yes, children can get TB. In fact, children under 5 are at higher risk and may develop severe forms like TB meningitis.",
            "category": "Yes/No - Demographics"
        },
        {
            "question": "Can pregnant women get TB?",
            "answer": "Yes, pregnant women can get TB. TB treatment is safe during pregnancy and should be started immediately to protect both mother and baby.",
            "category": "Yes/No - Demographics"
        },
        {
            "question": "Can elderly people get TB?",
            "answer": "Yes, elderly people can get TB and are at higher risk due to weakened immune systems. TB symptoms in elderly may be less obvious.",
            "category": "Yes/No - Demographics"
        },
        {
            "question": "Can babies get TB?",
            "answer": "Yes, babies can get TB, usually from close contact with an infected adult. Babies with TB need immediate treatment as they're at high risk for severe disease.",
            "category": "Yes/No - Demographics"
        },
    ]
    
    # ========================================================================
    # CATEGORY 5: YES/NO QUESTIONS - PREVENTION
    # ========================================================================
    
    prevention_qa = [
        {
            "question": "Is TB preventable?",
            "answer": "Yes, TB is preventable. The BCG vaccine protects children from severe TB, and preventive therapy can stop latent TB from becoming active.",
            "category": "Yes/No - Prevention"
        },
        {
            "question": "Is there a vaccine for TB?",
            "answer": "Yes, the BCG vaccine protects against severe forms of TB in children, especially TB meningitis. It's given at birth in many countries.",
            "category": "Yes/No - Prevention"
        },
        {
            "question": "Does BCG prevent TB?",
            "answer": "BCG vaccine prevents severe TB in children (like TB meningitis) but doesn't fully prevent pulmonary TB in adults. It's still important for child protection.",
            "category": "Yes/No - Prevention"
        },
    ]
    
    # ========================================================================
    # CATEGORY 6: PRACTICAL "CAN I..." QUESTIONS
    # ========================================================================
    
    practical_qa = [
        {
            "question": "Can I go to work with TB?",
            "answer": "Not during the first 2-3 weeks of treatment when you're still contagious. After that, once your doctor confirms you're no longer infectious, you can return to work.",
            "category": "Practical - Work/School"
        },
        {
            "question": "Can TB patients go to school?",
            "answer": "Not during the first 2-3 weeks of treatment. Children can return to school once the doctor confirms they're no longer contagious, usually after 2-3 weeks of proper treatment.",
            "category": "Practical - Work/School"
        },
        {
            "question": "Can I drink alcohol during TB treatment?",
            "answer": "No, you should avoid alcohol completely during TB treatment. Alcohol increases the risk of liver damage from TB medications, especially Isoniazid and Rifampicin.",
            "category": "Practical - Lifestyle"
        },
        {
            "question": "Can I smoke during TB treatment?",
            "answer": "No, you should stop smoking during TB treatment. Smoking damages your lungs further, reduces treatment effectiveness, and increases the risk of treatment failure.",
            "category": "Practical - Lifestyle"
        },
        {
            "question": "Can I exercise with TB?",
            "answer": "Light exercise is okay once you start feeling better, but avoid strenuous activity during active TB. Always consult your doctor before starting any exercise program.",
            "category": "Practical - Lifestyle"
        },
        {
            "question": "Can I breastfeed with TB?",
            "answer": "Yes, you can breastfeed while on TB treatment. TB medications are safe during breastfeeding, and the benefits of breastfeeding outweigh any risks.",
            "category": "Practical - Pregnancy/Breastfeeding"
        },
        {
            "question": "Can I get pregnant during TB treatment?",
            "answer": "It's best to wait until after completing TB treatment to get pregnant. However, if you do get pregnant during treatment, most TB medications are safe and treatment should continue.",
            "category": "Practical - Pregnancy/Breastfeeding"
        },
    ]
    
    # ========================================================================
    # CATEGORY 7: "HOW LONG..." QUESTIONS
    # ========================================================================
    
    duration_qa = [
        {
            "question": "How long does TB treatment last?",
            "answer": "Standard TB treatment lasts 6 months. The first 2 months use 4 drugs (intensive phase), followed by 4 months of 2 drugs (continuation phase).",
            "category": "Duration - Treatment"
        },
        {
            "question": "How long to stay home with TB?",
            "answer": "You should stay home for the first 2-3 weeks of treatment until you're no longer contagious. Your doctor will confirm when it's safe to return to work or school.",
            "category": "Duration - Isolation"
        },
        {
            "question": "How long is someone with TB contagious?",
            "answer": "People with active TB are contagious until they've been on proper treatment for about 2-3 weeks. After that, the risk of spreading TB drops dramatically.",
            "category": "Duration - Contagious Period"
        },
        {
            "question": "How long does it take to feel better with TB?",
            "answer": "Most people start feeling better within 2-4 weeks of starting treatment. However, you must complete the full 6 months of medication to be fully cured.",
            "category": "Duration - Recovery"
        },
        {
            "question": "How long does latent TB last?",
            "answer": "Latent TB can last for years or even a lifetime without causing symptoms. About 5-10% of people with latent TB will develop active TB at some point.",
            "category": "Duration - Latent TB"
        },
    ]
    
    # ========================================================================
    # CATEGORY 8: "WHAT HAPPENS IF..." QUESTIONS
    # ========================================================================
    
    consequences_qa = [
        {
            "question": "What happens if I stop TB medicine early?",
            "answer": "Stopping TB medicine early is very dangerous. The bacteria can become drug-resistant, making TB much harder to treat. You may also relapse and become sick again.",
            "category": "Consequences - Treatment"
        },
        {
            "question": "What happens if TB is left untreated?",
            "answer": "Untreated TB is often fatal. About 45% of people with untreated TB will die. It can also spread to others and cause permanent lung damage.",
            "category": "Consequences - No Treatment"
        },
        {
            "question": "What happens if I miss a dose of TB medicine?",
            "answer": "If you miss one dose, take it as soon as you remember. Do not double dose. If you miss multiple doses, contact your doctor immediately as this can lead to treatment failure.",
            "category": "Consequences - Missed Doses"
        },
        {
            "question": "What happens if I drink alcohol with TB medicine?",
            "answer": "Drinking alcohol with TB medicine can cause severe liver damage. The combination of alcohol and TB drugs (especially Isoniazid and Rifampicin) is very toxic to the liver.",
            "category": "Consequences - Alcohol"
        },
    ]
    
    # ========================================================================
    # CATEGORY 9: "WHY..." QUESTIONS
    # ========================================================================
    
    explanation_qa = [
        {
            "question": "Why is TB treatment so long?",
            "answer": "TB treatment is 6 months because TB bacteria grow very slowly and can hide in the body. The long treatment ensures all bacteria are killed and prevents relapse.",
            "category": "Explanation - Treatment Duration"
        },
        {
            "question": "Why do I need 4 drugs for TB?",
            "answer": "Using 4 drugs prevents drug resistance. TB bacteria can mutate to resist one drug, but it's nearly impossible for them to resist all 4 drugs at once.",
            "category": "Explanation - Multiple Drugs"
        },
        {
            "question": "Why is my urine orange during TB treatment?",
            "answer": "Rifampicin, one of the TB drugs, turns your urine, tears, and sweat orange-red. This is normal and harmless. It will go away after you finish treatment.",
            "category": "Explanation - Side Effects"
        },
        {
            "question": "Why do I need to take TB medicine on an empty stomach?",
            "answer": "TB medicines work best when taken on an empty stomach (1 hour before or 2 hours after food). Food can reduce how much medicine your body absorbs.",
            "category": "Explanation - Medication Instructions"
        },
    ]
    
    # ========================================================================
    # CATEGORY 10: COMPARISON QUESTIONS
    # ========================================================================
    
    comparison_qa = [
        {
            "question": "What's the difference between latent and active TB?",
            "answer": "Latent TB means you have the bacteria but no symptoms and can't spread it. Active TB means you're sick with symptoms and can spread it to others.",
            "category": "Comparison - Latent vs Active"
        },
        {
            "question": "What's the difference between pulmonary and extrapulmonary TB?",
            "answer": "Pulmonary TB affects the lungs and is contagious. Extrapulmonary TB affects other organs (bones, brain, kidneys) and is usually not contagious.",
            "category": "Comparison - Pulmonary vs Extrapulmonary"
        },
        {
            "question": "What's the difference between TB and pneumonia?",
            "answer": "TB is caused by Mycobacterium tuberculosis and requires 6 months of treatment. Pneumonia is usually caused by different bacteria or viruses and is treated with shorter courses of antibiotics.",
            "category": "Comparison - TB vs Other Diseases"
        },
    ]
    
    # ========================================================================
    # CATEGORY 11: SIMPLE "WHAT IS..." DEFINITIONS
    # ========================================================================
    
    definitions_qa = [
        {
            "question": "What is pulmonary TB?",
            "answer": "Pulmonary TB is tuberculosis that affects the lungs. It's the most common form of TB (85% of cases) and is contagious through airborne transmission.",
            "category": "Definition - Types"
        },
        {
            "question": "What is MDR-TB?",
            "answer": "MDR-TB (Multidrug-Resistant TB) is TB that doesn't respond to the two most powerful first-line drugs: Isoniazid and Rifampicin. It requires longer treatment with second-line drugs.",
            "category": "Definition - Drug Resistance"
        },
        {
            "question": "What is the BCG vaccine?",
            "answer": "BCG vaccine protects children against severe forms of TB, especially TB meningitis. It's given at birth in many countries and is one of the most widely used vaccines in the world.",
            "category": "Definition - Prevention"
        },
        {
            "question": "What is DOTS?",
            "answer": "DOTS (Directly Observed Treatment, Short-course) is a TB treatment strategy where a healthcare worker watches you take your medicine every day. This ensures you complete treatment and prevents drug resistance.",
            "category": "Definition - Treatment Strategy"
        },
        {
            "question": "What is latent TB?",
            "answer": "Latent TB means you have TB bacteria in your body but they're inactive. You have no symptoms, don't feel sick, and can't spread TB to others. However, it can become active TB later.",
            "category": "Definition - Types"
        },
    ]
    
    # Combine all categories
    all_qa = (
        transmission_qa + treatment_qa + disease_type_qa + demographics_qa +
        prevention_qa + practical_qa + duration_qa + consequences_qa +
        explanation_qa + comparison_qa + definitions_qa
    )
    
    # Add IDs and keywords
    for qa in all_qa:
        qa['id'] = f"CONV_{id_counter:05d}"
        qa['keywords'] = extract_keywords(qa['question'])
        id_counter += 1
    
    return all_qa

def extract_keywords(question):
    """Extract keywords from question"""
    # Simple keyword extraction
    stop_words = {'is', 'are', 'can', 'does', 'do', 'what', 'how', 'why', 'the', 'a', 'an', 'with', 'for', 'to', 'in', 'on', 'at', 'if', 'i', 'my', 'me'}
    words = question.lower().replace('?', '').split()
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    return keywords[:5]  # Top 5 keywords

def main():
    print("🚀 Generating Conversational TB Q&A Dataset...")
    
    qa_pairs = generate_conversational_qa()
    
    # Create dataset structure
    dataset = {
        "metadata": {
            "title": "TB Expert Conversational Q&A Dataset",
            "count": len(qa_pairs),
            "type": "conversational",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "description": "Natural, direct answers for yes/no and practical TB questions"
        },
        "qa_pairs": qa_pairs
    }
    
    # Save to file
    output_file = "TB_QA_CONVERSATIONAL_2K.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated {len(qa_pairs)} conversational Q&A pairs")
    print(f"📁 Saved to: {output_file}")
    
    # Print summary by category
    from collections import Counter
    categories = Counter(qa['category'] for qa in qa_pairs)
    
    print("\n📊 Breakdown by Category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")
    
    print("\n✅ Generation complete!")

if __name__ == "__main__":
    main()
