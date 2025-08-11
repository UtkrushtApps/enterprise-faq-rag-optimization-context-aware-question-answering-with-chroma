# Task Overview

You will implement the core Retrieval-Augmented Generation (RAG) logic for an enterprise FAQ chatbot. The vector database (Chroma) is pre-populated with embedded FAQ documents; your focus is on completing the retrieval, context preparation, and LLM interaction pipeline so users get accurate, cited answers to their questions.

## Guidance

- Your RAG system should convert user queries into vector embeddings, retrieve the most relevant FAQ chunks, assemble a context respecting LLM token limitations, add citation markers, and forward this prompt to a (mocked or real) LLM generator.
- Use LangChain to manage the pipeline flow and tiktoken for token budgeting. Carefully track how retrieval quality and prompt formatting impact answer accuracy and user experience.
- Be sure your code cleanly separates database operations, retrieval logic, context management, and logging. Your implementation should help reduce hallucination and context dilution by precise chunk selection with citations.

## Database Access Information

- Chroma DB is available at `localhost:8000` (collection: `enterprise_faq`).
- All vector embeddings are 1536-dimensional (OpenAI model spec).
- Chunk metadata: `chunk_id`, `faq_id`, `chunk_index`, `category`, `content`, `embedding`, `token_count`, `title`.
- Use the provided `database_client.py` utility to query/retrieve from Chroma.

## Objectives
- Complete the RAG pipeline (`rag_retrieval.py`):
  - Implement query encoding using OpenAI or sentence-transformers (per config).
  - Retrieve top-k FAQ chunks using cosine/dot-product search.
  - Assemble context up to a maximum LLM token limit (default 1200 from context, 800 left for answer).
  - Add citation markers to context and prompts.
  - Track and log retrieval latency, token usage, and retrieval hit rate.
- Respect the context window of the downstream LLM.

## How To Verify

- Issue queries from `sample_queries.txt` using your CLI/REST wrapper; validate answers reference the correct FAQ category and include citations.
- Check retrieval logs for latency and token statistics.
- Confirm the number of FAQ chunks in the prompt never exceeds the LLM context window.
- Conduct spot checks for context dilution or missed answers using provided FAQ dataset.