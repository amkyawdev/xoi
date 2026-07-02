"""ChromaDB wrapper"""

from typing import Any

import chromadb


class ChromaDB:
    """ChromaDB vector database"""
    
    def __init__(self, persist_directory: str = "./storage/vectors"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collections: dict[str, Any] = {}
    
    def get_or_create(self, name: str) -> Any:
        """Get or create collection"""
        if name not in self.collections:
            self.collections[name] = self.client.get_or_create_collection(name)
        return self.collections[name]
    
    def add(self, collection_name: str, documents: list[str], embeddings: list[list[float]], metadata: list[dict] | None = None) -> None:
        """Add documents"""
        collection = self.get_or_create(collection_name)
        ids = [f"doc_{i}" for i in range(len(documents))]
        metadata = metadata or [{}] * len(documents)
        
        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadata
        )
    
    def query(self, collection_name: str, query_embedding: list[float], n_results: int = 5) -> dict:
        """Query collection"""
        collection = self.get_or_create(collection_name)
        return collection.query(query_embeddings=[query_embedding], n_results=n_results)
    
    def delete_collection(self, name: str) -> None:
        """Delete collection"""
        self.client.delete_collection(name)
        if name in self.collections:
            del self.collections[name]
