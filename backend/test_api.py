import requests

def test_api():
    try:
        url = "http://127.0.0.1:8000/search"
        params = {"q": "کھانسی", "limit": 1}
        response = requests.get(url, params=params)
        data = response.json()
        if data:
            print(f"✅ API Success: Found '{data[0]['question']}'")
        else:
            print("❌ API Failure: No results found.")
            
        stats = requests.get("http://127.0.0.1:8000/stats").json()
        print(f"📊 Stats: {stats}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()
