# API Reference

Complete API documentation for Amkyaw AI Agent backend.

## Base URL

```
Production: https://your-backend-url.onrender.com
Development: http://localhost:8000
```

## Authentication

Most endpoints require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <your-token>
```

## Endpoints

### Health Check

**GET /health**

Check if the API is running.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### Chat

**POST /api/chat**

Send a message and receive an AI response.

**Headers:**
- `Authorization: Bearer <token>` (optional)
- `Content-Type: application/json`

**Request Body:**
```json
{
  "message": "Hello, how are you?",
  "conversation_id": "optional-conversation-id",
  "context": {}
}
```

**Response:**
```json
{
  "message": "Hello! I'm doing well...",
  "conversation_id": "abc-123",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### Authentication

**POST /api/auth/login**

Authenticate a user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "user-123",
    "name": "John Doe",
    "email": "user@example.com",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

---

**POST /api/auth/register**

Register a new user.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "user-456",
    "name": "John Doe",
    "email": "user@example.com",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

---

**POST /api/auth/reset**

Request a password reset.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "Password reset email sent"
}
```

---

### History

**GET /api/history**

Get chat history.

**Query Parameters:**
- `conversation_id` (optional): Filter by conversation ID
- `limit` (optional): Number of results (default: 50, max: 100)
- `offset` (optional): Pagination offset

**Response:**
```json
{
  "conversations": [
    {
      "id": "conv-123",
      "messages": [
        {
          "id": "msg-1",
          "role": "user",
          "content": "Hello",
          "created_at": "2024-01-15T10:30:00Z"
        }
      ],
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:31:00Z"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

---

**POST /api/history**

Create a new conversation.

**Response:**
```json
{
  "conversation_id": "new-conv-id"
}
```

---

**DELETE /api/history/{conversation_id}**

Delete a conversation.

**Response:**
```json
{
  "message": "Conversation deleted"
}
```

---

### Settings

**GET /api/settings**

Get user settings.

**Response:**
```json
{
  "theme": "light",
  "language": "en",
  "notifications": true,
  "model": "gpt-4o",
  "temperature": 0.7
}
```

---

**PUT /api/settings**

Update user settings.

**Request Body:**
```json
{
  "theme": "dark",
  "temperature": 0.8
}
```

**Response:**
```json
{
  "theme": "dark",
  "language": "en",
  "notifications": true,
  "model": "gpt-4o",
  "temperature": 0.8
}
```

---

### File Upload

**POST /api/upload**

Upload a file.

**Request:**
- `Content-Type: multipart/form-data`
- Body: `file` - The file to upload

**Response:**
```json
{
  "file_id": "file-123",
  "filename": "document.pdf",
  "size": 1024000,
  "content_type": "application/pdf",
  "url": "/uploads/file-123.pdf"
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message",
  "detail": "Optional detailed error info"
}
```

**Common status codes:**
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error
