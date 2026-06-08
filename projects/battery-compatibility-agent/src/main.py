"""
Battery Compatibility Agent
Usage: python3 src/main.py "<battery name>"
"""

import sys
import json
import textwrap
from typing import Any

import anthropic
from exa_py import Exa

from config import ANTHROPIC_API_KEY, EXA_API_KEY, MODEL, MAX_SEARCH_RESULTS, MAX_TEXT_CHARS, validate_env


def generate_search_queries(client: anthropic.Anthropic, battery_name: str) -> list[str]:
    message = client.messages.create(
        model=MODEL,
        max_tokens=256,
        system=(
            "You are a search query specialist for battery compatibility research. "
            "Given a battery name or model number, generate 2-3 focused search queries "
            "that will find authoritative compatibility information. "
            "Prefer queries targeting manufacturer pages, product manuals, reputable retailers. "
            "Include the exact model number in at least one query. "
            "Return a JSON array of strings only, no explanation."
        ),
        messages=[
            {
                "role": "user",
                "content": (
                    f'Battery: {battery_name}\n\n'
                    'Generate 2-3 search queries to find compatible devices. '
                    'Return JSON array only, example: ["query1", "query2"]'
                ),
            }
        ],
    )
    return json.loads(message.content[0].text)


def search_web(exa: Exa, queries: list[str]) -> list[dict[str, Any]]:
    results = []
    for query in queries:
        try:
            response = exa.search_and_contents(
                query,
                num_results=MAX_SEARCH_RESULTS,
                text={"max_characters": MAX_TEXT_CHARS},
            )
            for r in response.results:
                results.append({"url": r.url, "title": r.title or "", "text": r.text or ""})
        except Exception as e:
            print(f"  [search warning] query failed: {e}", file=sys.stderr)
    return results


def extract_from_source(
    client: anthropic.Anthropic, battery_name: str, source: dict[str, Any]
) -> dict[str, Any]:
    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=(
            "You are a precise data extraction specialist. "
            "Extract device compatibility information from web page text. "
            "CRITICAL: Only extract devices EXPLICITLY mentioned in the provided text. "
            "Do NOT add devices from your training knowledge. "
            "Return valid JSON only."
        ),
        messages=[
            {
                "role": "user",
                "content": (
                    f"Battery model: {battery_name}\n"
                    f"Source URL: {source['url']}\n\n"
                    f"TEXT FROM SOURCE:\n{source['text']}\n\n"
                    "---\n"
                    f"Extract all devices explicitly mentioned as compatible with \"{battery_name}\".\n\n"
                    "Return JSON:\n"
                    '{"brand": "detected brand or null", '
                    '"compatible_devices": [{"brand": "...", "series": "...", "models": ["..."]}], '
                    '"extraction_confidence": "high|medium|low", '
                    '"note": "any caveat"}'
                ),
            }
        ],
    )
    try:
        return json.loads(message.content[0].text)
    except json.JSONDecodeError:
        return {"brand": None, "compatible_devices": [], "extraction_confidence": "low", "note": "parse error"}


def synthesize(
    client: anthropic.Anthropic, battery_name: str, extractions: list[dict], sources: list[str]
) -> dict[str, Any]:
    message = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=(
            "You are a data synthesis specialist for battery compatibility. "
            "Combine extraction results from multiple sources into one clean deduplicated list. "
            "Confidence: High=official manufacturer page, Medium=reputable retailer/manual, Low=forums only. "
            "Return valid JSON only."
        ),
        messages=[
            {
                "role": "user",
                "content": (
                    f"Battery: {battery_name}\n\n"
                    f"EXTRACTION RESULTS FROM {len(extractions)} SOURCES:\n"
                    f"{json.dumps(extractions, ensure_ascii=False, indent=2)}\n\n"
                    "---\n"
                    "Synthesize into final compatibility report. Deduplicate, group by brand/series.\n\n"
                    "Return JSON:\n"
                    '{"battery_name": "...", "brand": "...", '
                    '"compatible_devices": [{"brand": "...", "series": "...", "models": ["..."]}], '
                    '"third_party_compatibility": [], '
                    f'"confidence": "High|Medium|Low", "sources": {json.dumps(sources)}}}'
                ),
            }
        ],
    )
    try:
        return json.loads(message.content[0].text)
    except json.JSONDecodeError:
        return {
            "battery_name": battery_name,
            "brand": None,
            "compatible_devices": [],
            "confidence": "Low",
            "sources": sources,
        }


def format_output(result: dict[str, Any]) -> str:
    lines = [f"\nBattery: {result.get('battery_name', 'unknown')}"]
    if result.get("brand"):
        lines[0] += f" ({result['brand']})"

    devices = result.get("compatible_devices", [])
    if devices:
        lines.append("\nCompatible devices:")
        for group in devices:
            brand = group.get("brand", "")
            series = group.get("series", "")
            models = group.get("models", [])
            header = f"  Brand: {brand}"
            if series:
                header += f" | Series: {series}"
            lines.append(header)
            if models:
                model_str = ", ".join(models[:10])
                if len(models) > 10:
                    model_str += f" (+{len(models) - 10} more)"
                lines.append(f"  Models: {model_str}")
    else:
        lines.append("\nNo compatible devices found.")

    third = result.get("third_party_compatibility", [])
    if third:
        lines.append("\nAdditional compatibility (3rd party):")
        for item in third:
            lines.append(f"  - {item.get('brand', '')}: {item.get('note', '')}")

    lines.append(f"\nConfidence: {result.get('confidence', 'Low')}")

    sources = result.get("sources", [])
    if sources:
        lines.append("Sources:")
        for s in sources[:3]:
            lines.append(f"  - {s}")

    return "\n".join(lines)


def run(battery_name: str) -> None:
    validate_env()
    claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    exa = Exa(api_key=EXA_API_KEY)

    print(f"Searching compatibility for: {battery_name}...")

    queries = generate_search_queries(claude, battery_name)
    print(f"Queries: {queries}")

    sources = search_web(exa, queries)
    if not sources:
        print("\nNo search results found. Try a different battery name or check your EXA_API_KEY.")
        sys.exit(1)

    print(f"Found {len(sources)} source(s). Extracting compatibility data...")
    extractions = [extract_from_source(claude, battery_name, s) for s in sources]

    source_urls = [s["url"] for s in sources]
    result = synthesize(claude, battery_name, extractions, source_urls)

    print(format_output(result))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 src/main.py \"<battery name>\"")
        sys.exit(1)
    run(sys.argv[1])
