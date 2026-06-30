import os
import json
from typing import Dict, List, Optional, Any
from app.config import settings
from app.core.tools import ToolOrchestrator

class Agent:
    def __init__(self):
        self.tools = ToolOrchestrator()
        self.conversation_history: Dict[str, List[Dict]] = {}
        self.system_prompt = """You are Amkyaw, a helpful AI assistant. You are designed to be helpful, harmless, and honest.

Guidelines:
- Be friendly and professional
- Provide accurate information
- Admit when you don't know something
- Ask clarifying questions when needed
- Be concise but thorough
- Code should be clean and well-documented

You have access to various tools for:
- Web search and research
- Code execution and debugging
- File operations
- And more

Always think step by step and explain your reasoning."""

    async def process_message(
        self, 
        message: str, 
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        conversation_id = conversation_id or self._generate_id()
        
        # Initialize conversation if needed
        if conversation_id not in self.conversation_history:
            self.conversation_history[conversation_id] = []
        
        # Add user message to history
        self.conversation_history[conversation_id].append({
            "role": "user",
            "content": message
        })
        
        # Build messages for AI
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add conversation history (last 10 messages)
        history = self.conversation_history[conversation_id][-10:]
        messages.extend(history)
        
        # Add context if provided
        if context:
            context_msg = f"Context: {json.dumps(context)}"
            messages.append({"role": "system", "content": context_msg})
        
        # Determine if tools should be used
        should_use_tools = self._should_use_tools(message)
        
        if should_use_tools:
            response = await self._process_with_tools(messages)
        else:
            response = await self._generate_response(messages)
        
        # Add assistant response to history
        self.conversation_history[conversation_id].append({
            "role": "assistant",
            "content": response["message"]
        })
        
        return {
            "message": response["message"],
            "conversation_id": conversation_id,
            "tools_used": response.get("tools_used", [])
        }

    def _should_use_tools(self, message: str) -> bool:
        tool_keywords = [
            "search", "find", "lookup", "research", "web",
            "run", "execute", "code", "python", "script",
            "file", "read", "write", "create",
            "calculate", "compute", "analyze",
            "weather", "news", "latest", "current"
        ]
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in tool_keywords)

    async def _process_with_tools(self, messages: List[Dict]) -> Dict[str, Any]:
        # Simple response without actual tool execution for demo
        # In production, this would use OpenAI function calling
        response = await self._generate_response(messages)
        response["tools_used"] = []
        return response

    async def _generate_response(self, messages: List[Dict]) -> Dict[str, Any]:
        # Placeholder for actual AI API call
        # In production, this would call OpenAI or another AI provider
        last_message = messages[-1]["content"] if messages else ""
        
        # Simple response logic
        response_text = self._generate_simple_response(last_message)
        
        return {
            "message": response_text,
            "tools_used": []
        }

    def _generate_simple_response(self, message: str) -> str:
        message_lower = message.lower()
        
        if "hello" in message_lower or "hi" in message_lower:
            return "Hello! I'm Amkyaw, your AI assistant. How can I help you today?"
        elif "how are you" in message_lower:
            return "I'm doing great, thank you for asking! I'm here and ready to help you with any questions or tasks you have."
        elif "thank" in message_lower:
            return "You're welcome! Is there anything else I can help you with?"
        elif "bye" in message_lower or "goodbye" in message_lower:
            return "Goodbye! Feel free to come back anytime you need assistance."
        elif "help" in message_lower:
            return """I can help you with various tasks:

• Answering questions on any topic
• Writing and editing content
• Code assistance and debugging
• Research and information retrieval
• File operations
• And much more!

Just let me know what you need help with."""
        else:
            return f"I understand you're asking about: \"{message[:50]}...\"\n\nI'm a simple demo response. In production, I would use advanced AI models to provide detailed, helpful answers to your questions.\n\nTry asking me about:\n- Writing or editing text\n- Technical questions\n- Research topics\n- Or anything else you're curious about!"

    def _generate_id(self) -> str:
        import uuid
        return str(uuid.uuid4())

    def get_conversation(self, conversation_id: str) -> List[Dict]:
        return self.conversation_history.get(conversation_id, [])

    def clear_conversation(self, conversation_id: str) -> bool:
        if conversation_id in self.conversation_history:
            del self.conversation_history[conversation_id]
            return True
        return False

# Singleton instance
agent = Agent()
