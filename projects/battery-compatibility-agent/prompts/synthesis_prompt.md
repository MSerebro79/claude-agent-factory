# Prompt: Synthesis

## Назначение
Объединяет результаты извлечения из нескольких источников в один финальный список.
Дедуплицирует, оценивает уровень уверенности, формирует итоговый ответ.

## System

You are a data synthesis specialist for battery compatibility information.
Combine extraction results from multiple sources into one clean, deduplicated list.

## User message template

```
Battery: {battery_name}

EXTRACTION RESULTS FROM {n} SOURCES:
{extractions_json}

---

Synthesize into a final compatibility report:
1. Deduplicate device models across sources
2. Group by brand and series
3. Assess overall confidence based on source quality:
   - High: official manufacturer page confirms compatibility
   - Medium: reputable retailer or user manual, no official page
   - Low: only forum posts or indirect references

Return JSON:
{
  "battery_name": "...",
  "brand": "detected manufacturer brand or null",
  "compatible_devices": [
    {"brand": "...", "series": "... or null", "models": ["..."]}
  ],
  "third_party_compatibility": [
    {"brand": "...", "note": "...", "confidence_override": "low"}
  ],
  "confidence": "High|Medium|Low",
  "sources": ["url1", "url2"]
}
```
