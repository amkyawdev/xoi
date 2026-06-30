import aiohttp
from typing import Dict, Any
from app.config import settings

class TelegramClient:
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    async def send_message(self, chat_id: str, text: str) -> Dict[str, Any]:
        """Send a message to a Telegram chat."""
        if not self.bot_token:
            return {"error": "Telegram bot token not configured"}
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/sendMessage"
                payload = {
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": "HTML"
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
                            "success": True
                        }
                    else:
                        error = await response.json()
                        return {"error": error.get("description", "Unknown error")}
        except Exception as e:
            return {"error": str(e)}

    async def get_updates(self, offset: int = 0, limit: int = 100) -> Dict[str, Any]:
        """Get updates from Telegram."""
        if not self.bot_token:
            return {"error": "Telegram bot token not configured"}
        
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
                        return {"updates": data.get("result", []), "success": True}
                    else:
                        return {"error": f"HTTP {response.status}"}
        except Exception as e:
            return {"error": str(e)}

    async def set_webhook(self, webhook_url: str) -> Dict[str, Any]:
        """Set a webhook for the bot."""
        if not self.bot_token:
            return {"error": "Telegram bot token not configured"}
        
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
                        return {"success": True}
                    else:
                        return {"error": f"HTTP {response.status}"}
        except Exception as e:
            return {"error": str(e)}
