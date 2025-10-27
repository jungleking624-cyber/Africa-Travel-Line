"""
Data models for the Travel FAQ Agent
"""

from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class TravelQuery(BaseModel):
    """Model for incoming travel queries"""
    query: str
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict] = None


class TravelResponse(BaseModel):
    """Model for agent responses"""
    response: str
    enhanced: bool = False
    metta_used: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: str
    message_id: UUID = Field(default_factory=uuid4)


class KnowledgeFact(BaseModel):
    """Model for MeTTa knowledge facts"""
    entity: str
    relations: List[Dict] = []
    properties: Dict = {}
    confidence: float = 0.0


class SessionState(BaseModel):
    """Model for user session state"""
    session_id: str
    user_address: str
    started_at: datetime
    last_activity: datetime
    message_count: int = 0
    context: List[Dict] = []