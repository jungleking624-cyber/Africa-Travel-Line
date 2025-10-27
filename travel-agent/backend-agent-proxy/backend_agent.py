"""
Backend Agent Proxy for Travel FAQ Assistant
This creates a uAgent that communicates with your travel agent via mailbox
"""

import os
import asyncio
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, Optional, List
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    chat_protocol_spec,
    ChatMessage,
    ChatAcknowledgement,
    TextContent,
    StartSessionContent,
    EndSessionContent,
)

# Load environment variables
load_dotenv()

# Configuration
TRAVEL_AGENT_ADDRESS = os.getenv(
    "TRAVEL_AGENT_ADDRESS",
    "agent1qwatl9nznqul3nldvh59lu7ph53fpm4r3y4t5t9ku352d3ur7lkscgzp6vy"
)
BACKEND_AGENT_SEED = os.getenv("BACKEND_AGENT_SEED", "backend_proxy_seed_12345")
BACKEND_AGENT_PORT = int(os.getenv("BACKEND_AGENT_PORT", "8002"))
FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))

# Storage for sessions and responses
sessions: Dict[str, Dict] = {}
response_queue: Dict[str, List[str]] = {}

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Initialize uAgent with mailbox
backend_agent = Agent(
    name="backend_proxy",
    seed=BACKEND_AGENT_SEED,
    port=BACKEND_AGENT_PORT,
    mailbox=True,
    endpoint=[f"http://localhost:{BACKEND_AGENT_PORT}/submit"]
)

# Create chat protocol
chat_protocol = Protocol(spec=chat_protocol_spec)

print("\n" + "="*70)
print("🤖 BACKEND AGENT PROXY")
print("="*70)
print(f"Backend Agent Address: {backend_agent.address}")
print(f"Travel Agent Address: {TRAVEL_AGENT_ADDRESS}")
print(f"Flask API Port: {FLASK_PORT}")
print(f"Agent Port: {BACKEND_AGENT_PORT}")
print("="*70 + "\n")


# ============================================
# Agent Event Handlers
# ============================================

@backend_agent.on_event("startup")
async def agent_startup(ctx: Context):
    """Called when agent starts"""
    ctx.logger.info("🚀 Backend proxy agent started")
    ctx.logger.info(f"📍 Address: {ctx.agent.address}")
    ctx.logger.info(f"🎯 Target: {TRAVEL_AGENT_ADDRESS}")


@backend_agent.on_event("shutdown")
async def agent_shutdown(ctx: Context):
    """Called when agent stops"""
    ctx.logger.info("👋 Backend proxy agent shutting down")


# ============================================
# Chat Protocol Handlers
# ============================================

@chat_protocol.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages from travel agent"""
    ctx.logger.info(f"📨 Received message from {sender}")
    
    # Always ACK first
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.now(timezone.utc),
        acknowledged_msg_id=msg.msg_id,
    ))
    
    # Process message content
    for content_item in msg.content:
        if isinstance(content_item, TextContent):
            text = content_item.text
            ctx.logger.info(f"💬 Response: {text[:100]}...")
            
            # Store response in queue (keyed by sender for now)
            if sender not in response_queue:
                response_queue[sender] = []
            response_queue[sender].append(text)
            
            # Also store as 'latest' for simple retrieval
            response_queue['latest'] = [text]
            
            ctx.logger.info(f"✅ Stored response in queue")


@chat_protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle acknowledgements"""
    ctx.logger.info(f"✓ ACK from {sender} for message {msg.acknowledged_msg_id}")


# Include protocol
backend_agent.include(chat_protocol, publish_manifest=True)


# ============================================
# Helper Functions
# ============================================

async def send_to_travel_agent(session_id: str, message: str) -> bool:
    """Send message to travel agent"""
    try:
        # Create chat message with session start
        chat_msg = ChatMessage(
            timestamp=datetime.now(timezone.utc),
            msg_id=uuid4(),
            content=[
                StartSessionContent(type="start-session"),
                TextContent(type="text", text=message)
            ]
        )
        
        # Get agent context
        ctx = Context(
            agent=backend_agent,
            storage=backend_agent._storage,
            ledger=backend_agent._ledger,
            resolver=backend_agent._resolver,
            interval_messages=backend_agent._interval_messages,
            message_queue=backend_agent._message_queue,
            session=uuid4()
        )
        
        # Send to travel agent
        await ctx.send(TRAVEL_AGENT_ADDRESS, chat_msg)
        print(f"📤 Sent to travel agent: {message[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error sending to travel agent: {e}")
        return False


def get_latest_response(timeout: int = 5) -> Optional[str]:
    """Wait for and get latest response from queue"""
    import time
    
    elapsed = 0
    check_interval = 0.5
    
    while elapsed < timeout:
        if 'latest' in response_queue and response_queue['latest']:
            response = response_queue['latest'][0]
            response_queue['latest'] = []  # Clear after reading
            return response
        
        time.sleep(check_interval)
        elapsed += check_interval
    
    return None


# ============================================
# Flask HTTP Endpoints
# ============================================

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """HTTP endpoint to send messages to travel agent"""
    try:
        data = request.json
        message = data.get('message', '').strip()
        session_id = data.get('sessionId', str(uuid4()))
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        print(f"\n📨 HTTP Request:")
        print(f"   Session: {session_id}")
        print(f"   Message: {message}")
        
        # Store session
        if session_id not in sessions:
            sessions[session_id] = {
                'id': session_id,
                'messages': [],
                'created_at': datetime.now().isoformat()
            }
        
        sessions[session_id]['messages'].append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Send to travel agent via agent communication
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success = loop.run_until_complete(
            send_to_travel_agent(session_id, message)
        )
        loop.close()
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Failed to send message to agent',
                'message': 'Error communicating with travel agent'
            }), 500
        
        print("⏳ Waiting for agent response...")
        
        # Wait for response
        response_text = get_latest_response(timeout=10)
        
        if response_text:
            print(f"✅ Got response: {response_text[:100]}...")
            
            sessions[session_id]['messages'].append({
                'role': 'agent',
                'content': response_text,
                'timestamp': datetime.now().isoformat()
            })
            
            return jsonify({
                'success': True,
                'message': response_text,
                'sessionId': session_id,
                'enhanced': True
            })
        else:
            print("⚠️  No response received within timeout")
            
            # Return helpful message
            fallback_message = (
                "Your message was sent to the travel agent. "
                "Agent responses may take a moment. For immediate responses, "
                "please visit https://agentverse.ai/chat?agent=" + TRAVEL_AGENT_ADDRESS
            )
            
            return jsonify({
                'success': True,
                'message': fallback_message,
                'sessionId': session_id,
                'timeout': True,
                'chatUrl': f'https://agentverse.ai/chat?agent={TRAVEL_AGENT_ADDRESS}'
            })
        
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Internal server error'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'backend_agent': str(backend_agent.address),
        'travel_agent': TRAVEL_AGENT_ADDRESS,
        'flask_port': FLASK_PORT,
        'agent_port': BACKEND_AGENT_PORT,
        'sessions': len(sessions),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/agent-info', methods=['GET'])
def agent_info():
    """Get agent information"""
    return jsonify({
        'backendAgent': str(backend_agent.address),
        'travelAgent': TRAVEL_AGENT_ADDRESS,
        'chatUrl': f'https://agentverse.ai/chat?agent={TRAVEL_AGENT_ADDRESS}',
        'flaskPort': FLASK_PORT,
        'agentPort': BACKEND_AGENT_PORT
    })


@app.route('/api/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get session history"""
    if session_id in sessions:
        return jsonify({
            'success': True,
            'session': sessions[session_id]
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Session not found'
        }), 404


# ============================================
# Run Both Flask and Agent
# ============================================

def run_flask():
    """Run Flask app"""
    print(f"\n🌐 Starting Flask API on port {FLASK_PORT}...")
    app.run(
        host='0.0.0.0',
        port=FLASK_PORT,
        debug=False,
        use_reloader=False,
        threaded=True
    )


def run_agent():
    """Run uAgent"""
    print(f"\n🤖 Starting Backend Agent on port {BACKEND_AGENT_PORT}...")
    backend_agent.run()


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 STARTING BACKEND AGENT PROXY")
    print("="*70)
    print(f"📍 Backend Agent: {backend_agent.address}")
    print(f"🎯 Travel Agent: {TRAVEL_AGENT_ADDRESS}")
    print(f"🌐 Flask API: http://localhost:{FLASK_PORT}")
    print(f"🤖 Agent Port: {BACKEND_AGENT_PORT}")
    print(f"💚 Health: http://localhost:{FLASK_PORT}/api/health")
    print("="*70 + "\n")
    
    # Start Flask in separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Small delay to let Flask start
    import time
    time.sleep(2)
    
    print("\n✅ Flask API started successfully")
    print("\n🤖 Starting uAgent (this will take a moment)...\n")
    
    # Run agent in main thread
    try:
        run_agent()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()