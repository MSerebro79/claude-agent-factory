# Battery Compatibility Agent

Агент находит список устройств и брендов, совместимых с заданным аккумулятором.

## Быстрый старт (5 минут)

### 1. Установи зависимости

```bash
pip install anthropic exa-py python-dotenv pydantic
```

### 2. Создай `.env`

```
ANTHROPIC_API_KEY=sk-ant-...
EXA_API_KEY=...
```

### 3. Запусти

```bash
python3 src/main.py "BL1850B"
python3 src/main.py "iPhone 14 battery"
python3 src/main.py "LP803048"
```

## Структура

```
battery-compatibility-agent/
  src/
    main.py        ← точка входа, CLI
    config.py      ← ключи и константы
  prompts/
    search_query_prompt.md    ← генерирует поисковые запросы
    extraction_prompt.md      ← извлекает устройства из текста
    synthesis_prompt.md       ← финальная сборка списка
  data/
    sample_input.json
    sample_output.json
  tests/
    test_scenario.md
  docs/
    acceptance_criteria.md
```

## Как работает

1. Принимает название батареи из CLI
2. LLM формирует 2–3 поисковых запроса
3. Exa ищет по вебу
4. LLM извлекает устройства из каждого результата
5. LLM синтезирует финальный список с дедупликацией
6. Выводит структурированный результат + уровень уверенности

## Ключевые ограничения

- Только поиск совместимости, не физические параметры
- Stateless — результаты не сохраняются
- Уровень уверенности Low означает: проверь вручную
