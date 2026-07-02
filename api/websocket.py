"""WebSocket handling"""

from typing import Any

from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str) -> None:
        """Connect a new client"""
        await websocket.accept()
        self.active_connections[client_id] = websocket
    
    def disconnect(self, client_id: str) -> None:
        """Disconnect a client"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
    
    async def send_personal_message(self, message: str, client_id: str) -> None:
        """Send message to specific client"""
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)
    
    async def broadcast(self, message: str) -> None:
        """Broadcast message to all clients"""
        for connection in self.active_connections.values():
            await connection.send_text(message)
    
    async def send_json(self, data: dict[str, Any], client_id: str) -> None:
        """Send JSON to client"""
        import json
        await self.send_personal_message(json.dumps(data), client_id)


# Global connection manager
manager = ConnectionManager()
