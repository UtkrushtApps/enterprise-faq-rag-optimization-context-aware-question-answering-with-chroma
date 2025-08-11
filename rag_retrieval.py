from typing import List, Dict, Any
import numpy as np

class EnterpriseFAQRAG:
    def __init__(self):
        pass
    def encode_query(self, query: str) -> np.ndarray:
        """Converts a user query into a semantic embedding vector."""
        raise NotImplementedError
    def retrieve_chunks(self, query_vec: np.ndarray, top_k: int = 6, category_filter: str = None) -> List[Dict[str, Any]]:
        """Retrieves top_k most relevant FAQ chunks for the query embedding, optionally filtered by category."""
        raise NotImplementedError
    def assemble_context(self, retrieved_chunks: List[Dict[str, Any]], max_context_tokens: int = 1200) -> str:
        """Combines retrieved chunks into a context passage with citation markers, respecting max_context_tokens."""
        raise NotImplementedError
    def build_prompt(self, query: str, context: str) -> str:
        """Formats the prompt for the LLM including the assembled context and user/system directives."""
        raise NotImplementedError
    def query_llm(self, prompt: str) -> str:
        """Passes the prompt to the LLM and returns the raw answer."""
        raise NotImplementedError
    def log_metrics(self, retrieval_latency_ms: float, tokens_used: int, hit_rate: float):
        """Tracks retrieval latency, token usage, and hit rate per query."""
        raise NotImplementedError
    def answer(self, query: str, top_k: int = 6, max_context_tokens: int = 1200, category_filter: str = None) -> str:
        """Orchestrates the end-to-end RAG QA pipeline."""
        raise NotImplementedError
