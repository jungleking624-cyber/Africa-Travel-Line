# Africa-Travel-Line - Fetch.ai Hackathon

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

![tag:avmcp](https://img.shields.io/badge/avmcp-6C63FF) ![tag:ai-powered](https://img.shields.io/badge/AI_Powered-00D4AA) ![tag:travel](https://img.shields.io/badge/Travel-FF6B6B)

**An intelligent travel planning platform for Africa powered by AI agents and modern web technologies**

Africa Travel Line is a comprehensive travel planning ecosystem that combines a responsive web frontend, robust API backend, and an AI-powered travel assistant agent. The platform helps travelers discover destinations, plan trips, and get personalized travel advice enhanced with verified knowledge from SingularityNet's MeTTa Knowledge Graph.

---

## 🎯 Project Overview

Africa Travel Line is a **three-tier architecture** consisting of:

1. **Frontend Web Application** - User-facing interface for browsing destinations and interacting with the AI travel assistant
2. **Backend API Server** - RESTful API handling business logic, data management, and integrations
3. **AI Travel Agent** - Intelligent agent powered by ASI1 LLM and MeTTa Knowledge Graph providing verified travel information

### Key Capabilities

- 🔍 **Destination Discovery** - Browse and search African travel destinations
- 🤖 **AI Travel Advisor** - Get personalized travel advice powered by dual AI systems
- ✅ **Verified Information** - Travel requirements backed by structured knowledge graphs
- 💬 **Interactive Chat** - Real-time conversation with the travel assistant
- 📱 **Responsive Design** - Seamless experience across desktop and mobile devices
- 🌐 **Multi-Agent System** - Leverages Fetch.ai's agent framework for distributed intelligence

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                        │
│                  (React/Next.js Web App)                 │
└────────────────────────┬────────────────────────────────┘
                         │
                         │ HTTPS/REST API
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   BACKEND API SERVER                     │
│              (Node.js/Express + Database)                │
└────────────────────────┬────────────────────────────────┘
                         │
                         │ uAgents Protocol
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  AI TRAVEL AGENT                         │
│        (Fetch.ai Agent + ASI1 LLM + MeTTa KG)           │
│                                                          │
│  ┌──────────────┐      ┌─────────────────┐             │
│  │  ASI1 LLM    │◄────►│  MeTTa Knowledge│             │
│  │  (Neural AI) │      │  Graph (Symbolic)│             │
│  └──────────────┘      └─────────────────┘             │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
africa-travel-line/
│
├── frontend(Africa-Travel-line)/                    # Frontend Web Application
│   ├── public/                 # Static assets (images, icons)
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/             # React Typescript pages/routes
│   │   ├── styles/            # CSS/styling files
│   │   ├── type/              # Auth Interface
|   |── index.html
│   ├── package.json           # Frontend dependencies
│   └── README.md              # Frontend-specific docs
│
├── backend(server)/           # Backend API Server
│   ├── src/
│   │   ├── routes/            # API route handlers
│   │   ├── config/            # Configuring database
│   │
|   |── app.js
|   |── index.js               # Root node app
│   ├── package.json           # Backend dependencies
│   └── README.md              # Backend-specific docs
│
├── travel-agent/                # AI Travel Agent (Fetch.ai)
│   ├── agent.py               # Main agent code with Chat Protocol
│   ├── config.py              # Configuration management
│   ├── services.py            # ASI1 & MeTTa API integrations
│   ├── models.py              # Data models for agent
│   ├── utils.py               # Helper functions
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables template
│   └── README.md              # Agent-specific docs
│
├── .gitignore                  # Git ignore rules
├── package.json               # Root workspace configuration
└── README.md                  # This file - main project documentation
```

---

## 🤖 AI Travel Agent Details

### Agent Information

- **Agent Name:** Travel Assistant (MeTTa Enhanced)
- **Agent Address:** `agent1qwatl9nznqul3nldvh59lu7ph53fpm4r3y4t5t9ku352d3ur7lkscgzp6vy`
- **Wallet Address:** `fetch1f4k3akwuexxwhtuj3fdne7jwesatzagy8vhf6r`
- **Network:** Testnet
- **Status:** ✅ Live & Running
- **Type:** Mailbox Agent (Accessible from Agentverse)

### Dual AI Intelligence

The Travel Agent uses a **hybrid AI architecture** combining:

1. **ASI1 LLM (Neural AI)**

   - Natural language understanding
   - Contextual responses
   - Flexible conversation handling
   - Personalized recommendations

2. **SingularityNet MeTTa Knowledge Graph (Symbolic AI)**
   - Verified travel facts
   - Structured knowledge about destinations
   - Geographic and cultural information
   - Requirements and regulations

### Agent Capabilities

The AI Travel Agent can help with:

✅ **Visa & Entry Requirements**

- Visa policies by nationality
- Entry requirements and documentation
- Passport validity rules
- Visa exemptions and on-arrival options

✅ **Health & Safety**

- Required vaccinations by destination
- Health advisories and recommendations
- Medical facility information
- Travel insurance guidance

✅ **Destination Information**

- Climate and weather patterns
- Best times to visit
- Cultural customs and etiquette
- Local laws and regulations

✅ **Practical Travel Tips**

- Currency and exchange information
- Power adapter requirements (voltage/plug types)
- Transportation options
- Communication (SIM cards, WiFi)
- Accommodation recommendations

✅ **Packing Assistance**

- Climate-appropriate clothing lists
- Essential documents checklist
- Electronics and adapters
- Health and safety items
- Destination-specific needs

### Example Interactions

**User:** "What do I need to visit Kenya?"

**Agent Response:**

> According to verified data from the knowledge graph:
>
> **Visa Requirements for Kenya:**
>
> - US citizens: eVisa required (apply online at evisa.go.ke)
> - UK citizens: eVisa required
> - Processing time: 2-7 business days
> - Cost: $50 USD for single-entry tourist visa
> - Passport validity: 6+ months from entry date
> - Confidence: 0.94
>
> **Health Requirements:**
>
> - Yellow fever vaccination required (certificate must be shown)
> - Malaria prophylaxis recommended
> - Hepatitis A & Typhoid vaccines recommended
>
> **Packing Essentials:**
>
> - Light, breathable clothing (tropical climate)
> - Sunscreen (SPF 30+) and insect repellent
> - Power adapter: Type G (240V)
> - Travel insurance with medical coverage
>
> **Currency & Payments:**
>
> - Currency: Kenyan Shilling (KES)
> - Credit cards widely accepted in cities
> - Carry cash for rural areas
>
> ---
>
> 💡 _This response is enhanced with structured knowledge from SingularityNet's MeTTa Knowledge Graph_

---

**User:** "What should I pack for Morocco in winter?"

**Agent Response:**

> According to verified data:
>
> **Morocco Weather in Winter (Dec-Feb):**
>
> - Temperature: 8°C to 18°C (46°F to 64°F) - varies by region
> - Climate: Mild in coastal areas, cold in Atlas Mountains
> - Rainfall: Moderate, especially in December
> - Confidence: 0.91
>
> **Packing List:**
>
> Clothing:
>
> - Layers (mornings/evenings can be chilly)
> - Light jacket or sweater
> - Long pants and long-sleeve shirts
> - Scarf (useful for warmth and modesty)
> - Comfortable walking shoes
> - Warm coat if visiting Atlas Mountains
>
> Documents:
>
> - Passport (6+ months validity)
> - Visa: Not required for US/EU citizens (90-day exemption)
> - Travel insurance documents
> - Hotel confirmations
>
> Electronics:
>
> - Power adapter: Type C/E (220V)
> - Phone/camera with chargers
> - Portable battery pack
>
> Health & Safety:
>
> - Sunscreen (strong sun even in winter)
> - Hand sanitizer
> - Basic first-aid kit
> - Prescription medications
>
> Other:
>
> - Reusable water bottle
> - Day backpack
> - Money belt or secure wallet
> - Phrasebook or translation app
>
> ---
>
> 💡 _Weather data from MeTTa Knowledge Graph, packing recommendations from travel expertise_

### How to Interact with the Agent

**Option 1: Via Agentverse Chat**

1. Go to [Agentverse Chat](https://agentverse.ai)
2. Enter agent address: `agent1qwatl9nznqul3nldvh59lu7ph53fpm4r3y4t5t9ku352d3ur7lkscgzp6vy` or search "travel-ai"
3. Navigate to "Chat with Agent"
4. Start asking your travel questions!
   ![av travel agent](https://raw.githubusercontent.com/jungleking624-cyber/Africa-Travel-Line/refs/heads/main/travel-agent/images/av1.png)

---

## ![av travel agent2](https://raw.githubusercontent.com/jungleking624-cyber/Africa-Travel-Line/refs/heads/main/travel-agent/images/av2.png)

![av travel agent3](https://raw.githubusercontent.com/jungleking624-cyber/Africa-Travel-Line/refs/heads/main/travel-agent/images/av3.png)

**Option 2: Via Africa Travel Line Platform**

- Use the integrated chat interface in the web application
- The frontend communicates with the agent via the backend API

**Option 3: Programmatic Access**

```python
from uagents import Agent
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent
from datetime import datetime, timezone
from uuid import uuid4

# Send message to travel agent

await ctx.send(
"agent1qwatl9nznqul3nldvh59lu7ph53fpm4r3y4t5t9ku352d3ur7lkscgzp6vy",
ChatMessage(
timestamp=datetime.now(timezone.utc),
msg_id=uuid4(),
content=[TextContent(type="text", text="What vaccinations do I need for Tanzania?")]
)
)
```

**Option 4: Test Agents with ASI:One:**
![asi one](https://raw.githubusercontent.com/jungleking624-cyber/Africa-Travel-Line/refs/heads/main/travel-agent/images/asi1%20llm.png)

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** 16+ and npm/yarn (for frontend and backend)
- **Python** 3.8+ (for AI agent)
- **Git** for version control

### Environment Variables

Each component requires specific environment variables. Copy the example files and configure:

**Frontend** (`frontend/.env.local`):

```bash
PUBLIC_API_URL=http://localhost:5173/
PUBLIC_AGENT_ADDRESS=agent1qwatl9nznqul3nldvh59lu7ph53fpm4r3y4t5t9ku352d3ur7lkscgzp6vy
```

**Backend** (`backend/.env`):

```bash
PORT=3000
DATABASE_URL=db_url
AGENT_ADDRESS=agent1qwatl9nznqul3nldvh59lu7ph53fpm4r3y4t5t9ku352d3ur7lkscgzp6vy
JWT_SECRET=your_jwt_secret_here
CORS_ORIGIN=http://localhost:5000
```

**AI Agent** (`travel-agent/.env`):

```bash
AGENT_NAME=travel_assistant
AGENT_SEED=your_unique_secret_seed_phrase_
PORT=8001
ASI1_API_KEY=your_asi1_api_key_here
METTA_API_KEY=your_metta_api_key_here
AGENTVERSE_URL=https://agentverse.ai
```

### Installation & Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/jungleking624-cyber/Africa-Travel-Line.git
cd africa-travel-line
```

#### 2. Setup Frontend

```bash
cd Africa-Travel-line
npm install
cp  .env.local
# Edit .env.local with your configuration
npm run dev
```

The frontend will be available at `http://localhost:5173`

#### 3. Setup Backend

```bash
cd ../server
npm install
cp  .env
# Edit .env with your configuration
npm run dev
```

The backend API will be available at `http://localhost:3000`. The Flask will be available at Port 5000.

#### 4. Setup AI Agent

```bash
cd ../travel-agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp  .env
# Edit .env with your API keys
python agent.py
```

The agent will start and connect to Agentverse mailbox.

---

## 🌐 Frontend Application

### Technology Stack

- **Framework:** Typescript (React )
- **UI Components:** Custom components + Tailwind CSS
- **State Management:** React Context API / Redux (if applicable)
- **HTTP Client:** Axios / Fetch API
- **Form Handling:** React Hook Form
- **Styling:** Tailwind CSS + CSS Modules

### Key Features

- 🏠 **Home Page** - Showcase featured African destinations
- 🔍 **Search & Filter** - Find destinations by region, activities, budget (Still in process because of time limit)
- 📍 **Destination Pages** - Detailed information about each location
- 💬 **AI Chat Interface** - Interactive travel assistant
- 👤 **User Profiles** - Save favorites and trip plans
- 📱 **Responsive Design** - Mobile-first approach

### Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run test         # Run tests
```

---

## 🔧 Backend API Server

### Technology Stack

- **Runtime:** Node.js
- **Framework:** Express.js
- **Database:** Postgresql (with pgAdmin)
- **Authentication:** JWT (JSON Web Tokens)
- **Validation:** Joi / Express Validator
- **Testing:** Jest + Supertest

### API Endpoints

#### Users & Authentication

```

POST /register # Register new user
POST /login # Login user
GET /api/auth/me # Get current user
GET /profile # User profile

```

#### AI Agent Integration

```

POST /api/chat # Send message to AI agent
GET /api/health # Check health endpoint
GET /api/agent-info # Get agent information
GET /api/sessions/<session_id> # Get session history
POST /api/chat/session # Start chat session
```

### Middleware

- **Authentication** - JWT verification
- **Rate Limiting** - Prevent abuse
- **CORS** - Cross-origin resource sharing
- **Error Handling** - Centralized error responses
- **Request Validation** - Input sanitization
- **Logging** - Request/response logging

### Available Scripts

```bash
npm run dev          # Start development server with nodemon
npm run start        # Start production server
npm run test         # Run tests
npm run lint         # Run ESLint
npm run seed         # Seed database with sample data
```

---

## 🤖 AI Travel Agent (Fetch.ai)

### Technology Stack

- **Framework:** uAgents (v0.22.9)
- **Core Protocol:** uAgents-core (v0.3.9)
- **Chat Protocol:** Fetch.ai Agent Chat Protocol
- **LLM Integration:** ASI1 API
- **Knowledge Graph:** SingularityNet MeTTa
- **HTTP Client:** httpx (async)
- **Environment:** Python 3.8+

### Architecture

The agent implements a **hybrid intelligence** system:

```python
# Simplified agent flow
@chat_proto.on_message(ChatMessage)
async def on_chat(ctx: Context, sender: str, msg: ChatMessage):
    # 1. ACK immediately
    await ctx.send(sender, ChatAcknowledgement(...))

    # 2. Query MeTTa Knowledge Graph for verified facts
    metta_knowledge = await metta_service.query(user_question)
    metta_context = format_structured_knowledge(metta_knowledge)

    # 3. Call ASI1 LLM with enhanced context
    response = await asi1_service.chat(
        user_message=user_question,
        system_prompt=TRAVEL_ADVISOR_PROMPT,
        metta_context=metta_context
    )

    # 4. Add attribution and send response
    if metta_context:
        response += "\n\n💡 Enhanced with MeTTa Knowledge Graph"

    await ctx.send(sender, ChatMessage(content=[TextContent(text=response)]))
```

### Key Components

**agent.py** - Main agent implementation

- Chat Protocol handlers
- Session management (start/end)
- Message routing and ACK handling
- Integration orchestration

**services.py** - External API integrations

- `ASI1Service` - LLM API calls with retry logic
- `MeTTaService` - Knowledge graph queries
- Error handling and graceful degradation

**config.py** - Configuration management

- Environment variable loading
- API endpoint configuration
- Feature flags
- Validation

**models.py** - Data models

- Pydantic models for type safety
- Request/response schemas
- Session state management

**utils.py** - Helper functions

- Input sanitization
- Logging setup
- Destination extraction
- Error formatting

### Configuration

**Required Environment Variables:**

```bash
# Agent Identity
AGENT_NAME=travel_assistant
AGENT_SEED=<your-unique-seed>
PORT=8001

# API Keys (Required)
ASI1_API_KEY=<your-asi1-key>          # Required for responses
METTA_API_KEY=<your-metta-key>        # METTA do not have api key at this time

# API Endpoints
ASI1_API_URL=https://api.asi1.ai/v1/chat/completions
METTA_API_URL=https://metta-api.singularitynet.io/v1/query
AGENTVERSE_URL=https://agentverse.ai

# Agent Settings
LOG_LEVEL=INFO
MAX_MESSAGE_LENGTH=2000
REQUEST_TIMEOUT=30
ENABLE_METTA=true
```

### Running the Agent

**Local Development:**

```bash
cd travel-agent
source venv/bin/activate
python agent.py
```

**Agentverse Hosted:**

- Upload code to Agentverse
- Set secrets in Agentverse UI
- Start agent from dashboard

**Docker:**

```bash
docker build -t travel-agent .
docker run -d --env-file .env travel-agent
```

### Testing the Agent

```bash
# Run agent
python agent.py

# Test backend-agent for Frontend integration (In another terminal)
cd /backend-agent-proxy
python backend_agent.py

```

**Manual Testing via Agentverse:**

1. Go to https://agentverse.ai
2. Search the agent address "agent1qwatl9nznqul3nldvh59lu7ph53fpm4r3y4t5t9ku352d3ur7lkscgzp6vy" ot travel assistant
3. Click the agent
4. Click "Chat with Agent"
5. Send test messages:
   - "What do I need for Egypt?"
   - "Best time to visit South Africa?"
   - "Vaccinations for Tanzania?"

---

## 🎯 Use Cases

### 1. Trip Planning

**Scenario:** User planning a 2-week trip to Morocco

**Interaction:**

- User browses Morocco on the website
- Clicks "Ask AI Assistant"
- Asks: "Help me plan a 2-week Morocco itinerary"

**Agent Response:**

- Suggests cities (Marrakech, Fes, Casablanca, Chefchaouen)
- Provides day-by-day breakdown
- Includes travel times between cities
- Recommends activities for each location
- Suggests best times to visit each city

### 2. Visa & Requirements Check

**Scenario:** US citizen checking requirements for Kenya

**Interaction:**

- User: "I'm from the US, what do I need to visit Kenya?"

**Agent Response:**

- eVisa requirement (with link)
- Processing time and cost
- Passport validity rules
- Yellow fever certificate requirement
- Travel insurance recommendations
- Currency and payment info

### 3. Health & Safety Information

**Scenario:** Traveler concerned about vaccinations for West Africa

**Interaction:**

- User: "What vaccinations do I need for Nigeria?"

**Agent Response:**

- Required: Yellow fever (with certificate)
- Recommended: Hepatitis A, Typhoid, Malaria prophylaxis
- Optional: Hepatitis B, Rabies
- Health facility information
- Travel insurance with medical coverage

### 4. Packing Assistance

**Scenario:** First-time traveler to sub-Saharan Africa

**Interaction:**

- User: "What should I pack for a safari in Tanzania?"

**Agent Response:**

- Clothing (neutral colors, layers)
- Sun protection (hat, sunscreen, sunglasses)
- Camera equipment
- Binoculars
- Insect repellent
- First aid kit
- Power adapters
- Documents checklist

### 5. Cultural Etiquette

**Scenario:** Business traveler to Ethiopia

**Interaction:**

- User: "What cultural customs should I know for Ethiopia?"

**Agent Response:**

- Greeting customs (handshakes, bowing)
- Dining etiquette
- Dress codes (conservative)
- Religious considerations
- Business meeting protocols
- Gift-giving practices
- Photography rules

---

## 🔒 Security & Privacy

### Authentication

- JWT-based authentication for backend API
- Secure password hashing (bcrypt)
- Token expiration and refresh mechanisms

### Data Protection

- User data encrypted at rest
- HTTPS for all communications
- Secure environment variable management
- No storage of sensitive payment information

### Agent Security

- Agent identity managed via secure seed phrases
- API keys stored as environment variables
- Rate limiting on agent endpoints
- Input sanitization and validation

### Best Practices

- Regular dependency updates
- Security audits
- GDPR compliance considerations
- Data retention policies

---

## 🧪 Testing

### Frontend Testing

```bash
cd frontend
npm run dev               # Run frontend app
```

### Backend Testing

```bash
cd backend
npm run dev               # Run backend app
```

### Agent Testing

```bash
cd travel-agent
pytest                    # Run all tests
pytest tests/test_agent.py # Specific test file
pytest --cov              # With coverage
pytest -v                 # Verbose output
```

### Manual Testing Checklist

**Frontend:**

- [ ] Homepage loads correctly
- [ ] Search functionality works
- [ ] Destination pages display properly (Limited destinations)
- [ ] Chat interface connects to agent
- [ ] Mobile responsive design verified
- [ ] Forms validate correctly
- [ ] User authentication works

**Backend:**

- [ ] All API endpoints return expected responses
- [ ] Authentication and authorization work
- [ ] Database CRUD operations succeed
- [ ] Error handling returns proper status codes
- [ ] Rate limiting functions correctly
- [ ] CORS configured properly

**AI Agent:**

- [ ] Agent starts successfully
- [ ] Responds to chat messages
- [ ] MeTTa knowledge graph queries work
- [ ] ASI1 LLM integration functional
- [ ] Session management works
- [ ] Error handling graceful
- [ ] ACK pattern followed correctly

---

## 🎨 Tech Stack Summary

### Frontend

- **Framework:** Typescript react
- **Language:** Javascript
- **Styling:** Tailwind CSS
- **State:** React Context API
- **HTTP:** Axios
- **Forms:** React Hook Form
- **Testing:** Jest, React Testing Library

### Backend

- **Runtime:** Node.js
- **Framework:** Express.js
- **Language:** TypeScript/JavaScript
- **Database:** PostgreSQL
- **Auth:** JWT, bcrypt
- **Validation:** Joi
- **Testing:** Jest, Supertest

### AI Agent

- **Framework:** uAgents (Fetch.ai)
- **Language:** Python 3.8+
- **LLM:** ASI1 API
- **Knowledge:** MeTTa Knowledge Graph
- **HTTP:** httpx
- **Validation:** Pydantic
- **Testing:** pytest

### Infrastructure

- **Frontend Hosting:** Vercel / Netlify
- **Backend Hosting:** Railway / Heroku / AWS
- **Database:** MongoDB Atlas
- **Agent Hosting:** Agentverse / VPS
- **CI/CD:** GitHub Actions

---

## 🐛 Troubleshooting

### Frontend Issues

**Build fails:**

```bash
# Clear cache and reinstall
rm -rf .next node_modules
npm install
npm run build
```

**API connection errors:**

- Verify backend is running
- Check CORS configuration on backend

### Backend Issues

**Database connection fails:**

- Verify `DATABASE_URL` is correct
- Have a pgAdmin and all unique credentials

**Port already in use:**

```bash
# Kill process on port 3001
lsof -ti:3001 | xargs kill -9
```

### Agent Issues

**Agent won't start:**

- Check Python version (3.8+)
- Verify all dependencies installed
- Check `PORT` is available
- Review logs for specific errors

**No responses from agent:**

- Verify `ASI1_API_KEY` is set correctly
- Check internet connection
- Review agent logs for API errors
- Test API keys with curl

**MeTTa not working:**

- Optional feature, agent works without it
- You don't need to check `METTA_API_KEY` because it is not available currently
- Logs will show if MeTTa queries succeed

**Common Error Messages:**

| Error                    | Solution                                  |
| ------------------------ | ----------------------------------------- |
| "API Key Not Configured" | Set `ASI1_API_KEY` in environment         |
| "Invalid API Key"        | Verify API key is correct and active      |
| "Connection timeout"     | Check network, increase `REQUEST_TIMEOUT` |
| "Module not found"       | Run `pip install -r requirements.txt`     |

---

### Code Review Checklist

- [ ] Code follows project style guide
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] No console.logs or debug code
- [ ] Environment variables documented
- [ ] Error handling implemented
- [ ] Security considerations addressed

---

## 📚 Additional Resources

### Documentation Links

- **Fetch.ai uAgents:** https://fetch.ai/docs
- **Agentverse Platform:** https://agentverse.ai/docs
- **ASI1 API:** https://asi1.ai/docs
- **SingularityNet MeTTa:** https://metta-lang.dev
- **Next.js:** https://nextjs.org/docs
- **Express.js:** https://expressjs.com

### Community & Support

- **GitHub Issues:** Report bugs and request features
- **Discord:** Join our community server
- **Fetch.ai Discord:** https://discord.gg/fetchai

---

## 🎯 Limitations & Scope

### What the Platform Does

✅ Provides verified travel information for African destinations
✅ Offers AI-powered travel advice and recommendations
✅ Helps plan trips and create itineraries
✅ Gives visa, vaccination, and health requirement information
✅ Suggests packing lists and practical travel tips
✅ Shares cultural customs and etiquette guidance

### What the Platform Does NOT Do (Because of Time contraints)

❌ **Not a Booking Platform** - Does not handle flight/hotel reservations
❌ **Not Real-Time Updates** - Travel information may not reflect daily changes
❌ **Not Legal Advice** - Always verify official government sources
❌ **Not Medical Advice** - Consult healthcare professionals for health needs
❌ **Not Travel Insurance** - Recommends but doesn't provide insurance
❌ **Not Emergency Services** - Contact local authorities for emergencies
❌ **Limited Geographic Scope** - Focuses on African destinations only (But the agent has no Geographical limitation)
❌ **No Payment Processing** - No financial transactions handled

### Important Disclaimers

⚠️ **Verify Requirements:** Always check official embassy/consulate websites for latest visa and entry requirements.

⚠️ **Health Consultation:** Consult a travel medicine specialist for personalized vaccination advice.

⚠️ **Travel Advisories:** Check government travel advisories before departure.

⚠️ **Insurance Required:** We strongly recommend comprehensive travel insurance.

⚠️ **AI Limitations:** AI responses are informative but may not cover every scenario. Use as a guide, not definitive source.

---

## 🏷️ Keywords & Tags

**Domain:** Travel, Tourism, Africa, AI Assistant, Trip Planning

**Technologies:** Node.js, Express.js, Python, Fetch.ai, uAgents, AI Agents, LLM, Knowledge Graph

**Features:** Destination Discovery, Travel Advice, Visa Information, Packing Lists, Cultural Etiquette, Health Requirements

**Use Cases:** Trip Planning, Travel Research, Requirements Check, Packing Assistance, Cultural Learning

**Regions:** Africa, North Africa, West Africa, East Africa, Southern Africa, Central Africa

**Integration Points:** Chat Protocol, Agentverse, ASI1, MeTTa, REST API, Agent Communication

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Contributors

- **Project Lead:** [HOSEA]
- **Team Developer:** [JOSHUA]

---

## 🙏 Acknowledgments

- **Fetch.ai** for the uAgents framework and Agentverse platform
- **SingularityNet** for MeTTa Knowledge Graph technology
- **ASI1** for LLM API access
- **Open Source Community** for various libraries and tools

---

## 📧 Contact

- **Website:**---
- **Email:** izuchukwunwali09@gmail.com
- **GitHub:** https://https://github.com/jungleking624-cyber/Africa-Travel-Line
- **Twitter:** @---

---

**Built with ❤️ for ASI Agents Track hackathon**

_Last Updated: October 2025_
