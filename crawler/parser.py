"""HTML parser"""

from typing import Any

from bs4 import BeautifulSoup


class HTMLParser:
    """Parses HTML content"""
    
    def __init__(self):
        self.parser = "lxml"
    
    def parse(self, html: str) -> BeautifulSoup:
        """Parse HTML string"""
        return BeautifulSoup(html, self.parser)
    
    def extract_links(self, html: str, base_url: str = "") -> list[str]:
        """Extract all links from HTML"""
        soup = self.parse(html)
        links = []
        
        for a in soup.find_all("a", href=True):
            href = a["href"]
            # Handle relative URLs
            if href.startswith("/"):
                from urllib.parse import urljoin
                href = urljoin(base_url, href)
            links.append(href)
        
        return links
    
    def extract_images(self, html: str) -> list[str]:
        """Extract all image URLs"""
        soup = self.parse(html)
        images = []
        
        for img in soup.find_all("img", src=True):
            images.append(img["src"])
        
        return images
    
    def extract_metadata(self, html: str) -> dict[str, Any]:
        """Extract metadata from HTML"""
        soup = self.parse(html)
        
        metadata = {
            "title": None,
            "description": None,
            "keywords": None,
            "author": None
        }
        
        # Title
        if title := soup.find("title"):
            metadata["title"] = title.get_text().strip()
        
        # Meta tags
        for meta in soup.find_all("meta"):
            name = meta.get("name", meta.get("property", ""))
            content = meta.get("content", "")
            
            if name in ["description", "keywords", "author"]:
                metadata[name] = content
            elif name == "og:title":
                metadata["title"] = content
        
        return metadata
    
    def find_by_selector(self, html: str, selector: str) -> list[str]:
        """Find elements by CSS selector"""
        soup = self.parse(html)
        elements = soup.select(selector)
        return [el.get_text(strip=True) for el in elements]
