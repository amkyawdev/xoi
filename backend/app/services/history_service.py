import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from app.core.agent import agent

class HistoryService:
    def __init__(self):
        # In-memory storage (replace with database in production)
        self.conversations: Dict[str, Dict[str, Any]] = {}

    async def get_history(
        self,
        conversation_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """Get chat history."""
        if conversation_id:
            conv = self.conversations.get(conversation_id)
            if conv:
                return {
                    "conversations": [conv],
                    "total": 1,
                    "limit": limit,
                    "offset": offset
                }
            return {
                "conversations": [],
                "total": 0,
                "limit": limit,
                "offset": offset
            }
        
        # Get all conversations, sorted by updated_at
        all_convs = sorted(
            self.conversations.values(),
            key=lambda x: x["updated_at"],
            reverse=True
        )
        
        # Apply pagination
        paginated = all_convs[offset:offset + limit]
        
        return {
            "conversations": paginated,
            "total": len(all_convs),
            "limit": limit,
            "offset": offset
        }

    async def create_conversation(self) -> str:
        """Create a new conversation."""
        conversation_id = str(uuid.uuid4())
        self.conversations[conversation_id] = {
            "id": conversation_id,
            "messages": [],
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        return conversation_id

    async def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str
    ) -> Optional[Dict[str, Any]]:
        """Add a message to a conversation."""
        if conversation_id not in self.conversations:
            return None
        
        message = {
            "id": str(uuid.uuid4()),
            "role": role,
            "content": content,
            "created_at": datetime.now()
        }
        
        self.conversations[conversation_id]["messages"].append(message)
        self.conversations[conversation_id]["updated_at"] = datetime.now()
        
        return message

    async def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation."""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False

    async def sync_with_agent(self, conversation_id: str) -> bool:
        """Sync conversation with agent's memory."""
        agent_conv = agent.get_conversation(conversation_id)
        if agent_conv:
            self.conversations[conversation_id] = {
                "id": conversation_id,
                "messages": agent_conv,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            return True
        return False

# Singleton instance
history_service = HistoryService()
