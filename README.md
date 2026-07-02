# AmkyawDev AI Agent - Web Agent Platform

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-red.svg)

### бЂЎбЂ†бЂ„бЂ·бЂєбЂ™бЂјбЂ„бЂ·бЂє AI Agent - Advanced AI Assistant & Web Agent Platform

A powerful, minimalist AI agent application built with modern web technologies. Features a clean, distraction-free interface with a FastAPI backend, plus comprehensive web agent capabilities for crawling, scraping, and intelligent task automation.

[Features](#features) вЂў [Tech Stack](#tech-stack) вЂў [Getting Started](#getting-started) вЂў [Documentation](#documentation) вЂў [License](#license)

</div>

---

## вњЁ Features

| Feature | Description |
|---------|-------------|
| ржд' **Smart Chat** | Clean, intuitive chat interface with real-time AI responses |
| ржд" **User Authentication** | Secure login, registration, and password reset |
| ржд№ **Chat History** | Save and load conversation history |
| ржд» **Code Support** | Syntax highlighting and code formatting |
| рждЌ **Web Search** | Built-in web search capabilities |
| ржд– **AI Agent** | Intelligent agent powered by Groq/HuggingFace |
| ржд± **Responsive Design** | Works perfectly on desktop and mobile |
| ржд§ **MCP Integration** | Model Context Protocol for extended capabilities |
| рждЊ **Browser Automation** | Automated web browsing with Browserless |
| ржд¤ **Telegram Bot** | Send messages directly to Telegram |

### Web Agent Platform Features

| Feature | Description |
|---------|-------------|
| р№Њ **Web Crawling** | Intelligent web crawling with Playwright and HTTP support |
| рanno **Smart Search** | Web search integration with multiple engines |
| роб **AI Agents** | LLM-powered agents with planning and execution |
| рчх **Interactive Chat** | Real-time chat with AI assistants via WebSocket |
| раБ **RAG Capabilities** | Retrieval-augmented generation with ChromaDB |
| рум **Security** | JWT authentication, rate limiting, encryption |
| раЦ **Monitoring** | Prometheus metrics, tracing, health checks |
| рук **Extensible** | Modular architecture for easy extension |

---

## ржд™ Tech Stack

### Frontend
- **Vanilla JavaScript** (ES6+) - Lightweight & fast
- **CSS3** with CSS Variables - Modern styling
- **Bootstrap 5** - Responsive layout
- **AOS Animations** - Smooth page transitions

### Backend
- **Python 3.11+** - Modern Python
- **FastAPI** - High-performance web framework
- **Pydantic** - Data validation
- **JWT Authentication** - Secure user sessions
- **Groq API** - Fast AI inference
- **HuggingFace** - Alternative AI backend
- **PostgreSQL** - Database support

### Web Agent Platform Stack
- **Playwright** - Browser automation
- **BeautifulSoup4** - HTML parsing
- **OpenAI/Anthropic** - LLM providers
- **ChromaDB** - Vector storage
- **Celery** - Task queue
- **Redis** - Caching
- **Structured Logging** - Monitoring

---

## рждЉ Web Agent Platform Architecture

```
web-agent-platform/
в”њв”Ђв”Ђ cli/                    # Command-line interface
в”‚   в””в”Ђв”Ђ commands/          # CLI commands (ask, chat, crawl, etc.)
в”œв”‚
в”œв”‚ agent/                    # AI agent with planning and execution
в”‚   в”œв”‚ planner.py           # Task planning
в”‚   в”œв”‚ executor.py          # Task execution
в”‚   в”œв”‚ reasoning.py         # Reasoning engine
в”‚   в”œв”‚ workflow.py           # Workflow orchestration
в”‚   в”œв”‚ memory.py             # Memory management
в”‚   в””в”‚ tools.py             # Tool registry
в”œв”‚
в”œв”‚ llm/                      # LLM client with provider routing
в”‚   в”œв”‚ client.py            # Main LLM client
в”‚   в”œв”‚ router.py            # Model router
в”‚   в”œв”‚ providers/           # Provider implementations
в”‚   в””в”‚ models.py            # Data models
в”œв”‚
в”œв”‚ crawler/                  # Web crawling and scraping
в”‚   в”œв”‚ browser.py           # Playwright browser management
в”‚   в”œв”‚ fetcher.py           # HTTP fetching
в”‚   в”œв”‚ parser.py            # HTML parsing
в”‚   в”œв”‚ extractor.py         # Content extraction
в”‚   в”œв”‚ cleaner.py           # HTML cleaning
в”‚   в”œв”‚ markdown.py          # HTML to Markdown
в”‚   в”œв”‚ robots.py            # Robots.txt parsing
в”‚   в””в”‚ sitemap.py           # Sitemap parsing
в”œв”‚
в”œв”‚ rag/                      # RAG (Retrieval Augmented Generation)
в”‚   в”œв”‚ chunker.py           # Text chunking
в”‚   в”œв”‚ embedding.py         # Embedding generation
в”‚   в”œв”‚ vector_store.py      # ChromaDB integration
в”‚   в”œв”‚ retriever.py         # Document retrieval
в”‚   в””в”‚ generator.py         # RAG response generation
в”œв”‚
в”œв”‚ api/                      # FastAPI REST API
в”‚   в”œв”‚ server.py            # Main server
в”‚   в”œв”‚ routes/              # API endpoints
в”‚   в”œв”‚ schemas/             # Pydantic models
в”‚   в”œв”‚ websocket.py          # WebSocket handling
в”‚   в””в”‚ middleware/          # Middleware
в”œв”‚
в”œв”‚ database/                  # Database connections
в”‚   в”œв”‚ sqlite.py            # SQLite support
в”‚   в”œв”‚ postgres.py          # PostgreSQL support
в”‚   в”œв”‚ redis.py             # Redis support
в”‚   в”œв”‚ chroma.py             # ChromaDB wrapper
в”‚   в””в”‚ migrations/          # Database migrations
в”œв”‚
в”œв”‚ logger/                   # Structured logging
в”œв”‚ monitoring/               # Metrics, tracing, health checks
в”œв”‚ security/                 # JWT, encryption, rate limiting
в”œв”‚ cache/                    # Memory and Redis caching
в”œв”‚ scheduler/                # Task queue and cron scheduling
в”œв”‚ config/                   # Application settings
в”œв”‚ storage/                  # File storage directories
в”œв”‚ tests/                    # Unit and integration tests
в”œв”‚ scripts/                  # Shell scripts
в””в”‚ docs/                     # Documentation
```

---

## рждЌ Getting Started

### Prerequisites

- Python 3.11+
- Node.js (optional, for local development)
- PostgreSQL (optional, for production)

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run server
uvicorn app.main:app --reload
```

### Web Agent Platform Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install --with-deps chromium

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run API server
uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload

# Or use Docker
docker-compose up -d
```

---

## ржд" Environment Variables

| Variable | Description | Required |
|----------|------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | No |
| `SECRET_KEY` | JWT secret key | Yes |
| `GROQ_API_KEY` | Groq API key for AI | Yes |
| `HF_API_KEY` | HuggingFace API key | No |
| `AI_MODEL` | AI model to use | No |
| `BROWSERLESS_API_KEY` | Browserless API key | No |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | No |
| `RAPIDAPI_KEY` | RapidAPI key | No |
| `YOUTUBE_API_KEY` | YouTube Data API key | No |
| `OPENAI_API_KEY` | OpenAI API key (Web Agent) | No |
| `OPENROUTER_API_KEY` | OpenRouter API key | No |
| `REDIS_URL` | Redis connection string | No |

---

## ржд“ Documentation

### API Endpoints

#### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration  
- `POST /api/auth/reset` - Password reset

#### Chat
- `POST /api/chat` - Send message
- `POST /api/chat/stream` - Streaming chat (SSE)
- `GET /api/chat/models` - List available models

#### History
- `GET /api/history` - Get chat history
- `POST /api/history` - Create new conversation
- `DELETE /api/history/{id}` - Delete conversation

#### Settings
- `GET /api/settings` - Get user settings
- `PUT /api/settings` - Update settings

#### Upload
- `POST /api/upload` - Upload file

### Web Agent API Endpoints

#### Health
- `GET /api/health` - Health check
- `GET /api/health/ready` - Readiness check
- `GET /api/health/live` - Liveness check

#### AI
- `POST /api/ai/chat` - Send chat message
- `POST /api/ai/chat/stream` - Stream chat response

#### Crawler
- `POST /api/crawler/scrape` - Scrape single URL
- `POST /api/crawler/crawl` - Crawl website

#### Search
- `POST /api/search` - Search the web

### CLI Commands

```bash
# Ask a question
wap ask "What is machine learning?"

# Start a chat session
wap chat --session my-session

# Crawl a website
wap crawl https://example.com --depth 3

# Search the web
wap search "Python tutorial" --limit 10

# List available models
wap models --provider openai

# Check API health
wap health
```

---

## ржд" Project Structure

### Original App Structure
```
xoi/
в”œв”‚ frontend/
в”‚   в”œв”‚ public/
в”‚   в”‚   в””в”‚ images/
в”‚   в”‚       в””в”‚ animations/     # SVG animations
в”‚   в”œв”‚ src/
в”‚   в”‚   в”œв”‚ css/               # Stylesheets
в”‚   в”‚   в””в”‚ js/                # JavaScript modules
в”‚   в””в”‚ pages/                 # HTML pages
в”œв”‚ backend/
в”‚   в””в”‚ app/
в”‚       в”œв”‚ api/               # API routes & models
в”‚       в”œв”‚ core/               # Agent, tools, clients
в”‚       в”œв”‚ services/          # Business logic
в”‚       в”œв”‚ database/           # DB models
в”‚       в””в”‚ utils/             # Helpers
в”œв”‚ docs/                      # Documentation
в””в”‚ README.md
```

---

## ржд”— Related Repositories

- [agent-skills](https://github.com/amkyawdev/agent-skills) - OpenHands compatible AI skills
- [ai-brain-skills](https://github.com/amkyawdev/ai-brain-skills) - Advanced AI skills

---

## ржд„ License

MIT License - see [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with вќ¤пёЏ by [AmkyawDev](https://github.com/amkyawdev)**

</div>
