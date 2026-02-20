import requests

def test_chat():
    queries = [
        "what causes tb",
        "how does tb spread",
        "prevention of tb",
        "examples of extrapulmonary tb",
        "types of tb",
        "ٹی بی کیسے پھیلتی ہے؟",
        "ٹی بی سے بچاؤ؟",
        "ٹی بی کیوں ہوتی ہے؟"
    ]
    
    print("🚀 TESTING MATURE AI SEMANTIC ACCURACY...")
    for q in queries:
        try:
            r = requests.post("http://127.0.0.1:8000/chat", json={"message": q})
            data = r.json()
            print(f"\n💬 USER: {q}")
            print(f"📄 CAT:  [{data.get('category')}]")
            print(f"🤖 BOT:  {data.get('reply')}")
        except Exception as e:
            print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_chat()
