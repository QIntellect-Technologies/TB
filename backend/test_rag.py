"""
Test script for RAG system
Tests both retrieval-only and LLM-enhanced modes
"""
import requests
import json

API_BASE = "http://127.0.0.1:8000"

def test_rag_endpoint():
    """Test the RAG endpoint with various queries"""
    
    test_cases = [
        {
            "name": "Simple Definition",
            "query": "What is tuberculosis?",
            "expected_keywords": ["bacteria", "lung", "infection"]
        },
        {
            "name": "Complex Multi-Part",
            "query": "What is the difference between latent TB and active TB, and how should each be treated?",
            "expected_keywords": ["latent", "active", "treatment"]
        },
        {
            "name": "Drug-Specific",
            "query": "What is the dosage of Bedaquiline for MDR-TB?",
            "expected_keywords": ["bedaquiline", "mg", "dose"]
        },
        {
            "name": "Conversational",
            "query": "My patient has been coughing for 3 weeks with night sweats. Could this be TB?",
            "expected_keywords": ["symptom", "cough", "TB"]
        },
        {
            "name": "Urdu Query",
            "query": "ٹی بی کی علامات کیا ہیں؟",
            "expected_keywords": ["علامات", "کھانسی"]
        }
    ]
    
    print("="*70)
    print("🧪 TESTING RAG ENDPOINT")
    print("="*70)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"Test {i}: {test['name']}")
        print(f"Query: {test['query']}")
        print("-"*70)
        
        try:
            response = requests.post(
                f"{API_BASE}/chat-rag",
                json={"message": test['query']},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ Status: SUCCESS")
                print(f"📊 Method: {data.get('method', 'N/A')}")
                print(f"🌐 Language: {data.get('language', 'N/A')}")
                print(f"📁 Category: {data.get('category', 'N/A')}")
                
                print(f"\n💬 Answer:")
                print(f"{data['reply'][:300]}...")
                
                if data.get('sources'):
                    print(f"\n📚 Sources ({len(data['sources'])}):")
                    for j, src in enumerate(data['sources'][:3], 1):
                        print(f"  {j}. [{src['category']}] Relevance: {src['relevance']:.3f}")
                        print(f"     Q: {src['question'][:80]}...")
                
                # Check for expected keywords
                answer_lower = data['reply'].lower()
                found_keywords = [kw for kw in test['expected_keywords'] if kw.lower() in answer_lower or kw in data['reply']]
                
                if found_keywords:
                    print(f"\n✅ Found keywords: {', '.join(found_keywords)}")
                else:
                    print(f"\n⚠️  Expected keywords not found: {test['expected_keywords']}")
            
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text}")
        
        except requests.exceptions.Timeout:
            print("⏱️  Request timed out (>30s)")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'='*70}")
    print("✅ TESTING COMPLETE")
    print("="*70)

def compare_endpoints():
    """Compare standard chat vs RAG responses"""
    
    query = "What are the symptoms of tuberculosis?"
    
    print("\n" + "="*70)
    print("🔬 COMPARING ENDPOINTS")
    print("="*70)
    print(f"Query: {query}\n")
    
    # Test standard endpoint
    print("-"*70)
    print("⚡ STANDARD ENDPOINT (/chat)")
    print("-"*70)
    try:
        res1 = requests.post(f"{API_BASE}/chat", json={"message": query})
        if res1.status_code == 200:
            data1 = res1.json()
            print(f"Method: FTS")
            print(f"Answer: {data1['reply'][:200]}...\n")
    except Exception as e:
        print(f"Error: {e}\n")
    
    # Test RAG endpoint
    print("-"*70)
    print("🧠 RAG ENDPOINT (/chat-rag)")
    print("-"*70)
    try:
        res2 = requests.post(f"{API_BASE}/chat-rag", json={"message": query})
        if res2.status_code == 200:
            data2 = res2.json()
            print(f"Method: {data2.get('method', 'N/A')}")
            print(f"Answer: {data2['reply'][:200]}...")
            if data2.get('sources'):
                print(f"Sources: {len(data2['sources'])} documents")
    except Exception as e:
        print(f"Error: {e}")
    
    print("="*70)

if __name__ == "__main__":
    print("\n🚀 Starting RAG System Tests...\n")
    
    # Wait for user confirmation
    input("Press Enter to start testing (make sure backend is running)...")
    
    # Run tests
    test_rag_endpoint()
    compare_endpoints()
    
    print("\n✅ All tests completed!")
