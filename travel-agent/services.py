"""
External API service integrations
- ASI1 LLM for natural language responses
- MeTTa Knowledge Graph for verified facts
"""

import httpx
from typing import Optional, Dict, Any
from datetime import datetime


class ASI1Service:
    """ASI1 LLM API service"""
    
    def __init__(self, api_key: str, api_url: str = "https://api.asi1.ai/v1/chat/completions"):
        self.api_key = api_key
        self.api_url = api_url
        self.model = "gpt-4o-mini"
        self.timeout = 30.0
    
    async def chat(
        self, 
        user_message: str, 
        system_prompt: str,
        metta_context: str = "",
        ctx=None
    ) -> str:
        """Call ASI1 LLM API with the user's travel question"""
        if not self.api_key:
            return "Error: ASI1 API key not configured. Please set ASI1_API_KEY environment variable."
        
        # Construct enhanced prompt with structured knowledge
        enhanced_message = user_message
        if metta_context:
            enhanced_message = f"{metta_context}\n\nUser Question: {user_message}\n\nPlease answer using the structured knowledge above when relevant, and cite it as 'According to verified data'."
        
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
                    assistant_reply = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    return assistant_reply if assistant_reply else "I apologize, but I couldn't generate a response. Please try again."
                elif response.status_code == 401:
                    return "Error: Invalid ASI1 API key. Please check your configuration."
                else:
                    if ctx:
                        ctx.logger.error(f"ASI1 API error {response.status_code}: {response.text}")
                    return f"I'm experiencing technical difficulties (API error {response.status_code}). Please try again in a moment."
                    
        except httpx.TimeoutException:
            if ctx:
                ctx.logger.error("ASI1 API timeout")
            return "The request timed out. Please try asking a shorter question or try again later."
        except Exception as e:
            if ctx:
                ctx.logger.error(f"ASI1 API call failed: {e}")
            return "I encountered an error while processing your request. Please try again."


class MeTTaService:
    """SingularityNet MeTTa Knowledge Graph service"""
    
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.api_url = api_url
        self.timeout = 10.0
    
    async def query(self, query: str, ctx=None) -> Optional[Dict]:
        """Query MeTTa knowledge graph for structured travel information"""
        if not self.api_key:
            if ctx:
                ctx.logger.warning("MeTTa API key not configured, skipping knowledge graph query")
            return None
        
        try:
            query_payload = {
                "query": query,
                "domains": ["travel", "geography", "health", "culture"],
                "max_results": 5,
                "include_relations": True
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=query_payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if ctx:
                        ctx.logger.info(f"MeTTa knowledge retrieved: {len(data.get('results', []))} results")
                    return data
                elif response.status_code == 404:
                    if ctx:
                        ctx.logger.info("MeTTa API endpoint not available, using fallback knowledge")
                    return None
                else:
                    if ctx:
                        ctx.logger.warning(f"MeTTa API returned {response.status_code}")
                    return None
                    
        except httpx.TimeoutException:
            if ctx:
                ctx.logger.warning("MeTTa API timeout, continuing without structured knowledge")
            return None
        except Exception as e:
            if ctx:
                ctx.logger.warning(f"MeTTa query failed: {e}, continuing without structured knowledge")
            return None
    
    def format_context(self, knowledge: Optional[Dict]) -> str:
        """Format MeTTa knowledge graph results for LLM context"""
        if not knowledge or not knowledge.get("results"):
            return ""
        
        context_parts = ["\n\n=== STRUCTURED KNOWLEDGE FROM KNOWLEDGE GRAPH ==="]
        
        for idx, result in enumerate(knowledge.get("results", [])[:5], 1):
            context_parts.append(f"\n[Fact {idx}]")
            
            # Add entity information
            if "entity" in result:
                context_parts.append(f"Entity: {result['entity']}")
            
            # Add relationships
            if "relations" in result:
                for rel in result["relations"]:
                    context_parts.append(f"  - {rel.get('predicate', 'related_to')}: {rel.get('object', 'N/A')}")
            
            # Add properties
            if "properties" in result:
                for key, value in result["properties"].items():
                    context_parts.append(f"  {key}: {value}")
            
            # Add confidence score if available
            if "confidence" in result:
                context_parts.append(f"  Confidence: {result['confidence']}")
        
        context_parts.append("\n=== END STRUCTURED KNOWLEDGE ===\n")
        return "\n".join(context_parts)