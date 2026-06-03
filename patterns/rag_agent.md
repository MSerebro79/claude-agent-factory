# Pattern: RAG Agent

## Description

Retrieval-Augmented Generation agent that answers questions grounded in a private document corpus. Suitable for internal knowledge bases, deal memos, and research archives.

## Core Loop

1. Receive a user question.
2. Embed the question and retrieve top-k chunks from the vector store.
3. Inject retrieved chunks into the context window.
4. Generate a grounded answer with inline citations.
5. Return answer and source references.

## Recommended Tools

- Embedding model: `text-embedding-3-small` (OpenAI) or `voyage-3-lite` (Voyage AI)
- Vector store: Pinecone, Supabase pgvector, or Chroma (local)
- Reranker (optional): Cohere Rerank for precision boost

## Typical Cost

~2 000–8 000 tokens per query (retrieval + generation). Embedding is cheap; generation dominates.

## Known Risks

- Retrieval misses — tune chunk size and overlap; test with diverse queries.
- Out-of-date corpus — schedule re-indexing when source documents change.
- Answer not grounded — enforce citation requirement in system prompt; validate programmatically.
