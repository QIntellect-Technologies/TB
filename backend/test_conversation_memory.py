"""
Test Conversation Memory Feature
Demonstrates context-aware responses
"""
import requests
import json

API_BASE = "http://127.0.0.1:8000"
SESSION_ID = "test_session_123"

def test_conversation(messages):
    """Test a conversation flow"""
    print("\n" + "="*80)
    print("🧪 TESTING CONVERSATION MEMORY")
    print("="*80)
    
    for i, msg in enumerate(messages, 1):
        print(f"\n{'='*80}")
        print(f"Message {i}: {msg}")
        print("-"*80)
        
        response = requests.post(
            f"{API_BASE}/chat-rag",
            json={
                "message": msg,
                "session_id": SESSION_ID
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("reply", "")
            method = data.get("method", "")
            
            print(f"✅ Method: {method}")
            print(f"💬 Answer: {answer[:300]}...")
        else:
            print(f"❌ Error: {response.status_code}")
        
        print()

if __name__ == "__main__":
    print("\n⚠️  Make sure the backend is running on http://127.0.0.1:8000")
    input("Press Enter to start conversation test...")
    
    # Test 1: Basic conversation flow
    print("\n" + "="*80)
    print("TEST 1: Basic Conversation Flow")
    print("="*80)
    
    conversation1 = [
        "Hi",
        "What is TB?",
        "Is it curable?",  # "it" refers to text, expect direct answer
        "What are its symptoms?",
        "How is it treated?", 
        "Tell me more about the treatment",
        "What about prevention?"
    ]
    
    test_conversation(conversation1)
    
    # Test 2: Topic switching
    print("\n" + "="*80)
    print("TEST 2: Topic Switching")
    print("="*80)
    
    conversation2 = [
        "What is MDR-TB?",
        "Explain it in detail",  # "it" refers to MDR-TB
        "What drugs are used?",  # Context: MDR-TB drugs
        "What is XDR-TB?",  # New topic
        "How is it different?",  # "it" refers to XDR-TB
    ]
    
    test_conversation(conversation2)
    
    # Test 3: Complex follow-ups
    print("\n" + "="*80)
    print("TEST 3: Complex Follow-ups")
    print("="*80)
    
    conversation3 = [
        "What is pulmonary TB?",
        "And extrapulmonary?",  # Follow-up with "and"
        "Explain the difference",  # Needs context
        "Which is more common?",  # Needs context
    ]
    
    test_conversation(conversation3)
    
    print("\n" + "="*80)
    print("✅ CONVERSATION MEMORY TEST COMPLETE")
    print("="*80)
