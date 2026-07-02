"""Content extractor"""

from typing import Any

from bs4 import BeautifulSoup


class ContentExtractor:
    """Extracts meaningful content from HTML"""
    
    def extract_main_content(self, html: str) -> str:
        """Extract main content, removing navigation, ads, etc."""
        soup = BeautifulSoup(html, "lxml")
        
        # Remove unwanted elements
        for tag in soup.find_all(["script", "style", "nav", "header", "footer", "aside"]):
            tag.decompose()
        
        # Try to find main content
        main = soup.find("main") or soup.find("article") or soup.find("div", class_="content")
        
        if main:
            return main.get_text(separator="\n", strip=True)
        
        return soup.get_text(separator="\n", strip=True)
    
    def extract_by_selector(self, html: str, selector: str) -> str:
        """Extract content matching selector"""
        soup = BeautifulSoup(html, "lxml")
        elements = soup.select(selector)
        
        if elements:
            return "\n".join(el.get_text(separator="\n", strip=True) for el in elements)
        
        return ""
    
    def extract_article(self, html: str) -> dict[str, Any]:
        """Extract structured article content"""
        soup = BeautifulSoup(html, "lxml")
        
        title = ""
        if title_tag := soup.find("h1"):
            title = title_tag.get_text(strip=True)
        elif title := soup.find("meta", property="og:title"):
            title = title.get("content", "")
        
        content = self.extract_main_content(html)
        
        author = ""
        if author_tag := soup.find("meta", attrs={"name": "author"}):
            author = author_tag.get("content", "")
        
        published_time = ""
        if time_tag := soup.find("meta", property="article:published_time"):
            published_time = time_tag.get("content", "")
        
        return {
            "title": title,
            "content": content,
            "author": author,
            "published_time": published_time
        }
