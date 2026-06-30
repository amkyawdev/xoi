import aiohttp
from typing import Dict, Any
from app.config import settings

class RapidAPIClient:
    def __init__(self):
        self.api_key = settings.RAPIDAPI_KEY
        self.base_url = "https://rapidapi.com"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "generic-api-workspace"
        } if self.api_key else {}

    async def search_web(self, query: str) -> Dict[str, Any]:
        """Search the web using RapidAPI web search."""
        if not self.api_key:
            return {
                "query": query,
                "results": [],
                "message": "RapidAPI key not configured"
            }
        
        try:
            # This is a placeholder - actual implementation would use a specific RapidAPI service
            async with aiohttp.ClientSession() as session:
                # Example: Google Search API via RapidAPI
                url = "https://google-search72.p.rapidapi.com/search"
                
                async with session.get(
                    url,
                    headers=self.headers,
                    params={"q": query, "num": 10},
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "query": query,
                            "results": data.get("results", []),
                            "success": True
                        }
                    else:
                        return {"error": f"HTTP {response.status}"}
        except Exception as e:
            return {"error": str(e)}

    async def call_endpoint(
        self, 
        endpoint: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Call a RapidAPI endpoint."""
        if not self.api_key:
            return {"error": "RapidAPI key not configured"}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    endpoint,
                    headers=self.headers,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {"data": data, "success": True}
                    else:
                        return {"error": f"HTTP {response.status}"}
        except Exception as e:
            return {"error": str(e)}
