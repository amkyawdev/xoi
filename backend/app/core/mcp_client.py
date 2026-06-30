import aiohttp
from typing import Dict, Any, Optional
from app.config import settings

class MCPClient:
    def __init__(self):
        self.api_key = settings.BROWSERLESS_API_KEY
        self.base_url = "https://chrome.browserless.io"

    async def navigate(self, url: str) -> Dict[str, Any]:
        """Navigate to a URL and return the page content."""
        if not self.api_key:
            return {"error": "Browserless API key not configured"}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/content",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "url": url,
                        "waitForSelector": "body"
                    },
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        content = await response.json()
                        return {
                            "url": url,
                            "title": content.get("title", ""),
                            "text": content.get("text", ""),
                            "success": True
                        }
                    else:
                        return {"error": f"HTTP {response.status}"}
        except Exception as e:
            return {"error": str(e)}

    async def screenshot(self, url: Optional[str] = None) -> Dict[str, Any]:
        """Take a screenshot of a webpage."""
        if not self.api_key:
            return {"error": "Browserless API key not configured"}
        
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
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        content = await response.read()
                        import base64
                        return {
                            "screenshot": base64.b64encode(content).decode(),
                            "success": True
                        }
                    else:
                        return {"error": f"HTTP {response.status}"}
        except Exception as e:
            return {"error": str(e)}

    async def evaluate(self, script: str) -> Dict[str, Any]:
        """Execute JavaScript in the browser context."""
        if not self.api_key:
            return {"error": "Browserless API key not configured"}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/function",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={"code": script},
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {"result": result, "success": True}
                    else:
                        return {"error": f"HTTP {response.status}"}
        except Exception as e:
            return {"error": str(e)}
