"""AI routes"""

from fastapi import APIRouter, Depends

from api.dependencies import LLMDep
from api.schemas import ChatRequest, ChatResponse


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, llm: LLMDep) -> ChatResponse:
    """Send chat message to AI"""
    from llm.models import Message
    
    messages = [Message(**m) for m in request.messages]
    response = await llm.chat(
        messages=messages,
        model=request.model,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=False
    )
    
    return ChatResponse(**response)


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest, llm: LLMDep):
    """Stream chat response"""
    from fastapi.responses import StreamingResponse
    from llm.models import Message
    
    messages = [Message(**m) for m in request.messages]
    
    async def generate():
        async for chunk in llm.chat(
            messages=messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=True
        ):
            yield f"data: {chunk}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")
