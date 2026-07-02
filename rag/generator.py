"""RAG generator"""

from typing import Any

from llm.client import LLMClient
from llm.models import Message


class RAGGenerator:
    """Generates responses using RAG"""
    
    def __init__(self, llm_client: LLMClient, retriever: Any):
        self.llm = llm_client
        self.retriever = retriever
    
    async def generate(
        self,
        query: str,
        collection: str,
        system_prompt: str | None = None
    ) -> dict[str, Any]:
        """Generate response with RAG"""
        # Retrieve relevant documents
        context = await self.retriever.retrieve_with_context(query, collection)
        
        # Build prompt
        system = system_prompt or """You are a helpful assistant. Use the provided context to answer questions accurately. If the context doesn't contain relevant information, say so."""
        
        messages = [
            Message(role="system", content=system),
            Message(role="user", content=f"Context:\n{context}\n\nQuestion: {query}")
        ]
        
        # Generate response
        response = await self.llm.chat(messages)
        
        return {
            "answer": response["choices"][0]["message"]["content"],
            "sources": await self.retriever.retrieve(query, collection)
        }
    
    async def generate_stream(
        self,
        query: str,
        collection: str,
        system_prompt: str | None = None
    ):
        """Generate streaming response with RAG"""
        context = await self.retriever.retrieve_with_context(query, collection)
        
        system = system_prompt or "You are a helpful assistant."
        
        messages = [
            Message(role="system", content=system),
            Message(role="user", content=f"Context:\n{context}\n\nQuestion: {query}")
        ]
        
        async for chunk in self.llm.chat(messages, stream=True):
            yield chunk
