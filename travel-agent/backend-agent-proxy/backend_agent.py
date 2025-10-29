"""
Local Travel Agent - Runs on your machine
Communicates via HTTP endpoints for easy UI integration
"""

import os
import asyncio
import httpx
from datetime import datetime, timezone
from uuid import uuid4
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask app for UI communication
app = Flask(__name__, static_folder='.')
CORS(app)

# Configuration
ASI1_API_KEY = os.getenv("ASI1_API_KEY", "")
METTA_API_KEY = os.getenv("METTA_API_KEY", "")
TRAVEL_AGENT_ADDRESS = "agent1qwatl9nznqul3nldvh59lu7ph53fpm4r3y4t5t9ku352d3ur7lkscgzp6vy"
AGENTVERSE_API_KEY = os.getenv("AGENTVERSE_API_KEY", "")
ASI1_API_URL = "https://api.asi1.ai/v1/chat/completions"
METTA_API_URL = "https://metta-api.singularitynet.io/v1/query"

# In-memory conversation storage
conversations = {}

# System prompt for the travel agent
SYSTEM_PROMPT = """You are an expert travel advisor assistant. Your role is to:

1. Answer travel questions about visas, vaccinations, weather, customs, currency, and safety
2. Provide verified, fact-based information when available
3. Suggest comprehensive packing lists and travel preparations
4. Be specific, practical, and safety-conscious
5. Always prioritize traveler safety and legal compliance

When answering:
- Be specific about requirements (visa types, vaccination names, documents needed)
- Include seasonal and regional variations
- Mention cultural sensitivities and local customs
- Provide practical tips (power adapters, SIM cards, transportation)
- Recommend checking official government sources for critical requirements
"""


class MeTTaService:
    """MeTTa Knowledge Graph service"""
    
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.api_url = api_url
        self.timeout = 10.0
    
    async def query(self, query: str) -> dict:
        """Query MeTTa knowledge graph"""
        if not self.api_key:
            return None
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "query": query,
                        "domains": ["travel", "geography", "health", "culture"],
                        "max_results": 5,
                        "include_relations": True
                    }
                )
                
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            print(f"MeTTa query failed: {e}")
            return None
    
    def format_context(self, knowledge: dict) -> str:
        """Format MeTTa knowledge for LLM context"""
        if not knowledge or not knowledge.get("results"):
            return ""
        
        context_parts = ["\n\n=== VERIFIED KNOWLEDGE ==="]
        
        for idx, result in enumerate(knowledge.get("results", [])[:5], 1):
            context_parts.append(f"\n[Fact {idx}]")
            
            if "entity" in result:
                context_parts.append(f"Entity: {result['entity']}")
            
            if "relations" in result:
                for rel in result["relations"]:
                    context_parts.append(f"  - {rel.get('predicate', 'related_to')}: {rel.get('object', 'N/A')}")
            
            if "properties" in result:
                for key, value in result["properties"].items():
                    context_parts.append(f"  {key}: {value}")
            
            if "confidence" in result:
                context_parts.append(f"  Confidence: {result['confidence']}")
        
        context_parts.append("\n=== END VERIFIED KNOWLEDGE ===\n")
        return "\n".join(context_parts)


class ASI1Service:
    """ASI1 LLM service"""
    
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.api_url = api_url
        self.model = "asi1-mini"
        self.timeout = 30.0
    
    async def chat(self, user_message: str, system_prompt: str, metta_context: str = "") -> str:
        """Call ASI1 LLM API"""
        if not self.api_key:
            return "Error: ASI1 API key not configured. Please set ASI1_API_KEY in .env file."
        
        # Enhance message with MeTTa context
        enhanced_message = user_message
        if metta_context:
            enhanced_message = f"{metta_context}\n\nUser Question: {user_message}\n\nPlease answer using the verified knowledge above when relevant."
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": enhanced_message}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 1000
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("choices", [{}])[0].get("message", {}).get("content", "")
                elif response.status_code == 401:
                    return "Error: Invalid ASI1 API key."
                else:
                    return f"Error: API returned {response.status_code}"
        
        except httpx.TimeoutException:
            return "Error: Request timed out. Please try again."
        except Exception as e:
            return f"Error: {str(e)}"


# Initialize services
metta_service = MeTTaService(METTA_API_KEY, METTA_API_URL)
asi1_service = ASI1Service(ASI1_API_KEY, ASI1_API_URL)


# ============================================
# Flask Routes
# ============================================

@app.route('/')
def index():
    """Serve the chat UI"""
    return send_from_directory('.', 'chat_ui.html')


@app.route('/api/chat', methods=['POST'])
async def chat():
    """Handle chat messages from UI"""
    try:
        data = request.json
        message = data.get('message', '').strip()
        session_id = data.get('sessionId', str(uuid4()))
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        print(f"\n📨 Message from UI: {message}")
        print(f"   Session: {session_id}")
        
        # Initialize session if needed
        if session_id not in conversations:
            conversations[session_id] = []
        
        # Store user message
        conversations[session_id].append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now(timezone.utc).isoformat()  # FIXED
        })
        
        # Query MeTTa knowledge graph
        metta_knowledge = await metta_service.query(message)
        metta_context = metta_service.format_context(metta_knowledge)
        
        # Get response from ASI1 LLM
        assistant_response = await asi1_service.chat(
            user_message=message,
            system_prompt=SYSTEM_PROMPT,
            metta_context=metta_context
        )
        
        # Add knowledge attribution if used
        if metta_context and not assistant_response.startswith("Error:"):
            assistant_response += "\n\n---\n💡 *Enhanced with verified knowledge from MeTTa Knowledge Graph*"
        
        # Store agent response
        conversations[session_id].append({
            'role': 'assistant', 
            'content': assistant_response,
            'timestamp': datetime.now(timezone.utc).isoformat() 
        })
        
        print(f"✅ Response: {assistant_response[:100]}...")
        
        return jsonify({
            'success': True,
            'message': assistant_response,
            'sessionId': session_id,
            'timestamp': datetime.now(timezone.utc).isoformat()  
        })
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history/<session_id>', methods=['GET'])
def get_history(session_id):
    """Get conversation history"""
    if session_id not in conversations:
        return jsonify({
            'success': False,
            'error': 'Session not found'
        }), 404
    
    return jsonify({
        'success': True,
        'sessionId': session_id,
        'messages': conversations[session_id]
    })


@app.route('/api/clear/<session_id>', methods=['DELETE'])
def clear_history(session_id):
    """Clear conversation history"""
    if session_id in conversations:
        del conversations[session_id]
    
    return jsonify({
        'success': True,
        'message': 'History cleared'
    })


@app.route('/api/status', methods=['GET'])
def status():
    """Get agent status"""
    return jsonify({
        'status': 'online',
        'asi1_configured': bool(ASI1_API_KEY),
        'metta_configured': bool(METTA_API_KEY),
        'active_sessions': len(conversations),
        'timestamp': datetime.now(timezone.utc).isoformat()
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'travel_agent': TRAVEL_AGENT_ADDRESS,
        'agentverse_configured': bool(AGENTVERSE_API_KEY),
        'chat_url': f'https://agentverse.ai/chat?agent={TRAVEL_AGENT_ADDRESS}',
        'timestamp': datetime.now(timezone.utc).isoformat()
    })


@app.route('/api/agent-info', methods=['GET'])
def agent_info():
    """Get agent information"""
    return jsonify({
        'agentAddress': TRAVEL_AGENT_ADDRESS,
        'chatUrl': f'https://agentverse.ai/chat?agent={TRAVEL_AGENT_ADDRESS}',
        'profileUrl': f'https://agentverse.ai/agents/{TRAVEL_AGENT_ADDRESS}',
        'apiConfigured': bool(AGENTVERSE_API_KEY),
        'recommendation': (
            'For the best real-time experience, use Agentverse Chat UI directly. '
            'The Chat API integration is being developed.'
        )
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌍 Local Travel FAQ Agent")
    print("="*60)
    print(f"ASI1 API: {'✅ Configured' if ASI1_API_KEY else '❌ Not configured'}")
    print(f"MeTTa API: {'✅ Configured' if METTA_API_KEY else '❌ Not available'}")
    print(f"\n🌐 Open in browser: http://localhost:5000")
    print(f"📡 API endpoint: http://localhost:5000/api/chat")
    print("="*60 + "\n")
    
    if not ASI1_API_KEY:
        print("⚠️  WARNING: ASI1_API_KEY not set!")
        print("   Add it to your .env file to enable responses\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)