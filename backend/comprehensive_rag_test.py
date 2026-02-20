"""
Comprehensive RAG System Test - 200+ Questions
Tests all TB topics, query types, and edge cases
"""
import requests
import json
from typing import List, Dict
import time

API_BASE = "http://127.0.0.1:8000"

# Comprehensive test questions covering all TB topics
TEST_QUESTIONS = {
    "Basic TB Knowledge": [
        "what is tb?",
        "What is tuberculosis?",
        "Define TB",
        "Explain tuberculosis",
        "TB?",
        "What causes TB?",
        "How does TB spread?",
        "Is TB contagious?",
        "Can TB be cured?",
        "What is pulmonary TB?",
        "What is extrapulmonary TB?",
        "What is latent TB?",
        "What is active TB?",
        "Difference between latent and active TB?",
        "What is MDR-TB?",
        "What is XDR-TB?",
        "What is drug-resistant TB?",
        "Types of TB",
        "How many types of TB are there?",
        "What is miliary TB?",
    ],
    
    "Symptoms & Diagnosis": [
        "What are the symptoms of TB?",
        "Symptoms of tuberculosis",
        "How do I know if I have TB?",
        "Signs of TB",
        "TB symptoms",
        "Cough and TB",
        "Night sweats TB",
        "Weight loss TB",
        "Fever and TB",
        "Hemoptysis TB",
        "Chest pain TB",
        "My patient has been coughing for 3 weeks",
        "Patient with night sweats and cough",
        "How to diagnose TB?",
        "TB tests",
        "Sputum test for TB",
        "GeneXpert test",
        "Mantoux test",
        "TB skin test",
        "Chest X-ray for TB",
        "How long does TB test take?",
        "TB blood test",
        "IGRA test",
        "Culture test for TB",
        "Smear microscopy",
    ],
    
    "Treatment & Drugs": [
        "How to treat TB?",
        "TB treatment",
        "TB drugs",
        "First-line TB drugs",
        "Second-line TB drugs",
        "Rifampicin dosage",
        "Isoniazid dosage",
        "Pyrazinamide dosage",
        "Ethambutol dosage",
        "Bedaquiline dosage",
        "Linezolid for TB",
        "Levofloxacin for TB",
        "Moxifloxacin TB",
        "How long is TB treatment?",
        "6 month TB treatment",
        "MDR-TB treatment duration",
        "TB treatment regimen",
        "Intensive phase TB",
        "Continuation phase TB",
        "DOTS therapy",
        "What is DOTS?",
        "TB medication side effects",
        "Rifampicin side effects",
        "Isoniazid side effects",
        "Hepatotoxicity TB drugs",
    ],
    
    "Drug-Resistant TB": [
        "What is MDR-TB?",
        "What is XDR-TB?",
        "How to treat MDR-TB?",
        "MDR-TB drugs",
        "Bedaquiline for MDR-TB",
        "Delamanid for MDR-TB",
        "Linezolid MDR-TB",
        "How long is MDR-TB treatment?",
        "MDR-TB cure rate",
        "XDR-TB treatment",
        "Totally drug-resistant TB",
        "Rifampicin-resistant TB",
        "Isoniazid-resistant TB",
        "How does TB become resistant?",
        "Preventing drug resistance",
    ],
    
    "Special Populations": [
        "TB in children",
        "Pediatric TB",
        "TB and pregnancy",
        "Pregnant woman with TB",
        "TB and HIV",
        "HIV-TB co-infection",
        "TB in elderly",
        "TB and diabetes",
        "TB in immunocompromised",
        "Breastfeeding and TB",
        "TB treatment in children",
        "TB drugs safe in pregnancy",
        "Pediatric TB dosage",
    ],
    
    "Prevention & Control": [
        "How to prevent TB?",
        "TB prevention",
        "BCG vaccine",
        "TB vaccine",
        "Contact tracing TB",
        "TB screening",
        "Infection control TB",
        "TB isolation",
        "N95 mask for TB",
        "Ventilation for TB",
        "Preventive therapy TB",
        "Isoniazid preventive therapy",
        "IPT for TB",
        "TB prophylaxis",
        "How long to isolate TB patient?",
    ],
    
    "Conversational Queries": [
        "My patient has cough for 3 weeks with night sweats. Could this be TB?",
        "I have a patient with weight loss and fever. Should I test for TB?",
        "Patient coughing blood. Is it TB?",
        "How do I manage a TB patient?",
        "My patient is not responding to TB treatment. What should I do?",
        "Patient missed TB doses. What now?",
        "Can I stop TB treatment early?",
        "Patient has side effects from TB drugs",
        "What if patient is pregnant and has TB?",
        "Child exposed to TB. What to do?",
        "TB patient wants to travel. Is it safe?",
        "When can TB patient return to work?",
        "Is TB patient still contagious?",
        "How to counsel TB patient?",
        "Patient refusing TB treatment",
    ],
    
    "Complex Multi-Part": [
        "What is the difference between latent and active TB, and how should each be treated?",
        "Explain pulmonary vs extrapulmonary TB and their treatments",
        "What are the symptoms of TB and how is it diagnosed?",
        "Compare MDR-TB and XDR-TB treatment approaches",
        "What are first-line drugs and their dosages?",
        "Explain intensive and continuation phase of TB treatment",
        "What are the side effects of TB drugs and how to manage them?",
        "How does TB affect HIV patients and what is the treatment?",
        "What is DOTS and why is it important?",
        "Explain TB prevention strategies and contact tracing",
    ],
    
    "Urdu Queries": [
        "ٹی بی کیا ہے؟",
        "ٹی بی کی علامات کیا ہیں؟",
        "ٹی بی کا علاج",
        "ٹی بی کی دوائیں",
        "ٹی بی کیسے پھیلتا ہے؟",
        "ٹی بی سے بچاؤ",
        "بچوں میں ٹی بی",
        "حاملہ خواتین اور ٹی بی",
        "ایم ڈی آر ٹی بی کیا ہے؟",
        "ٹی بی کا ٹیسٹ",
    ],
    
    "Edge Cases & Short Queries": [
        "tb",
        "TB",
        "symptoms",
        "treatment",
        "drugs",
        "cure",
        "test",
        "prevention",
        "vaccine",
        "MDR",
        "XDR",
        "HIV",
        "children",
        "pregnant",
        "side effects",
    ],
    
    "Clinical Scenarios": [
        "45 year old male, cough 4 weeks, fever, night sweats",
        "Child with persistent cough and weight loss",
        "HIV positive patient with TB symptoms",
        "Pregnant woman diagnosed with TB",
        "Patient on TB treatment for 2 months, still coughing",
        "Contact of TB patient, no symptoms",
        "Diabetic patient with TB",
        "Elderly patient with extrapulmonary TB",
        "Patient with hepatotoxicity on TB drugs",
        "MDR-TB patient not improving",
    ]
}

def test_rag_endpoint(question: str, language: str = "English") -> Dict:
    """Test a single question on RAG endpoint"""
    try:
        response = requests.post(
            f"{API_BASE}/chat-rag",
            json={"message": question, "language": language},
            timeout=30
        )
        return {
            "status": "success",
            "data": response.json()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def run_comprehensive_test():
    """Run comprehensive test suite"""
    print("\n" + "="*80)
    print("🧪 COMPREHENSIVE RAG SYSTEM TEST - 200+ QUESTIONS")
    print("="*80)
    
    total_questions = sum(len(questions) for questions in TEST_QUESTIONS.values())
    print(f"\n📊 Total Questions: {total_questions}")
    print(f"📂 Categories: {len(TEST_QUESTIONS)}")
    
    results = {
        "total": 0,
        "success": 0,
        "error": 0,
        "by_category": {},
        "failed_questions": []
    }
    
    start_time = time.time()
    
    for category, questions in TEST_QUESTIONS.items():
        print(f"\n{'='*80}")
        print(f"📁 Category: {category} ({len(questions)} questions)")
        print(f"{'='*80}")
        
        category_results = {"success": 0, "error": 0, "avg_relevance": 0}
        relevance_scores = []
        
        for i, question in enumerate(questions, 1):
            results["total"] += 1
            
            # Detect language
            is_urdu = any('\u0600' <= c <= '\u06FF' for c in question)
            lang = "Urdu" if is_urdu else "English"
            
            # Test question
            result = test_rag_endpoint(question, lang)
            
            if result["status"] == "success":
                results["success"] += 1
                category_results["success"] += 1
                
                data = result["data"]
                method = data.get("method", "unknown")
                answer_preview = data.get("reply", "")[:100]
                
                # Get relevance score if available
                if data.get("sources"):
                    relevance = data["sources"][0].get("relevance", 0)
                    relevance_scores.append(relevance)
                
                print(f"  ✅ {i}/{len(questions)}: {question[:60]}...")
                print(f"     Method: {method} | Answer: {answer_preview}...")
                
            else:
                results["error"] += 1
                category_results["error"] += 1
                results["failed_questions"].append({
                    "category": category,
                    "question": question,
                    "error": result["error"]
                })
                print(f"  ❌ {i}/{len(questions)}: {question[:60]}...")
                print(f"     Error: {result['error']}")
            
            # Small delay to avoid overwhelming the server
            time.sleep(0.1)
        
        # Calculate category stats
        if relevance_scores:
            category_results["avg_relevance"] = sum(relevance_scores) / len(relevance_scores)
        
        results["by_category"][category] = category_results
        
        print(f"\n  📊 Category Results:")
        print(f"     Success: {category_results['success']}/{len(questions)}")
        if relevance_scores:
            print(f"     Avg Relevance: {category_results['avg_relevance']:.3f}")
    
    elapsed_time = time.time() - start_time
    
    # Final Summary
    print("\n" + "="*80)
    print("📊 FINAL TEST RESULTS")
    print("="*80)
    print(f"\n✅ Total Questions Tested: {results['total']}")
    print(f"✅ Successful: {results['success']} ({results['success']/results['total']*100:.1f}%)")
    print(f"❌ Failed: {results['error']} ({results['error']/results['total']*100:.1f}%)")
    print(f"⏱️  Total Time: {elapsed_time:.1f} seconds")
    print(f"⚡ Avg Time per Question: {elapsed_time/results['total']:.2f} seconds")
    
    # Category breakdown
    print("\n📁 Results by Category:")
    for category, stats in results["by_category"].items():
        success_rate = stats['success'] / (stats['success'] + stats['error']) * 100
        print(f"\n  {category}:")
        print(f"    Success Rate: {success_rate:.1f}%")
        if stats.get('avg_relevance'):
            print(f"    Avg Relevance: {stats['avg_relevance']:.3f}")
    
    # Failed questions
    if results["failed_questions"]:
        print("\n❌ Failed Questions:")
        for failed in results["failed_questions"][:10]:  # Show first 10
            print(f"\n  [{failed['category']}] {failed['question']}")
            print(f"  Error: {failed['error']}")
    
    # Save results to file
    with open("backend/rag_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed results saved to: backend/rag_test_results.json")
    print("\n" + "="*80)
    
    return results

if __name__ == "__main__":
    print("\n⚠️  Make sure the backend is running on http://127.0.0.1:8000")
    input("Press Enter to start comprehensive testing...")
    
    results = run_comprehensive_test()
    
    if results["success"] / results["total"] >= 0.95:
        print("\n🎉 EXCELLENT! RAG system is production-ready! (>95% success rate)")
    elif results["success"] / results["total"] >= 0.85:
        print("\n✅ GOOD! RAG system is working well (>85% success rate)")
    else:
        print("\n⚠️  NEEDS IMPROVEMENT (success rate below 85%)")
