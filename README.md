# Amkyaw AI Agent

A minimalist AI agent application built with modern web technologies. The project features a clean, distraction-free interface with a FastAPI backend.

## Features

- **Clean Chat Interface** - Minimalist design focused on conversations
- **User Authentication** - Login, registration, and password reset
- **Real-time Responses** - Streaming AI responses
- **Chat History** - Save and load conversation history
- **Code Support** - Code highlighting and formatting
- **Responsive Design** - Works on desktop and mobile
- **MCP Integration** - Model Context Protocol support for extended capabilities

## Tech Stack

### Frontend
- Vanilla JavaScript (ES6+)
- CSS3 with CSS Variables
- No external frameworks (lightweight & fast)

### Backend
- Python 3.11+
- FastAPI
- Pydantic
- JWT Authentication

## Project Structure

```
amkyawdev-ai-agent/
├── frontend/
│   ├── public/           # Static assets
│   ├── src/
│   │   ├── css/          # Stylesheets
│   │   ├── js/           # JavaScript modules
│   │   └── pages/        # HTML pages
│   └── vercel.json
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Core agent logic
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utilities
│   └── requirements.txt
├── docs/                 # Documentation
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js (optional, for development)
- PostgreSQL (optional, for production)

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file:
   ```bash
   cp .env.example .env
   ```

5. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

The frontend can be deployed directly to Vercel or served statically.

1. Deploy to Vercel:
   ```bash
   cd frontend
   vercel
   ```

2. Or serve locally with any static server:
   ```bash
   python -m http.server 8000
   ```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | - |
| `SECRET_KEY` | JWT secret key | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `AI_MODEL` | AI model to use | gpt-4o |
| `BROWSERLESS_API_KEY` | Browserless API key | - |
| `RAPIDAPI_KEY` | RapidAPI key | - |

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/reset` - Password reset

### Chat
- `POST /api/chat` - Send message

### History
- `GET /api/history` - Get chat history
- `POST /api/history` - Create new conversation
- `DELETE /api/history/{id}` - Delete conversation

### Settings
- `GET /api/settings` - Get user settings
- `PUT /api/settings` - Update settings

### Upload
- `POST /api/upload` - Upload file

## License

MIT License - see LICENSE file for details.
