"""Robots.txt parser"""

from urllib.parse import urlparse

import httpx


class RobotsParser:
    """Parses robots.txt files"""
    
    def __init__(self):
        self.rules: dict[str, dict[str, list[str]]] = {}
    
    async def fetch(self, url: str) -> dict[str, Any]:
        """Fetch and parse robots.txt"""
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        try:
            client = httpx.AsyncClient()
            response = await client.get(robots_url)
            await client.aclose()
            
            if response.status_code == 200:
                self.rules[parsed.netloc] = self._parse_rules(response.text)
                return {"url": url, "allowed": True, "rules": self.rules[parsed.netloc]}
            
            return {"url": url, "allowed": True, "rules": {}}
        except httpx.HTTPError:
            return {"url": url, "allowed": True, "rules": {}}
    
    def _parse_rules(self, content: str) -> dict[str, list[str]]:
        """Parse robots.txt content"""
        rules = {"allow": [], "disallow": []}
        current_user_agent = None
        
        for line in content.split("\n"):
            line = line.strip()
            
            if not line or line.startswith("#"):
                continue
            
            if line.lower().startswith("user-agent:"):
                current_user_agent = line.split(":", 1)[1].strip().lower()
            elif line.lower().startswith("allow:"):
                if current_user_agent == "*":
                    rules["allow"].append(line.split(":", 1)[1].strip())
            elif line.lower().startswith("disallow:"):
                if current_user_agent == "*":
                    rules["disallow"].append(line.split(":", 1)[1].strip())
        
        return rules
    
    def can_fetch(self, netloc: str, path: str) -> bool:
        """Check if path can be fetched according to rules"""
        if netloc not in self.rules:
            return True
        
        rules = self.rules[netloc]
        
        for disallow in rules["disallow"]:
            if path.startswith(disallow):
                for allow in rules["allow"]:
                    if path.startswith(allow):
                        return True
                return False
        
        return True
