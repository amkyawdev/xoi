"""API dependencies"""

from typing import Annotated

from fastapi import Depends

from llm.client import LLMClient, get_client
from crawler.fetcher import Fetcher
from rag.vector_store import VectorStore
from rag.embedding import EmbeddingGenerator


def get_llm_client() -> LLMClient:
    """Get LLM client dependency"""
    return get_client()


def get_fetcher() -> Fetcher:
    """Get fetcher dependency"""
    return Fetcher()


def get_vector_store() -> VectorStore:
    """Get vector store dependency"""
    return VectorStore()


def get_embedding_generator() -> EmbeddingGenerator:
    """Get embedding generator dependency"""
    return EmbeddingGenerator()


# Type aliases for dependency injection
LLMDep = Annotated[LLMClient, Depends(get_llm_client)]
FetcherDep = Annotated[Fetcher, Depends(get_fetcher)]
VectorStoreDep = Annotated[VectorStore, Depends(get_vector_store)]
EmbeddingDep = Annotated[EmbeddingGenerator, Depends(get_embedding_generator)]
