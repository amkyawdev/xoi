import aiohttp
import logging
from typing import Dict, Any, List
from app.config import settings

logger = logging.getLogger(__name__)

class TelegramClient:
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.enabled = bool(self.bot_token)
        logger.info(f"Telegram Client initialized: enabled={self.enabled}")

    async def send_message(self, chat_id: str, text: str, parse_mode: str = "HTML") -> Dict[str, Any]:
        """Send a message to a Telegram chat."""
        if not self.enabled:
            return {
                "error": "Telegram bot not configured. TELEGRAM_BOT_TOKEN not set.",
                "available": False
            }
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/sendMessage"
                payload = {
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": parse_mode
                }
                
                async with session.post(
                    url, 
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "message_id": data.get("result", {}).get("message_id"),
                            "chat_id": chat_id,
                            "success": True,
                            "available": True
                        }
                    else:
                        error = await response.json()
                        return {"error": error.get("description", "Unknown error"), "available": True}
        except Exception as e:
            logger.error(f"Telegram send_message error: {str(e)}")
            return {"error": str(e), "available": True}

    async def send_photo(self, chat_id: str, photo_url: str, caption: str = "") -> Dict[str, Any]:
        """Send a photo to a Telegram chat."""
        if not self.enabled:
            return {
                "error": "Telegram bot not configured. TELEGRAM_BOT_TOKEN not set.",
                "available": False
            }
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/sendPhoto"
                payload = {
                    "chat_id": chat_id,
                    "photo": photo_url,
                    "caption": caption,
                    "parse_mode": "HTML"
                }
                
                async with session.post(
                    url, 
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "message_id": data.get("result", {}).get("message_id"),
                            "success": True,
                            "available": True
                        }
                    else:
                        error = await response.json()
                        return {"error": error.get("description", "Unknown error"), "available": True}
        except Exception as e:
            logger.error(f"Telegram send_photo error: {str(e)}")
            return {"error": str(e), "available": True}

    async def send_document(self, chat_id: str, document_url: str, caption: str = "") -> Dict[str, Any]:
        """Send a document to a Telegram chat."""
        if not self.enabled:
            return {
                "error": "Telegram bot not configured. TELEGRAM_BOT_TOKEN not set.",
                "available": False
            }
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/sendDocument"
                payload = {
                    "chat_id": chat_id,
                    "document": document_url,
                    "caption": caption,
                    "parse_mode": "HTML"
                }
                
                async with session.post(
                    url, 
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "message_id": data.get("result", {}).get("message_id"),
                            "success": True,
                            "available": True
                        }
                    else:
                        error = await response.json()
                        return {"error": error.get("description", "Unknown error"), "available": True}
        except Exception as e:
            logger.error(f"Telegram send_document error: {str(e)}")
            return {"error": str(e), "available": True}

    async def get_updates(self, offset: int = 0, limit: int = 100) -> Dict[str, Any]:
        """Get updates from Telegram."""
        if not self.enabled:
            return {
                "error": "Telegram bot not configured. TELEGRAM_BOT_TOKEN not set.",
                "available": False
            }
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/getUpdates"
                payload = {
                    "offset": offset,
                    "limit": limit,
                    "timeout": 60
                }
                
                async with session.post(
                    url, 
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=65)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {"updates": data.get("result", []), "success": True, "available": True}
                    else:
                        return {"error": f"HTTP {response.status}", "available": True}
        except Exception as e:
            logger.error(f"Telegram get_updates error: {str(e)}")
            return {"error": str(e), "available": True}

    async def set_webhook(self, webhook_url: str) -> Dict[str, Any]:
        """Set a webhook for the bot."""
        if not self.enabled:
            return {
                "error": "Telegram bot not configured. TELEGRAM_BOT_TOKEN not set.",
                "available": False
            }
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/setWebhook"
                payload = {"url": webhook_url}
                
                async with session.post(
                    url, 
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        return {"success": True, "available": True}
                    else:
                        return {"error": f"HTTP {response.status}", "available": True}
        except Exception as e:
            logger.error(f"Telegram set_webhook error: {str(e)}")
            return {"error": str(e), "available": True}

    async def get_me(self) -> Dict[str, Any]:
        """Get bot information."""
        if not self.enabled:
            return {
                "error": "Telegram bot not configured. TELEGRAM_BOT_TOKEN not set.",
                "available": False
            }
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/getMe"
                
                async with session.post(
                    url, 
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {"bot": data.get("result", {}), "success": True, "available": True}
                    else:
                        return {"error": f"HTTP {response.status}", "available": True}
        except Exception as e:
            logger.error(f"Telegram get_me error: {str(e)}")
            return {"error": str(e), "available": True}
