# Startup Radar AI

Находит AI-стартапы в нише аналитики стартапов и готовит данные для сравнительной таблицы.

## Запуск за 5 минут

```bash
cd projects/startup-radar-ai

# 1. Установить зависимости (только Exa — Claude API не нужен)
pip install exa-py python-dotenv

# 2. Создать .env
cp .env.example .env
# Вставить EXA_API_KEY (получить на exa.ai, free tier)

# 3. Запустить
python src/main.py
```

## После запуска

```
output/candidates_YYYY-MM-DD.json  — собранные данные
output/prompt_YYYY-MM-DD.txt       — готовый промпт
```

Открыть `output/prompt_YYYY-MM-DD.txt`, скопировать всё содержимое,
вставить в claude.ai → получить сравнительную таблицу.

## Параметры

Редактировать `src/config.py`:
- `DAYS_BACK` — период поиска (по умолчанию 60 дней)
- `TARGET_COUNT` — желаемое количество стартапов
- `SEARCH_QUERIES` — поисковые запросы (можно добавить свои)

## Стоимость

~$0.00 (Exa free tier, Claude через подписку)
