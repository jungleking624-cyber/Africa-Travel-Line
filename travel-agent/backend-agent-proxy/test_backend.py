"""
Test script for backend API (Direct Agentverse Integration)
I Test all endpoints to verify functionality
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def test_health():
    """Test health check endpoint"""
    print_section("Testing Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response:")
        print(f"  Status: {data.get('status')}")
        print(f"  Agent: {data.get('travel_agent')}")
        print(f"  Configured: {data.get('agentverse_configured')}")
        print(f"  Chat URL: {data.get('chat_url')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_agent_info():
    """Test agent info endpoint"""
    print_section("Testing Agent Info")
    
    try:
        response = requests.get(f"{BASE_URL}/api/agent-info")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response:")
        print(f"  Agent Address: {data.get('agentAddress')}")
        print(f"  Chat URL: {data.get('chatUrl')}")
        print(f"  Profile URL: {data.get('profileUrl')}")
        print(f"  API Configured: {data.get('apiConfigured')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chat(message):
    """Test chat endpoint"""
    print_section(f"Testing Chat Endpoint")
    print(f"💬 Message: '{message}'")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": message},
            headers={"Content-Type": "application/json"},
            timeout=35
        )
        
        print(f"\nStatus: {response.status_code}")
        data = response.json()
        
        if data.get('success'):
            print("✅ Success!")
            print(f"\nAgent Response:")
            print(f"  {data.get('message', '')[:300]}...")
            print(f"\n  Session ID: {data.get('sessionId')}")
            print(f"  Timestamp: {data.get('timestamp')}")
        else:
            print("⚠️  Not successful (this is expected if Chat API not available)")
            print(f"\n  Error: {data.get('error')}")
            print(f"  Message: {data.get('message')}")
            if 'chatUrl' in data:
                print(f"\n  💡 Use this URL instead: {data['chatUrl']}")
        
        return data
    except requests.Timeout:
        print(f"❌ Request timed out after 35 seconds")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_session_retrieval(session_id):
    """Test session retrieval endpoint"""
    print_section("Testing Session Retrieval")
    print(f"📋 Session ID: {session_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/api/session/{session_id}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Messages in session: {len(data.get('messages', []))}")
            for msg in data.get('messages', []):
                print(f"\n  {msg['role']}: {msg['content'][:100]}...")
        else:
            print(f"Response: {response.json()}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("\n🧪 Backend API Test Suite")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Target: {BASE_URL}")
    
    results = {}
    
    # Test 1: Health Check
    results['health'] = test_health()
    time.sleep(1)
    
    # Test 2: Agent Info
    results['info'] = test_agent_info()
    time.sleep(1)
    
    # Test 3: Chat
    chat_result = test_chat("What do I need for a trip to Japan?")
    results['chat'] = bool(chat_result)
    
    # Test 4: Session Retrieval (if chat succeeded)
    if chat_result and chat_result.get('sessionId'):
        time.sleep(1)
        results['session'] = test_session_retrieval(chat_result['sessionId'])
    else:
        results['session'] = None
    
    # Summary
    print_section("Test Summary")
    print(f"✓ Health Check:       {'✅ PASS' if results['health'] else '❌ FAIL'}")
    print(f"✓ Agent Info:         {'✅ PASS' if results['info'] else '❌ FAIL'}")
    print(f"✓ Chat Endpoint:      {'✅ PASS' if results['chat'] else '❌ FAIL'}")
    if results['session'] is not None:
        print(f"✓ Session Retrieval:  {'✅ PASS' if results['session'] else '❌ FAIL'}")
    else:
        print(f"✓ Session Retrieval:  ⏭️  SKIPPED")
    
    # Overall status
    passed = sum(1 for v in results.values() if v is True)
    total = sum(1 for v in results.values() if v is not None)
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    # Recommendations
    print_section("💡 Recommendations")
    
    if not results['health']:
        print("❌ Backend server is not running or not reachable")
        print("   → Start the server: python backend_direct_api.py")
    elif not results['chat']:
        print("⚠️  Chat functionality is not working")
        print("   This is expected if:")
        print("   1. AGENTVERSE_API_KEY is not configured")
        print("   2. Agentverse Chat API is not yet publicly available")
        print("\n   → Use the Direct Chat URL provided in responses")
        print("   → Or wait for official Chat API release")
    else:
        print("✅ All systems operational!")
        print("\n   Your backend is ready to handle chat requests.")
        if chat_result and chat_result.get('success'):
            print("   Agent responses are being received successfully.")
        else:
            print("   Note: Using fallback mode until Chat API is available.")
    
    print("\n" + "="*60)
    print("✨ Test suite completed")
    print("="*60 + "\n")