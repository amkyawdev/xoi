from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from app.api.models.request_models import ChatRequest
from app.api.models.response_models import ChatResponse
from app.services.chat_service import ChatService
from app.core.agent import Agent
from app.core.limiter import limiter
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

async def get_chat_service():
    return ChatService()

@router.post("/chat", response_model=ChatResponse)
@limiter.limit("30/minute")
async def chat(
    request: Request,
    request_data: ChatRequest,
    service: ChatService = Depends(get_chat_service)
):
    try:
        response = await service.process_message(
            message=request_data.message,
            conversation_id=request_data.conversation_id
        )
        return ChatResponse(
            message=response.get("message", "No response"),
            conversation_id=response.get("conversation_id") or request_data.conversation_id or ""
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")
