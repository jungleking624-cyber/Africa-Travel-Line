"""
Configuration management for Travel Agent
Loads from environment variables with sensible defaults
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()


class Config:
    """Configuration class for agent settings"""
    
    def __init__(self):
        # Agent Configuration
        self.AGENT_NAME = os.getenv("AGENT_NAME", "travel_faq_assistant")
        self.AGENT_SEED = os.getenv("AGENT_SEED", self._generate_seed())
        self.PORT = int(os.getenv("PORT", "8001"))
        
        # API Keys
        self.ASI1_API_KEY = os.getenv("ASI1_API_KEY", "")
        self.METTA_API_KEY = os.getenv("METTA_API_KEY", "")
        
        # API URLs
        self.ASI1_API_URL = os.getenv("ASI1_API_URL", "https://api.asi1.ai/v1/chat/completions")
        self.METTA_API_URL = os.getenv("METTA_API_URL", "https://metta-api.singularitynet.io/v1/query")
        self.AGENTVERSE_URL = os.getenv("AGENTVERSE_URL", "https://agentverse.ai")
        
        # Agent Settings
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", "2000"))
        self.REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
        
        # Feature Flags
        self.ENABLE_METTA = os.getenv("ENABLE_METTA", "true").lower() == "true"
        self.ENABLE_LOGGING = os.getenv("ENABLE_LOGGING", "true").lower() == "true"
        
        # Directories
        self.LOG_DIR = Path(os.getenv("LOG_DIR", "logs"))
        self.LOG_DIR.mkdir(exist_ok=True)
        
        # Validate critical settings
        self._validate()
    
    def _generate_seed(self) -> str:
        """Generate a default seed if none provided"""
        import hashlib
        import socket
        
        # Use hostname + timestamp as seed base
        base = f"{socket.gethostname()}_{self.AGENT_NAME}"
        return hashlib.sha256(base.encode()).hexdigest()[:32]
    
    def _validate(self):
        """Validate critical configuration"""
        if not self.ASI1_API_KEY:
            print("⚠️  WARNING: ASI1_API_KEY not set. Agent will return errors.")
        
        if not self.METTA_API_KEY:
            print("ℹ️  INFO: METTA_API_KEY not set. Running without knowledge graph enhancement.")
        
        if self.PORT < 1024 or self.PORT > 65535:
            raise ValueError(f"Invalid PORT: {self.PORT}. Must be between 1024-65535")
    
    def __repr__(self):
        """String representation (hide sensitive data)"""
        return f"""
Travel FAQ Agent Configuration:
  Agent Name: {self.AGENT_NAME}
  Port: {self.PORT}
  ASI1 API: {'✓ Configured' if self.ASI1_API_KEY else '✗ Not Set'}
  MeTTa API: {'✓ Configured' if self.METTA_API_KEY else '✗ Not Set'}
  Log Level: {self.LOG_LEVEL}
  Log Directory: {self.LOG_DIR}
"""