# Pattern: Research Agent

## Description

Searches the web or a document corpus, synthesises findings, and returns a structured report. Suitable for market research, due diligence, and competitive analysis.

## Core Loop

1. Receive a research brief (topic, scope, depth).
2. Generate a list of search queries.
3. Execute searches (Perplexity / Brave / internal corpus).
4. Deduplicate and rank results by relevance.
5. Synthesise into a structured markdown report.
6. Return report with sources cited inline.

## Recommended Tools

- Web search (Perplexity API or Brave Search API)
- Optional: vector store retrieval for internal documents
- Optional: scraper for full-page content

## Typical Cost

~4 000–12 000 tokens per run depending on depth.

## Known Risks

- Hallucinated citations — always verify source URLs.
- Stale data — set a recency filter on searches.
- Rate limiting on search APIs — implement exponential backoff.
