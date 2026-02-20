import requests

def test_chat():
    queries = [
        "What is tb?",
        "define tb",
        "symptoms of tb",
        "What's the dose of Bedaquiline?",
        "ٹی بی کیا ہے؟",
        "کھانسی کا علاج"
    ]
    
    print("🚀 TESTING CHATBOT SEMANTIC ACCURACY...")
    for q in queries:
        try:
            r = requests.post("http://127.0.0.1:8000/chat", json={"message": q})
            data = r.json()
            print(f"\n💬 USER: {q}")
            print(f"📄 CAT:  [{data.get('category')}]")
            print(f"🤖 BOT:  {data.get('reply')[:200]}...")
        except Exception as e:
            print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_chat()
