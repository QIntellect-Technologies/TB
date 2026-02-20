import requests

def test_chat():
    queries = [
        "what is tb",
        "types of tb",
        "symptoms of tb",
        "What's the dose of Bedaquiline?",
        "ٹی بی کیا ہے؟",
        "ٹی بی کی علامات"
    ]
    
    print("🚀 TESTING CHATBOT SEMANTIC ACCURACY V2...")
    for q in queries:
        try:
            r = requests.post("http://127.0.0.1:8000/chat", json={"message": q})
            data = r.json()
            print(f"\n💬 USER: {q}")
            print(f"📄 CAT:  [{data.get('category')}]")
            print(f"🤖 BOT:  {data.get('reply')[:300]}...")
        except Exception as e:
            print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_chat()
