# Pattern: Sourcing Agent

## Description

Proactively discovers and qualifies leads — companies, founders, investors, or candidates — from public sources. Suitable for VC deal sourcing, talent search, and partnership identification.

## Core Loop

1. Receive sourcing criteria (sector, stage, geography, keywords).
2. Query data sources (LinkedIn, Crunchbase, Product Hunt, news APIs, GitHub, etc.).
3. Score each result against criteria.
4. Deduplicate against existing pipeline (CRM lookup).
5. Return ranked shortlist with a one-line rationale per item.

## Recommended Tools

- Crunchbase API or Apollo.io for company/founder data
- LinkedIn search (via scraper or API — check ToS)
- Perplexity or Brave for supplementary web research
- Airtable or Notion API for CRM deduplication

## Typical Cost

~5 000–15 000 tokens per sourcing run. Scales with shortlist size.

## Known Risks

- ToS violations on scraped data — prefer official APIs.
- False positives — require human review before outreach.
- Stale data — always include a data freshness timestamp in output.
