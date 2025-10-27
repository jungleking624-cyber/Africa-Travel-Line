# Backend Agent Proxy

Backend proxy agent that communicates with the Travel FAQ Assistant via agent-to-agent messaging.

## Setup

1. **Install dependencies:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and update BACKEND_AGENT_SEED
```

3. **Run the backend:**
```bash
python backend_agent.py
```

4. **Test it:**
```bash
# In another terminal
python test_backend.py
```

## Endpoints

- `GET /api/health` - Health check
- `GET /api/agent-info` - Agent information
- `POST /api/chat` - Send message to travel agent
- `GET /api/sessions/<id>` - Get session history

## Architecture