"""RAG retriever"""

from typing import Any

from rag.embedding import EmbeddingGenerator
from rag.vector_store import VectorStore


class Retriever:
    """Retrieves relevant documents for RAG"""
    
    def __init__(self, vector_store: VectorStore, embedding_generator: EmbeddingGenerator):
        self.vector_store = vector_store
        self.embeddings = embedding_generator
    
    async def retrieve(
        self,
        query: str,
        collection: str,
        top_k: int = 5,
        threshold: float = 0.7
    ) -> list[dict[str, Any]]:
        """Retrieve relevant documents"""
        # Generate query embedding
        query_embedding = await self.embeddings.generate(query)
        
        # Query vector store
        results = await self.vector_store.query(
            collection_name=collection,
            query_embedding=query_embedding,
            n_results=top_k
        )
        
        # Filter by threshold and format
        documents = []
        for i, doc in enumerate(results["documents"]):
            distance = results["distances"][i]
            similarity = 1 - distance  # Convert distance to similarity
            
            if similarity >= threshold:
                documents.append({
                    "content": doc,
                    "metadata": results["metadatas"][i],
                    "similarity": similarity
                })
        
        return documents
    
    async def retrieve_with_context(self, query: str, collection: str, max_context_length: int = 4000) -> str:
        """Retrieve documents and format as context"""
        docs = await self.retrieve(query, collection)
        
        context_parts = []
        total_length = 0
        
        for doc in docs:
            part = f"\n---\n{doc['content']}\n---"
            if total_length + len(part) > max_context_length:
                break
            context_parts.append(part)
            total_length += len(part)
        
        return "\n".join(context_parts) if context_parts else ""
