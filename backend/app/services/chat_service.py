from typing import Dict, Any, Optional
from app.core.agent import agent

class ChatService:
    def __init__(self):
        self.agent = agent

    async def process_message(
        self, 
        message: str, 
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process a user message and return AI response."""
        result = await self.agent.process_message(
            message=message,
            conversation_id=conversation_id,
            context=context
        )
        return result

    async def get_conversation(self, conversation_id: str) -> list:
        """Get conversation history."""
        return self.agent.get_conversation(conversation_id)

    async def clear_conversation(self, conversation_id: str) -> bool:
        """Clear a conversation."""
        return self.agent.clear_conversation(conversation_id)

# Singleton instance
chat_service = ChatService()
