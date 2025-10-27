"""
Test script for backend agent proxy
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("\n🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_agent_info():
    """Test agent info endpoint"""
    print("\n🔍 Testing agent info endpoint...")
    response = requests.get(f"{BASE_URL}/api/agent-info")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_chat(message):
    """Test chat endpoint"""
    print(f"\n💬 Testing chat with message: '{message}'")
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={
            "message": message,
            "sessionId": "test-session-123"
        },
        timeout=15
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("="*60)
    print("🧪 BACKEND AGENT PROXY TEST SUITE")
    print("="*60)
    
    try:
        test_health()
        test_agent_info()
        test_chat("What do I need for a trip to Japan?")
        
        print("\n" + "="*60)
        print("✅ All tests completed")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to backend")
        print("Make sure the backend is running: python backend_agent.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")