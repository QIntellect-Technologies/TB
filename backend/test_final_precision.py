import requests

def test_chat():
    queries = [
        "tb?",
        "what is tb",
        "what are the symptoms of tb",
        "how tb spread?",
        "ٹی بی کیا ہے؟",
        "ٹی بی کی علامات"
    ]
    
    print("🚀 FINAL PRECISION VERIFICATION...")
    for q in queries:
        try:
            r = requests.post("http://127.0.0.1:8000/chat", json={"message": q})
            try:
                data = r.json()
                print(f"\n💬 USER: {q}")
                print(f"📄 CAT:  [{data.get('category')}]")
                print(f"🤖 BOT REPLY: {data.get('reply')[:200]}...")
            except:
                print(f"❌ ERROR: JSON Decode Failed. Code: {r.status_code}")
                print(f"RAW: {r.text[:200]}")
        except Exception as e:
            print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_chat()
