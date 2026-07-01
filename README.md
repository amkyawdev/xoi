# AmkyawDev AI Agent

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-red.svg)

### အဆင့်မြင့် AI Agent - Advanced AI Assistant

A powerful, minimalist AI agent application built with modern web technologies. Features a clean, distraction-free interface with a FastAPI backend.

[Features](#features) • [Tech Stack](#tech-stack) • [Getting Started](#getting-started) • [Documentation](#documentation) • [License](#license)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💬 **Smart Chat** | Clean, intuitive chat interface with real-time AI responses |
| 🔐 **User Authentication** | Secure login, registration, and password reset |
| 📜 **Chat History** | Save and load conversation history |
| 💻 **Code Support** | Syntax highlighting and code formatting |
| 🔍 **Web Search** | Built-in web search capabilities |
| 🤖 **AI Agent** | Intelligent agent powered by Groq/HuggingFace |
| 📱 **Responsive Design** | Works perfectly on desktop and mobile |
| 🔧 **MCP Integration** | Model Context Protocol for extended capabilities |
| 🌐 **Browser Automation** | Automated web browsing with Browserless |
| 📤 **Telegram Bot** | Send messages directly to Telegram |

---

## 🛠 Tech Stack

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

---

## 🚀 Getting Started

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

### Frontend Setup

```bash
# Deploy to Vercel
cd frontend
vercel

# Or serve locally
python -m http.server 8000
```

---

## 🔑 Environment Variables

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

---

## 📚 Documentation

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

---

## 📁 Project Structure

```
xoi/
├── frontend/
│   ├── public/
│   │   └── images/
│   │       └── animations/     # SVG animations
│   ├── src/
│   │   ├── css/               # Stylesheets
│   │   └── js/                # JavaScript modules
│   └── pages/                 # HTML pages
├── backend/
│   └── app/
│       ├── api/               # API routes & models
│       ├── core/               # Agent, tools, clients
│       ├── services/          # Business logic
│       ├── database/           # DB models
│       └── utils/             # Helpers
├── docs/                      # Documentation
└── README.md
```

---

## 🔗 Related Repositories

- [agent-skills](https://github.com/amkyawdev/agent-skills) - OpenHands compatible AI skills
- [ai-brain-skills](https://github.com/amkyawdev/ai-brain-skills) - Advanced AI skills

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ by [AmkyawDev](https://github.com/amkyawdev)**

</div>
