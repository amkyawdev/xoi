"""Text chunking for RAG"""

from typing import Any


class TextChunker:
    """Splits text into chunks for embedding"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str) -> list[dict[str, Any]]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            
            chunks.append({
                "text": chunk,
                "start": start,
                "end": end,
                "index": len(chunks)
            })
            
            start = end - self.chunk_overlap
        
        return chunks
    
    def chunk_by_sentences(self, text: str) -> list[dict[str, Any]]:
        """Split text by sentences"""
        import re
        sentences = re.split(r"[.!?]+\s+", text)
        
        chunks = []
        current_chunk = ""
        current_size = 0
        
        for sentence in sentences:
            sentence_size = len(sentence)
            
            if current_size + sentence_size > self.chunk_size:
                if current_chunk:
                    chunks.append({
                        "text": current_chunk.strip(),
                        "index": len(chunks)
                    })
                current_chunk = sentence
                current_size = sentence_size
            else:
                current_chunk += " " + sentence
                current_size += sentence_size
        
        if current_chunk:
            chunks.append({
                "text": current_chunk.strip(),
                "index": len(chunks)
            })
        
        return chunks
    
    def chunk_by_paragraphs(self, text: str) -> list[dict[str, Any]]:
        """Split text by paragraphs"""
        paragraphs = text.split("\n\n")
        
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk) + len(para) > self.chunk_size:
                if current_chunk:
                    chunks.append({
                        "text": current_chunk.strip(),
                        "index": len(chunks)
                    })
                current_chunk = para
            else:
                current_chunk += "\n\n" + para
        
        if current_chunk:
            chunks.append({
                "text": current_chunk.strip(),
                "index": len(chunks)
            })
        
        return chunks
