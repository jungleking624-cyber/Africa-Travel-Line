
import os
import sys
from datetime import datetime, timezone
from uuid import uuid4
from typing import Optional, Dict, List

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    chat_protocol_spec,
    ChatMessage,
    ChatAcknowledgement,
    TextContent,
    MetadataContent,
    StartSessionContent,
    EndSessionContent,
)

# Import local modules
from config import Config
from services import ASI1Service, MeTTaService
from utils import setup_logging, sanitize_input

# Setup logging
logger = setup_logging()

# Load configuration
config = Config()

# Initialize agent with mailbox
agent = Agent(
    name=config.AGENT_NAME,
    seed=config.AGENT_SEED,
    port=config.PORT,
    mailbox=True,  # Enable mailbox for Agentverse connectivity
    endpoint=[f"http://localhost:{config.PORT}/submit"],
)

# Initialize services
asi1_service = ASI1Service(config.ASI1_API_KEY)
metta_service = MeTTaService(config.METTA_API_KEY, config.METTA_API_URL)

# Create chat protocol
chat_proto = Protocol(spec=chat_protocol_spec)

# System prompt
SYSTEM_PROMPT = """You are an expert travel advisor assistant enhanced with structured knowledge from SingularityNet's MeTTa knowledge graph. Your role is to:

1. Answer travel questions about visas, vaccinations, weather, customs, currency, and safety
2. Provide verified, fact-based information when available from the knowledge graph
3. Suggest comprehensive packing lists and travel preparations
4. Be specific, practical, and safety-conscious
5. Clearly distinguish between verified facts and general recommendations
6. Always prioritize traveler safety and legal compliance

When answering:
- Lead with structured facts from the knowledge graph when available (cite as "According to verified data...")
- Be specific about requirements (visa types, vaccination names, documents needed)
- Include seasonal and regional variations
- Mention cultural sensitivities and local customs
- Provide practical tips (power adapters, SIM cards, transportation)
- Recommend checking official government sources for critical requirements
"""


def _text(msg: str) -> ChatMessage:
    """Helper to create text ChatMessage"""
    return ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=uuid4(),
        content=[TextContent(type="text", text=msg)]
    )


@agent.on_event("startup")
async def startup(ctx: Context):
    """Agent startup event"""
    ctx.logger.info(f"Travel FAQ Agent started!")
    ctx.logger.info(f"Agent address: {ctx.agent.address}")
    ctx.logger.info(f"Mailbox enabled: True")
    ctx.logger.info(f"Port: {config.PORT}")
    ctx.logger.info(f"ASI1 configured: {bool(config.ASI1_API_KEY)}")
    ctx.logger.info(f"MeTTa configured: {bool(config.METTA_API_KEY)}")


@agent.on_event("shutdown")
async def shutdown(ctx: Context):
    """Agent shutdown event"""
    ctx.logger.info("Travel FAQ Agent shutting down...")


@chat_proto.on_message(ChatMessage)
async def on_chat(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages with MeTTa knowledge enhancement"""
    ctx.logger.info(f"Received message from {sender}")
    
    # Always ACK first
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.now(timezone.utc),
        acknowledged_msg_id=msg.msg_id,
    ))
    
    for content_item in msg.content:
        if isinstance(content_item, StartSessionContent):
            ctx.logger.info(f"Session started with {sender}")
            
            # Advertise enhanced capabilities
            await ctx.send(sender, ChatMessage(
                timestamp=datetime.now(timezone.utc),
                msg_id=uuid4(),
                content=[
                    MetadataContent(
                        type="metadata",
                        metadata={
                            "capabilities": "travel_advice,packing_lists,visa_info,vaccination_info,knowledge_graph_enhanced",
                            "knowledge_source": "asi1_llm,metta_knowledge_graph",
                            "version": "1.0.0"
                        }
                    )
                ]
            ))
            
            # Send welcome message
            welcome = (
                "Hello! I'm your Enhanced Travel FAQ Assistant powered by AI and structured knowledge. 🌍\n\n"
                "I combine:\n"
                "✅ ASI1 LLM for intelligent responses\n"
                "✅ SingularityNet's MeTTa Knowledge Graph for verified facts\n\n"
                "I can help you with:\n"
                "• Visa and entry requirements (with verified data)\n"
                "• Health requirements and vaccinations\n"
                "• Destination-specific packing lists\n"
                "• Weather and seasonal travel planning\n"
                "• Cultural customs and local etiquette\n"
                "• Currency, payments, and budget tips\n"
                "• Safety and security information\n\n"
                "Ask me anything about your travel plans! Examples:\n"
                "- 'What do I need to visit Japan?'\n"
                "- 'What vaccinations are required for Kenya?'\n"
                "- 'What should I pack for Iceland in December?'\n"
                "- 'Tell me about cultural customs in Thailand'"
            )
            await ctx.send(sender, _text(welcome))
        
        elif isinstance(content_item, EndSessionContent):
            ctx.logger.info(f"Session ended with {sender}")
            farewell = "Safe travels! Feel free to reach out anytime you need travel advice. ✈️"
            await ctx.send(sender, _text(farewell))
        
        elif isinstance(content_item, TextContent):
            user_text = sanitize_input(content_item.text)
            ctx.logger.info(f"User question from {sender}: {user_text}")
            
            if not user_text:
                await ctx.send(sender, _text("Please send me a travel question and I'll help you out!"))
                continue
            
            try:
                # Query MeTTa knowledge graph for structured information
                metta_knowledge = await metta_service.query(user_text, ctx)
                metta_context = metta_service.format_context(metta_knowledge)
                
                # Call ASI1 LLM with enhanced context
                assistant_response = await asi1_service.chat(
                    user_message=user_text,
                    system_prompt=SYSTEM_PROMPT,
                    metta_context=metta_context,
                    ctx=ctx
                )
                
                # Add knowledge source attribution if structured knowledge was used
                if metta_context:
                    assistant_response += "\n\n---\n💡 *This response is enhanced with structured knowledge from SingularityNet's MeTTa Knowledge Graph*"
                
                # Send the response
                await ctx.send(sender, _text(assistant_response))
                
            except Exception as e:
                ctx.logger.error(f"Error processing message: {e}")
                error_msg = "I encountered an error while processing your request. Please try again or rephrase your question."
                await ctx.send(sender, _text(error_msg))


@chat_proto.on_message(ChatAcknowledgement)
async def on_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle acknowledgements"""
    ctx.logger.info(f"ACK received from {sender} for message {msg.acknowledged_msg_id}")


# Include protocol and publish manifest
agent.include(chat_proto, publish_manifest=True)


if __name__ == "__main__":
    try:
        logger.info("Starting Travel FAQ Agent...")
        agent.run()
    except KeyboardInterrupt:
        logger.info("Agent stopped by user")
    except Exception as e:
        logger.error(f"Agent crashed: {e}")
        sys.exit(1)