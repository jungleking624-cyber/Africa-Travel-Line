# 🌍 Travel FAQ Assistant - Local Development

AI-powered travel advisor agent enhanced with SingularityNet's MeTTa Knowledge Graph.

## Features

- ✅ ASI1 LLM for intelligent responses
- ✅ MeTTa Knowledge Graph for verified facts
- ✅ Chat Protocol implementation
- ✅ Mailbox connectivity to Agentverse
- ✅ Local development and testing
- ✅ Production-ready error handling

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your favorite editor
```

### 3. Run the Agent

```bash
# Run locally with mailbox
python agent.py
```

The agent will:

- Start on port 8001 (configurable in .env)
- Connect to Agentverse via mailbox
- Display agent address in console
- Begin processing chat messages

## Configuration

Edit `.env` file:

| Variable        | Required | Description                                  |
| --------------- | -------- | -------------------------------------------- |
| `ASI1_API_KEY`  | Yes      | Your ASI1 LLM API key                        |
| `METTA_API_KEY` | Optional | MeTTa knowledge graph key                    |
| `AGENT_SEED`    | Yes      | Unique seed phrase (generates agent address) |
| `PORT`          | No       | Agent port (default: 8001)                   |

## Testing

```bash
# Run unit tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_agent.py::test_chat_message
```

## Project Structure
