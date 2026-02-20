import requests

def verify():
    queries = [
        "What is tb?",
        "What is Tuberculosis?",
        "Explain Latent TB",
        "ٹی بی کیا ہے؟"
    ]
    
    for q in queries:
        print(f"\n🔍 Query: {q}")
        r = requests.get('http://127.0.0.1:8000/search', params={'q': q, 'limit': 3})
        results = r.json()
        if results:
            for i, res in enumerate(results):
                print(f"  {i+1}. [{res['category']}] {res['question']}")
                print(f"     Ans: {res['answer'][:100]}...")
        else:
            print("  ❌ NO RESULTS")

if __name__ == "__main__":
    verify()
