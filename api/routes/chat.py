"""Chat routes"""

from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from api.websocket import manager


router = APIRouter()


@router.websocket("/ws/{client_id}")
async def websocket_chat(websocket: WebSocket, client_id: str):
    """WebSocket chat endpoint"""
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back for now
            await manager.send_personal_message(f"Echo: {data}", client_id)
    except WebSocketDisconnect:
        manager.disconnect(client_id)


@router.post("/session/create")
async def create_session() -> dict[str, str]:
    """Create new chat session"""
    import uuid
    return {"session_id": str(uuid.uuid4())}
