"""Vector store for RAG"""

import os
from typing import Any

import chromadb


class VectorStore:
    """Vector store using ChromaDB"""
    
    def __init__(self, persist_directory: str = "./storage/vectors"):
        os.makedirs(persist_directory, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collections: dict[str, Any] = {}
    
    def get_collection(self, name: str) -> Any:
        """Get or create collection"""
        if name not in self.collections:
            self.collections[name] = self.client.get_or_create_collection(name)
        return self.collections[name]
    
    async def add(self, collection_name: str, texts: list[str], embeddings: list[list[float]], metadata: list[dict] | None = None) -> None:
        """Add documents to collection"""
        collection = self.get_collection(collection_name)
        ids = [f"doc_{i}" for i in range(len(texts))]
        metadata = metadata or [{}] * len(texts)
        
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadata
        )
    
    async def query(self, collection_name: str, query_embedding: list[float], n_results: int = 5) -> dict[str, Any]:
        """Query collection"""
        collection = self.get_collection(collection_name)
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return {
            "documents": results.get("documents", [[]])[0],
            "metadatas": results.get("metadatas", [[]])[0],
            "distances": results.get("distances", [[]])[0]
        }
    
    async def delete_collection(self, name: str) -> None:
        """Delete collection"""
        self.client.delete_collection(name)
        if name in self.collections:
            del self.collections[name]
