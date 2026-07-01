import aiohttp
import logging
from typing import Dict, Any, Optional
from app.config import settings

logger = logging.getLogger(__name__)

class MCPClient:
    def __init__(self):
        self.api_key = settings.BROWSERLESS_API_KEY
        self.base_url = "https://chrome.browserless.io"
        self.enabled = bool(self.api_key)
        logger.info(f"MCP Client initialized: enabled={self.enabled}")

    async def navigate(self, url: str) -> Dict[str, Any]:
        """Navigate to a URL and return the page content."""
        if not self.enabled:
            return {
                "error": "Browser automation not available. BROWSERLESS_API_KEY not configured.",
                "available": False
            }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/content",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "url": url,
                        "waitForSelector": "body",
                        "gotoOptions": {"waitUntil": "networkidle2"}
                    },
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        content = await response.json()
                        return {
                            "url": url,
                            "title": content.get("title", ""),
                            "text": content.get("text", ""),
                            "links": content.get("links", []),
                            "images": content.get("images", [])[:10],  # Limit images
                            "success": True,
                            "available": True
                        }
                    elif response.status == 401:
                        return {"error": "Invalid Browserless API key", "available": False}
                    else:
                        return {"error": f"HTTP {response.status}", "available": True}
        except Exception as e:
            logger.error(f"Browserless navigate error: {str(e)}")
            return {"error": str(e), "available": True}

    async def screenshot(self, url: Optional[str] = None) -> Dict[str, Any]:
        """Take a screenshot of a webpage."""
        if not self.enabled:
            return {
                "error": "Browser automation not available. BROWSERLESS_API_KEY not configured.",
                "available": False
            }
        
        try:
            payload = {}
            if url:
                payload["url"] = url
            else:
                return {"error": "URL required for screenshot"}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/screenshot",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        content = await response.read()
                        import base64
                        return {
                            "screenshot": base64.b64encode(content).decode(),
                            "success": True,
                            "available": True
                        }
                    else:
                        return {"error": f"HTTP {response.status}", "available": True}
        except Exception as e:
            logger.error(f"Browserless screenshot error: {str(e)}")
            return {"error": str(e), "available": True}

    async def evaluate(self, script: str) -> Dict[str, Any]:
        """Execute JavaScript in the browser context."""
        if not self.enabled:
            return {
                "error": "Browser automation not available. BROWSERLESS_API_KEY not configured.",
                "available": False
            }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/function",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={"code": script},
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {"result": result, "success": True, "available": True}
                    else:
                        return {"error": f"HTTP {response.status}", "available": True}
        except Exception as e:
            logger.error(f"Browserless evaluate error: {str(e)}")
            return {"error": str(e), "available": True}

    async def scrape_text(self, url: str) -> Dict[str, Any]:
        """Scrape text content from a webpage."""
        if not self.enabled:
            return {
                "error": "Browser automation not available. BROWSERLESS_API_KEY not configured.",
                "available": False
            }
        
        return await self.navigate(url)
