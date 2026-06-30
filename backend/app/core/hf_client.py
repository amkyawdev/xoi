"""
Hugging Face Inference API Client for AmkyawDev AI Agent
======================================================

Uses Hugging Face Inference API to run LLM inference.
API: https://api-inference.huggingface.co/models
"""

import aiohttp
import logging
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
        """Send chat completion request to Hugging Face Inference API"""
        if not self.api_key:
            return await self._fallback_response(messages)
        
        try:
            # Convert messages to conversation format
            prompt = self._build_prompt(messages)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "temperature": self.temperature,
                    "max_new_tokens": self.max_tokens,
                    "return_full_text": False,
                    "truncate": 4096
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/{self.model}",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=120)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_response(data)
                    elif response.status == 503:
                        # Model is loading
                        error_data = await response.json()
                        error_msg = error_data.get("error", "")
                        if "loading" in error_msg.lower():
                            return {
                                "message": "Model is loading. Please try again in a few seconds.",
                                "tool_calls": None,
                                "loading": True
                            }
                        logger.error(f"HF API error: {response.status} - {error_msg}")
                        return await self._fallback_response(messages)
                    else:
                        error = await response.text()
                        logger.error(f"HF API error: {response.status} - {error}")
                        return await self._fallback_response(messages)
                        
        except aiohttp.ClientError as e:
            logger.error(f"Hugging Face client error: {str(e)}")
            return await self._fallback_response(messages)
        except Exception as e:
            logger.error(f"HF unexpected error: {str(e)}")
            return await self._fallback_response(messages)
    
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
