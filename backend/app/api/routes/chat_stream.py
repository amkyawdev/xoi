"""
Streaming Chat Endpoint for real-time AI responses
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.api.models.request_models import ChatRequest
from app.core.agent import agent
import json
import asyncio
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


async def generate_streaming_response(message: str, conversation_id: str = None):
    """
    Generate streaming response using SSE (Server-Sent Events)
    """
    try:
        # Start processing
        yield f"data: {json.dumps({'type': 'start', 'conversation_id': conversation_id})}\n\n"
        
        # Process message through agent
        result = await agent.process_message(
            message=message,
            conversation_id=conversation_id
        )
        
        # Stream the response word by word (simulated streaming)
        response_text = result.get("message", "")
        
        # Send in chunks
        chunk_size = 20
        for i in range(0, len(response_text), chunk_size):
            chunk = response_text[i:i + chunk_size]
            yield f"data: {json.dumps({'type': 'content', 'content': chunk})}\n\n"
            await asyncio.sleep(0.01)  # Small delay for smooth streaming
        
        # Send completion
        yield f"data: {json.dumps({'type': 'done', 'conversation_id': result.get('conversation_id')})}\n\n"
        
    except Exception as e:
        logger.error(f"Streaming error: {str(e)}")
        yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint - returns AI response as Server-Sent Events.
    
    Use this for real-time typing effect responses.
    """
    return StreamingResponse(
        generate_streaming_response(
            message=request.message,
            conversation_id=request.conversation_id
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )


@router.get("/chat/models")
async def list_available_models():
    """
    List available AI models for configuration
    """
    return {
        "models": [
            {
                "id": "mixtral-8x7b-32768",
                "name": "Mixtral 8x7B",
                "provider": "Groq",
                "context_length": 32768
            },
            {
                "id": "llama-3.1-70b-versatile",
                "name": "Llama 3.1 70B",
                "provider": "Groq",
                "context_length": 128000
            },
            {
                "id": "llama-3.1-8b-instant",
                "name": "Llama 3.1 8B",
                "provider": "Groq",
                "context_length": 128000
            },
            {
                "id": "gemma2-9b-it",
                "name": "Gemma 2 9B",
                "provider": "Groq",
                "context_length": 8192
            }
        ]
    }
