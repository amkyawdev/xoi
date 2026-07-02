"""HTML content cleaner"""

import re
from typing import Any


class HTMLCleaner:
    """Cleans HTML content"""
    
    def clean(self, html: str) -> str:
        """Clean HTML content"""
        # Remove script tags
        html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove style tags
        html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove comments
        html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
        
        # Remove extra whitespace
        html = re.sub(r"\s+", " ", html)
        
        return html.strip()
    
    def remove_attributes(self, html: str, keep: list[str] | None = None) -> str:
        """Remove HTML attributes except specified ones"""
        keep = keep or ["href", "src"]
        
        def replace_tag(match: re.Match) -> str:
            tag = match.group(1)
            attrs = match.group(2)
            
            if not attrs:
                return tag
            
            # Keep only specified attributes
            kept_attrs = []
            for attr in re.findall(r'(\w+)=["\']([^"\']*)["\']', attrs):
                if attr[0] in keep:
                    kept_attrs.append(f'{attr[0]}="{attr[1]}"')
            
            if kept_attrs:
                return f"<{tag} {' '.join(kept_attrs)}>"
            return tag
        
        return re.sub(r"<(\w+)([^>]*)>", replace_tag, html)
    
    def remove_empty_tags(self, html: str) -> str:
        """Remove empty HTML tags"""
        return re.sub(r"<(\w+)[^>]*>\s*</\1>", "", html, flags=re.IGNORECASE)
