"""Sitemap parser"""

from typing import Any

import httpx
from bs4 import BeautifulSoup


class SitemapParser:
    """Parses XML sitemaps"""
    
    async def fetch(self, url: str) -> list[str]:
        """Fetch and parse sitemap"""
        # Try common sitemap locations
        locations = [
            url.rstrip("/") + "/sitemap.xml",
            url.rstrip("/") + "/sitemap-index.xml",
            url.rstrip("/") + "/sitemap.xml.gz"
        ]
        
        for location in locations:
            try:
                urls = await self._fetch_sitemap(location)
                if urls:
                    return urls
            except httpx.HTTPError:
                continue
        
        return []
    
    async def _fetch_sitemap(self, url: str) -> list[str]:
        """Fetch sitemap from URL"""
        client = httpx.AsyncClient()
        response = await client.get(url)
        await client.aclose()
        response.raise_for_status()
        
        return self._parse_sitemap(response.text)
    
    def _parse_sitemap(self, content: str) -> list[str]:
        """Parse sitemap XML content"""
        soup = BeautifulSoup(content, "lxml")
        urls = []
        
        # Handle XML namespace
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        
        for loc in soup.find_all("loc"):
            if text := loc.get_text(strip=True):
                urls.append(text)
        
        return urls
    
    async def discover_sitemaps(self, url: str) -> list[str]:
        """Discover all sitemaps for a site"""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        
        # Common sitemap locations
        locations = [
            f"{base}/sitemap.xml",
            f"{base}/sitemap-index.xml",
            f"{base}/wp-sitemap.xml",
            f"{base}/sitemap_index.xml"
        ]
        
        found = []
        client = httpx.AsyncClient()
        
        for location in locations:
            try:
                response = await client.head(location)
                if response.status_code == 200:
                    found.append(location)
            except httpx.HTTPError:
                continue
        
        await client.aclose()
        return found
