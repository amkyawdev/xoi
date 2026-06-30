from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List
from app.api.models.response_models import HistoryResponse, ConversationResponse, MessageResponse
from app.services.history_service import HistoryService

router = APIRouter()

async def get_history_service():
    return HistoryService()

@router.get("/history", response_model=HistoryResponse)
async def get_history(
    conversation_id: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: HistoryService = Depends(get_history_service)
):
    try:
        result = await service.get_history(
            conversation_id=conversation_id,
            limit=limit,
            offset=offset
        )
        return HistoryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/history")
async def create_conversation(
    service: HistoryService = Depends(get_history_service)
):
    try:
        conversation_id = await service.create_conversation()
        return {"conversation_id": conversation_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/history/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    service: HistoryService = Depends(get_history_service)
):
    try:
        result = await service.delete_conversation(conversation_id)
        if not result:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return {"message": "Conversation deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
