from fastapi import APIRouter, HTTPException, Depends
from app.api.models.request_models import ChatRequest
from app.api.models.response_models import ChatResponse
from app.services.chat_service import ChatService
from app.core.agent import Agent

router = APIRouter()

async def get_chat_service():
    return ChatService()

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service)
):
    try:
        response = await service.process_message(
            message=request.message,
            conversation_id=request.conversation_id
        )
        return ChatResponse(
            message=response.get("message", "No response"),
            conversation_id=response.get("conversation_id") or request.conversation_id or ""
        )
    except Exception as e:
        # Return error as message
        return ChatResponse(
            message=f"Error: {str(e)}",
            conversation_id=request.conversation_id or ""
        )
