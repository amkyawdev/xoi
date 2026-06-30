# Amkyaw AI Agent - Backend API

FastAPI-based backend for the Amkyaw AI Agent application.

## Features

- 🤖 **AI Chat** - Groq LLM integration with streaming support
- 🔐 **Authentication** - JWT-based auth with bcrypt password hashing
- 💬 **Chat History** - Conversation management with pagination
- 📁 **File Upload** - Secure file handling
- 🔧 **Tool Orchestration** - Web search, social media, browser automation
- 📱 **Social Media** - TikTok, YouTube, Facebook integration
- 💾 **Database** - PostgreSQL/Neon support with async

## Quick Start

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your API keys

# Run server
uvicorn app.main:app --reload
```

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | No |
| `SECRET_KEY` | JWT secret key | Yes |
| `GROQ_API_KEY` | Groq API key | Yes |
| `YOUTUBE_API_KEY` | YouTube Data API key | No |
| `RAPIDAPI_KEY` | RapidAPI key | No |
| `BROWSERLESS_API_KEY` | Browserless API key | No |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | No |

## API Endpoints

### Chat
- `POST /api/chat` - Send message
- `POST /api/chat/stream` - Streaming chat (SSE)
- `GET /api/chat/models` - List available models

### Auth
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/reset` - Password reset

### History
- `GET /api/history` - Get chat history
- `POST /api/history` - Create conversation
- `DELETE /api/history/{id}` - Delete conversation

### Settings
- `GET /api/settings` - Get settings
- `PUT /api/settings` - Update settings

### Upload
- `POST /api/upload` - Upload file
- `GET /api/files/{id}` - Get file
- `DELETE /api/files/{id}` - Delete file

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry
│   ├── config.py            # Settings
│   ├── api/
│   │   ├── models/         # Pydantic models
│   │   └── routes/          # API endpoints
│   ├── core/
│   │   ├── agent.py        # AI Agent
│   │   ├── tools.py        # Tool orchestrator
│   │   ├── dependencies.py  # Auth dependencies
│   │   └── *.py            # API clients
│   ├── services/            # Business logic
│   ├── database/            # DB models & connection
│   └── utils/              # Helpers
├── requirements.txt
└── .env.example
```

## Streaming Chat Example

```javascript
const response = await fetch('/api/chat/stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: 'Hello!' })
});

const reader = response.body.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  const data = new TextDecoder().decode(value);
  // Parse SSE data: data: {"type": "content", "content": "..."}
}
```

## License

MIT
