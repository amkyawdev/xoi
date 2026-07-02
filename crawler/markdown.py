"""Convert HTML to Markdown"""

from typing import Any

from bs4 import BeautifulSoup
import markdown


class HTMLToMarkdown:
    """Converts HTML to Markdown format"""
    
    def convert(self, html: str) -> str:
        """Convert HTML to Markdown"""
        # Use markdown library for basic conversion
        md = markdown.markdown(html, extensions=["tables", "fenced_code"])
        return md
    
    def convert_with_links(self, html: str) -> str:
        """Convert HTML preserving links"""
        soup = BeautifulSoup(html, "lxml")
        
        # Convert links
        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True)
            href = a["href"]
            a.replace_with(soup.new_string(f"[{text}]({href})"))
        
        # Convert images
        for img in soup.find_all("img", src=True):
            alt = img.get("alt", "")
            src = img["src"]
            img.replace_with(soup.new_string(f"![{alt}]({src})"))
        
        return markdown.markdown(str(soup))
    
    def convert_article(self, html: str, title: str | None = None) -> str:
        """Convert article HTML to Markdown"""
        md = self.convert_with_links(html)
        
        if title:
            md = f"# {title}\n\n{md}"
        
        return md
