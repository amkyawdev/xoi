"""
AI Agent Core for AmkyawDev AI Agent
=====================================

Components:
1. LLM Client (Groq API integration)
2. Tool Manager (MCP, RapidAPI, Telegram)
3. Memory Manager (Conversation history)
4. Context Builder (System prompt construction)
5. Response Processor (Formatting and delivery)
6. Error Handler (Graceful failure recovery)
"""

import os
import json
import uuid
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from app.config import settings
from app.core.tools import ToolOrchestrator

logger = logging.getLogger(__name__)


class MemoryManager:
    """Manages conversation memory and context"""
    
    def __init__(self):
        self.short_term_memory: Dict[str, List[Dict]] = {}  # Current session
        self.long_term_memory: Dict[str, List[Dict]] = {}   # Persistent across sessions
    
    def add_to_short_term(self, conversation_id: str, message: Dict):
        """Add message to short-term memory (current session)"""
        if conversation_id not in self.short_term_memory:
            self.short_term_memory[conversation_id] = []
        
        message_with_meta = {
            **message,
            "timestamp": datetime.now().isoformat()
        }
        self.short_term_memory[conversation_id].append(message_with_meta)
        
        # Keep last 50 messages
        if len(self.short_term_memory[conversation_id]) > 50:
            self.short_term_memory[conversation_id].pop(0)
    
    def get_history(self, conversation_id: str, limit: int = 10) -> List[Dict]:
        """Get recent conversation history"""
        history = self.short_term_memory.get(conversation_id, [])
        return history[-limit:] if limit > 0 else history
    
    def compress_memory(self, conversation_id: str) -> str:
        """Compress conversation for context window - returns summary"""
        history = self.short_term_memory.get(conversation_id, [])
        if len(history) <= 10:
            return ""
        
        # Simple compression: keep last 5 and summarize
        recent = history[-5:]
        older = history[:-5]
        
        summary = f"[Previous {len(older)} messages summarized]: "
        summary += " | ".join([
            f"{m.get('role', 'unknown')}: {m.get('content', '')[:50]}..."
            for m in older[:3]
        ])
        return summary
    
    async def store_long_term(self, user_id: str, data: Dict):
        """Store in Neon DB (placeholder for production)"""
        if user_id not in self.long_term_memory:
            self.long_term_memory[user_id] = []
        self.long_term_memory[user_id].append(data)
    
    async def retrieve_long_term(self, user_id: str) -> List[Dict]:
        """Retrieve from Neon DB (placeholder for production)"""
        return self.long_term_memory.get(user_id, [])
    
    def clear(self, conversation_id: str):
        """Clear conversation memory"""
        if conversation_id in self.short_term_memory:
            del self.short_term_memory[conversation_id]


class GroqClient:
    """Groq API client for LLM inference"""
    
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.AI_MODEL
        self.temperature = settings.AI_TEMPERATURE
        self.max_tokens = settings.AI_MAX_TOKENS
        self.top_p = 0.95
        self.reasoning_effort = "default"
        self.base_url = "https://api.groq.com/openai/v1"
    
    async def chat(
        self, 
        messages: List[Dict], 
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send chat completion request to Groq API"""
        if not self.api_key:
            return await self._fallback_response(messages)
        
        try:
            import aiohttp
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "top_p": self.top_p,
                "reasoning_effort": self.reasoning_effort
            }
            
            if tools:
                payload["tools"] = tools
                if tool_choice:
                    payload["tool_choice"] = tool_choice
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_response(data)
                    else:
                        error = await response.text()
                        logger.error(f"Groq API error: {response.status} - {error}")
                        return await self._fallback_response(messages)
                        
        except Exception as e:
            logger.error(f"Groq client error: {str(e)}")
            return await self._fallback_response(messages)
    
    def _parse_response(self, data: Dict) -> Dict[str, Any]:
        """Parse Groq API response"""
        choices = data.get("choices", [])
        if not choices:
            return {"message": "No response generated", "tool_calls": None}
        
        choice = choices[0]
        message = choice.get("message", {})
        
        return {
            "message": message.get("content", ""),
            "tool_calls": message.get("tool_calls"),
            "finish_reason": choice.get("finish_reason")
        }
    
    async def _fallback_response(self, messages: List[Dict]) -> Dict[str, Any]:
        """Fallback response when Groq is not available"""
        raise Exception("GROQ_API_KEY not configured. Please set GROQ_API_KEY in environment variables.")


class ContextBuilder:
    """Builds system prompt with relevant skills and context"""
    
    def __init__(self):
        self.default_system_prompt = """You are AmkyawDev AI Agent, an intelligent assistant powered by advanced AI.

Core Capabilities:
- Natural language understanding and generation
- Code writing, debugging, and explanation
- Research and information synthesis
- Multi-step problem solving
- File operations and analysis

Guidelines:
- Be helpful, harmless, and honest
- Think step by step for complex problems
- Ask clarifying questions when needed
- Provide accurate, well-reasoned responses
- Code should be clean, documented, and follow best practices
- Admit uncertainty when you don't know something

You have access to tools for:
- Web search and research
- Code execution
- File read/write operations
- Calculations and analysis
- External API calls

Always prioritize user privacy and security."""
    
    async def build(
        self, 
        user_input: str, 
        user_id: Optional[str] = None,
        skills: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Build complete context for LLM"""
        messages = [{"role": "system", "content": self.default_system_prompt}]
        
        # Add relevant skills if available
        if skills:
            skills_context = self._format_skills(skills)
            if skills_context:
                messages.append({
                    "role": "system", 
                    "content": f"Available Skills:\n{skills_context}"
                })
        
        # Add user context if available
        if user_id:
            messages.append({
                "role": "system",
                "content": f"User ID: {user_id}"
            })
        
        return {"messages": messages, "system_prompt": self.default_system_prompt}
    
    def _format_skills(self, skills: Dict) -> str:
        """Format skills for system prompt"""
        lines = []
        for category, skill_list in skills.items():
            if skill_list:
                lines.append(f"\n{category.upper()}:")
                for skill in skill_list[:5]:  # Limit to 5 per category
                    if hasattr(skill, 'name'):
                        lines.append(f"- {skill.name}: {skill.description}")
        return "\n".join(lines)


class ResponseProcessor:
    """Processes and formats LLM responses"""
    
    def __init__(self):
        self.max_message_length = 10000
    
    def process(self, response: Dict[str, Any], user_id: Optional[str] = None) -> Dict[str, Any]:
        """Process and format response"""
        message = response.get("message", "")
        
        # Truncate if too long
        if len(message) > self.max_message_length:
            message = message[:self.max_message_length] + "\n\n[Response truncated]"
        
        return {
            "message": message,
            "tool_calls": response.get("tool_calls"),
            "success": True
        }


class ErrorHandler:
    """Handles errors gracefully"""
    
    def __init__(self):
        self.error_count = 0
    
    def handle(self, error: Exception, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Handle error and return user-friendly message"""
        self.error_count += 1
        logger.error(f"Agent error ({self.error_count}): {str(error)}", extra=context)
        
        return {
            "message": f"Error: {str(error)}",
            "error": str(error),
            "success": False
        }


class Agent:
    """
    AI Agent Architecture for AmkyawDev AI Agent
    ============================================
    
    Main processing pipeline:
    1. Build context with skills
    2. Get LLM response with tools
    3. Handle tool calls if any
    4. Process and return response
    """
    
    def __init__(self):
        self.llm_client = GroqClient()
        self.tool_manager = ToolOrchestrator()
        self.memory_manager = MemoryManager()
        self.context_builder = ContextBuilder()
        self.response_processor = ResponseProcessor()
        self.error_handler = ErrorHandler()
        self.conversation_history: Dict[str, List[Dict]] = {}
        self.max_iterations = 5  # Prevent infinite tool loops
    
    async def process(
        self, 
        user_input: str, 
        user_id: Optional[str] = None,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Main processing pipeline"""
        try:
            conversation_id = conversation_id or self._generate_id()
            
            # Initialize conversation if needed
            if conversation_id not in self.conversation_history:
                self.conversation_history[conversation_id] = []
            
            # Add user message to history
            self.conversation_history[conversation_id].append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now().isoformat()
            })
            
            # Build context with skills
            context = await self.context_builder.build(
                user_input=user_input,
                user_id=user_id
            )
            
            # Build messages for LLM
            messages = context["messages"]
            
            # Add conversation history (last 10 messages with compression)
            history = self.conversation_history[conversation_id][-10:]
            messages.extend(history)
            
            # Get tools definition
            tools = self.tool_manager.get_tools()
            
            # Get initial LLM response
            response = await self.llm_client.chat(
                messages=messages,
                tools=tools if tools else None
            )
            
            # Handle tool calls if present
            tools_used = []
            iteration = 0
            
            while response.get("tool_calls") and iteration < self.max_iterations:
                iteration += 1
                
                # Add assistant message with tool calls
                tool_message = {
                    "role": "assistant",
                    "content": response.get("message", ""),
                    "tool_calls": response["tool_calls"]
                }
                messages.append(tool_message)
                
                # Execute tools
                for tool_call in response["tool_calls"]:
                    tool_name = tool_call.get("function", {}).get("name")
                    tool_args = json.loads(tool_call.get("function", {}).get("arguments", "{}"))
                    
                    result = await self.tool_manager.execute_tool(tool_name, tool_args)
                    tools_used.append(tool_name)
                    
                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.get("id"),
                        "content": json.dumps(result)
                    })
                
                # Get next LLM response
                response = await self.llm_client.chat(
                    messages=messages,
                    tools=tools if tools else None
                )
            
            # Add assistant response to history
            self.conversation_history[conversation_id].append({
                "role": "assistant",
                "content": response.get("message", ""),
                "timestamp": datetime.now().isoformat()
            })
            
            # Update memory manager
            self.memory_manager.add_to_short_term(conversation_id, {
                "role": "user",
                "content": user_input
            })
            self.memory_manager.add_to_short_term(conversation_id, {
                "role": "assistant",
                "content": response.get("message", "")
            })
            
            # Process response
            processed = self.response_processor.process(
                response=response,
                user_id=user_id
            )
            
            return {
                "message": processed["message"],
                "conversation_id": conversation_id,
                "tools_used": tools_used,
                "success": True
            }
            
        except Exception as e:
            return self.error_handler.handle(e, {"user_input": user_input})

    async def process_message(
        self, 
        message: str, 
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Backward-compatible method"""
        user_id = context.get("user_id") if context else None
        return await self.process(
            user_input=message,
            user_id=user_id,
            conversation_id=conversation_id
        )

    def _generate_id(self) -> str:
        """Generate unique ID for conversation"""
        return str(uuid.uuid4())

    def get_conversation(self, conversation_id: str) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history.get(conversation_id, [])

    def clear_conversation(self, conversation_id: str) -> bool:
        """Clear a conversation"""
        if conversation_id in self.conversation_history:
            del self.conversation_history[conversation_id]
            self.memory_manager.clear(conversation_id)
            return True
        return False


# Singleton instance
agent = Agent()
