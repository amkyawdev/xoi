"""
Hugging Face Inference API Client for AmkyawDev AI Agent
======================================================

Uses Hugging Face Inference API to run LLM inference.
API: https://api-inference.huggingface.co/models
"""

import aiohttp
import logging
import urllib.parse
from typing import Dict, List, Any, Optional
from app.config import settings

logger = logging.getLogger(__name__)


class HuggingFaceClient:
    """Hugging Face Inference API client for LLM inference"""
    
    def __init__(self):
        self.api_key = settings.HF_API_KEY
        self.model = settings.AI_MODEL
        self.temperature = settings.AI_TEMPERATURE
        self.max_tokens = settings.AI_MAX_TOKENS
        self.base_url = settings.HF_INFERENCE_ENDPOINT
    
    async def chat(
        self, 
        messages: List[Dict], 
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send chat completion request using Groq API"""
        from app.config import settings
        
        # Use GROQ_API_KEY from settings (or HF_TOKEN as fallback)
        api_key = settings.GROQ_API_KEY
        groq_model = settings.GROQ_MODEL
        
        logger.info(f"GROQ_API_KEY set: {bool(api_key)}")
        logger.info(f"Using Groq API with model: {groq_model}")
        
        if not api_key:
            raise Exception("GROQ_API_KEY not configured")
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            # Use Groq API directly
            api_url = "https://api.groq.com/openai/v1/chat/completions"
            payload = {
                "model": groq_model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
            logger.info(f"Calling Groq API: {api_url}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    api_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=120)
                ) as response:
                    status = response.status
                    logger.info(f"Groq API response status: {status}")
                    
                    if status == 200:
                        data = await response.json()
                        return self._parse_groq_response(data)
                    else:
                        error = await response.text()
                        logger.error(f"Groq API error {status}: {error[:500]}")
                        raise Exception(f"Groq API error {status}: {error[:500]}")
                        
        except aiohttp.ClientError as e:
            logger.error(f"Groq client error: {str(e)}")
            raise Exception(f"Groq connection error: {str(e)}")
        except Exception as e:
            logger.error(f"Groq error: {str(e)}")
            raise
    
    def _build_prompt(self, messages: List[Dict]) -> str:
        """Build prompt from messages for text generation models"""
        prompt_parts = []
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"<|system|>\n{content}")
            elif role == "user":
                prompt_parts.append(f"<|user|>\n{content}")
            elif role == "assistant":
                prompt_parts.append(f"<|assistant|>\n{content}")
        
        # Add assistant prefix for generation
        prompt_parts.append("<|assistant|>\n")
        
        return "\n".join(prompt_parts)
    
    def _parse_response(self, data: Any) -> Dict[str, Any]:
        """Parse Hugging Face API response"""
        try:
            if isinstance(data, list) and len(data) > 0:
                generated_text = data[0].get("generated_text", "")
            elif isinstance(data, dict):
                generated_text = data.get("generated_text", "")
            else:
                return {"message": "No response generated", "tool_calls": None}
            
            # Clean up the response
            generated_text = generated_text.strip()
            
            return {
                "message": generated_text,
                "tool_calls": None,  # HF Inference API doesn't support tools natively
                "finish_reason": "stop"
            }
        except Exception as e:
            logger.error(f"Error parsing HF response: {str(e)}")
            return {"message": "Error parsing response", "tool_calls": None}

    def _parse_hf_space_response(self, data: Any) -> Dict[str, Any]:
        """Parse Hugging Face Spaces API response"""
        try:
            # HF Spaces /api/agents/chat/chat returns {"response": "...", ...}
            if isinstance(data, dict):
                message = data.get("response", "") or data.get("text", "") or data.get("message", "")
                if message:
                    return {
                        "message": message.strip(),
                        "tool_calls": None,
                        "finish_reason": "stop"
                    }
            return {"message": "No response generated", "tool_calls": None}
        except Exception as e:
            logger.error(f"Error parsing HF Space response: {str(e)}")
            return {"message": "Error parsing response", "tool_calls": None}

    def _parse_groq_response(self, data: Any) -> Dict[str, Any]:
        """Parse Groq API response"""
        try:
            if isinstance(data, dict) and "choices" in data:
                choices = data["choices"]
                if choices and len(choices) > 0:
                    message = choices[0].get("message", {})
                    content = message.get("content", "")
                    return {
                        "message": content.strip() if content else "",
                        "tool_calls": None,
                        "finish_reason": choices[0].get("finish_reason", "stop")
                    }
            return {"message": "No response generated", "tool_calls": None}
        except Exception as e:
            logger.error(f"Error parsing Groq response: {str(e)}")
            return {"message": "Error parsing response", "tool_calls": None}
    
    async def _fallback_response(self, messages: List[Dict]) -> Dict[str, Any]:
        """Fallback response when Hugging Face is not available"""
        if not self.api_key:
            raise Exception("HF_API_KEY not configured. Please set HF_API_KEY in environment variables.")
        else:
            raise Exception("Hugging Face API is unavailable. Please try again later.")
    
    async def check_model_status(self) -> Dict[str, Any]:
        """Check if model is loaded and ready"""
        if not self.api_key:
            return {"status": "error", "message": "API key not configured"}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/{self.model}",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "status": "ready",
                            "model": data.get("model_id", self.model)
                        }
                    elif response.status == 503:
                        return {"status": "loading", "message": "Model is loading"}
                    else:
                        return {"status": "error", "message": f"HTTP {response.status}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}


# Singleton instance
hf_client = HuggingFaceClient()
