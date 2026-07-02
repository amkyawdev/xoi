"""Web content fetcher"""

import asyncio
from typing import Any

import httpx


class Fetcher:
    """Fetches web content"""
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            follow_redirects=True,
            headers={
                "User-Agent": "WebAgent/1.0 (Educational/Research)"
            }
        )
    
    async def fetch(self, url: str) -> dict[str, Any]:
        """Fetch content from URL"""
        for attempt in range(self.max_retries):
            try:
                response = await self.client.get(url)
                response.raise_for_status()
                return {
                    "url": str(response.url),
                    "status": response.status_code,
                    "headers": dict(response.headers),
                    "content": response.text,
                    "encoding": response.encoding
                }
            except httpx.HTTPError as e:
                if attempt == self.max_retries - 1:
                    return {"url": url, "error": str(e)}
                await asyncio.sleep(2 ** attempt)
        
        return {"url": url, "error": "Max retries exceeded"}
    
    async def fetch_multiple(self, urls: list[str]) -> list[dict[str, Any]]:
        """Fetch multiple URLs concurrently"""
        tasks = [self.fetch(url) for url in urls]
        return await asyncio.gather(*tasks)
    
    async def close(self) -> None:
        """Close the client"""
        await self.client.aclose()


async def fetch_url(url: str) -> dict[str, Any]:
    """Fetch a single URL"""
    fetcher = Fetcher()
    try:
        return await fetcher.fetch(url)
    finally:
        await fetcher.close()
