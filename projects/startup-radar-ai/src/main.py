import os
import json
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse

from exa_py import Exa
from dotenv import load_dotenv

from config import (
    DAYS_BACK, TARGET_COUNT, EXA_NUM_RESULTS, MAX_CANDIDATES,
    SEARCH_QUERIES, INCLUDE_KEYWORDS, AI_KEYWORDS, EXCLUDE_KEYWORDS,
)
from prompts import ANALYSIS_PROMPT_TEMPLATE

load_dotenv()

EXA_API_KEY = os.getenv("EXA_API_KEY")
if not EXA_API_KEY:
    raise SystemExit("ERROR: EXA_API_KEY not set. Check your .env file. Get key: https://exa.ai/")

TODAY = datetime.now().strftime("%Y-%m-%d")

Path("logs").mkdir(exist_ok=True)
Path("output").mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"logs/run_{TODAY}.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

exa = Exa(api_key=EXA_API_KEY)


def search_exa(query: str, start_date: str) -> list[dict]:
    for attempt in range(3):
        try:
            results = exa.search_and_contents(
                query,
                num_results=EXA_NUM_RESULTS,
                start_published_date=start_date,
                text={"max_characters": 600},
            )
            return [
                {
                    "url": r.url,
                    "title": r.title or "",
                    "snippet": r.text or "",
                }
                for r in results.results
            ]
        except Exception as e:
            wait = 2 ** (attempt + 1)
            log.warning(f"Exa error (attempt {attempt+1}/3): {e} — retry in {wait}s")
            time.sleep(wait)
    log.error(f"Exa failed: {query[:60]}")
    return []


def get_domain(url: str) -> str:
    try:
        return urlparse(url).netloc.replace("www.", "")
    except Exception:
        return url


def is_relevant(title: str, snippet: str) -> bool:
    text = (title + " " + snippet).lower()

    if any(kw in text for kw in EXCLUDE_KEYWORDS):
        return False

    has_ai = any(kw in text for kw in AI_KEYWORDS)
    has_startup = any(kw in text for kw in INCLUDE_KEYWORDS)

    return has_ai and has_startup


def collect_candidates(start_date: str) -> list[dict]:
    log.info("Searching Exa...")
    domain_hits: dict[str, list] = defaultdict(list)

    for q in SEARCH_QUERIES:
        results = search_exa(q, start_date)
        log.info(f"  '{q[:55]}' → {len(results)} results")
        for r in results:
            domain = get_domain(r["url"])
            domain_hits[domain].append(r)

    candidates = []
    for domain, hits in domain_hits.items():
        best = max(hits, key=lambda x: len(x["snippet"]))
        if not is_relevant(best["title"], best["snippet"]):
            continue
        candidates.append(
            {
                "domain": domain,
                "url": best["url"],
                "title": best["title"],
                "snippet": best["snippet"],
                "mention_count": len(hits),
                "sources": list({h["url"] for h in hits}),
            }
        )

    candidates.sort(key=lambda x: x["mention_count"], reverse=True)
    log.info(f"Relevant candidates after filtering: {len(candidates)}")
    return candidates[:MAX_CANDIDATES]


def format_candidates_for_prompt(candidates: list[dict]) -> str:
    lines = []
    for i, c in enumerate(candidates, 1):
        lines.append(f"### {i}. {c['title'] or c['domain']}")
        lines.append(f"- **URL:** {c['url']}")
        lines.append(f"- **Упоминаний:** {c['mention_count']}")
        lines.append(f"- **Описание:** {c['snippet'][:400]}")
        lines.append(f"- **Источники:** {', '.join(c['sources'][:3])}")
        lines.append("")
    return "\n".join(lines)


def main():
    log.info(f"=== Startup Radar AI | {TODAY} ===")
    log.info(f"Period: last {DAYS_BACK} days | Target: {TARGET_COUNT} startups")

    start_date = (datetime.now() - timedelta(days=DAYS_BACK)).strftime("%Y-%m-%dT00:00:00.000Z")

    candidates = collect_candidates(start_date)

    if len(candidates) < 5:
        raise SystemExit(
            f"ERROR: Only {len(candidates)} relevant candidates found. "
            f"Try increasing DAYS_BACK in config.py."
        )

    candidates_json_path = f"output/candidates_{TODAY}.json"
    with open(candidates_json_path, "w", encoding="utf-8") as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)
    log.info(f"Candidates saved: {candidates_json_path}")

    candidates_text = format_candidates_for_prompt(candidates)
    prompt = ANALYSIS_PROMPT_TEMPLATE.format(
        days_back=DAYS_BACK,
        date=TODAY,
        candidates_text=candidates_text,
    )

    prompt_path = f"output/prompt_{TODAY}.txt"
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(prompt)
    log.info(f"Prompt saved: {prompt_path}")

    print(f"""
✓ Done. Found {len(candidates)} candidates.

Next step:
  1. Open claude.ai (your subscription)
  2. Copy the full content of: {prompt_path}
  3. Paste into Claude → get your comparative table

Raw data: {candidates_json_path}
""")


if __name__ == "__main__":
    main()
