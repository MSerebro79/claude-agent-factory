# Agent Factory v0.6

Система из трёх агентов для проектирования, проверки и сборки AI-агентов.
Работай строго по этому файлу. Никогда не пропускай шаги.

---

## Старт: выбор режима

Спроси пользователя в начале каждой сессии:

"Выбери режим:
1. NEW PROJECT — новая идея с нуля
2. EXISTING PROJECT — доработка существующего проекта
3. PROJECT AUDIT — аудит существующего проекта без сборки"

Жди ответа. Дальнейший цикл зависит от режима.

---

## Режим NEW PROJECT и EXISTING PROJECT

```
Idea
  ↓
Designer Mode
  ↓
blueprint.md
  ↓
Reviewer Mode
  ↓
review.md + вердикт
  ↓
⏸ Human Approval
  ↓
Builder Mode
  ↓
Definition of Done Check
  ↓
Claude Code-ready проект
```

---

## Режим PROJECT AUDIT

```
Существующий проект
  ↓
Reviewer Mode (audit)
  ↓
audit_report.md
```

Builder не запускается. Designer не запускается.

---

## Шаг 1 — Designer Mode

Читай: `agents/designer/system_prompt.md`

Сначала определи Idea Maturity:
- Raw — задай уточняющие вопросы перед заполнением
- Refined — заполняй blueprint сразу, уточняй только пробелы
- Existing Project — читай существующие файлы, обновляй blueprint

Выбери паттерн из `/patterns`:
`research_agent.md` / `monitoring_agent.md` / `workflow_agent.md` / `rag_agent.md` / `sourcing_agent.md`
Если ни один не подходит — Custom, объясни почему.

Заполни все секции [REQUIRED] по шаблону `templates/blueprint_template.md`.
Сохрани: `projects/<название>/blueprint.md`

После сохранения — переходи к Reviewer Mode без паузы.

---

## Шаг 2 — Reviewer Mode

Читай: `agents/reviewer/system_prompt.md`

Входной файл: `projects/<название>/blueprint.md`
В режиме AUDIT: читаешь все файлы существующего проекта.

Проверь по чеклисту из 7 критериев.
Запиши результат:
- NEW/EXISTING: `projects/<название>/review.md`
- AUDIT: `projects/<название>/audit_report.md`

Используй шаблон: `templates/review_template.md`

Вердикт:
- APPROVE — переходи к Human Approval
- APPROVE WITH RISKS — покажи риски явно, переходи к Human Approval
- REJECT — покажи рекомендации, вернись к Designer Mode

При REJECT Builder не запускается.
При PROJECT AUDIT Builder не запускается никогда.

---

## Шаг 3 — Human Approval

Покажи пользователю `blueprint.md` и `review.md` вместе.
Скажи: "Blueprint и Review готовы. Прочитай оба файла и напиши 'одобряю'."

Жди явного "одобряю" или "approve".
Если пользователь вносит правки — обнови blueprint, перезапусти Reviewer, снова жди.
Не продолжай без явного одобрения.

---

## Шаг 4 — Builder Mode

Читай: `agents/builder/system_prompt.md`

Сначала проверь Blueprint Validation Checklist.
Если checklist не пройден — создай `blocking_questions.md`, жди ответов.

Создай Universal артефакты (обязательны всегда):
- `blueprint.md` (копия)
- `review.md` (копия)
- `CLAUDE.md`
- `README.md`
- `docs/acceptance_criteria.md`
- `tests/test_scenario.md`
- `data/sample_input.json`
- `data/sample_output.json`

Создай Stack-Specific артефакты по секции Tools & Stack в blueprint:
- Python → `src/main.py`, `src/config.py`, `src/models.py`
- n8n → `workflows/main_workflow.json`
- Telegram → `src/bot.py`
- Supabase → `db/schema.sql`

Перед созданием нового компонента проверь `/libraries/components`.

---

## Шаг 5 — Definition of Done

После сборки проверь:
- [ ] Все Universal артефакты созданы
- [ ] Stack-Specific артефакты соответствуют blueprint
- [ ] CLAUDE.md объясняет как запустить за 5 минут
- [ ] sample_input/output соответствуют blueprint
- [ ] Acceptance Criteria покрыты
- [ ] Нет открытых blocking_questions
- [ ] README содержит: описание, требования, запуск, пример

Напиши итог: "Definition of Done: passed / failed"
При failed — создай `TODO.md` со списком что осталось.

---

## Стек по умолчанию

- LLM: claude-sonnet-4-20250514
- Автоматизация: n8n
- База данных: Supabase
- Векторный поиск: Qdrant
- Уведомления: Telegram
- Язык кода: Python

Используй только то что указано в blueprint. Не добавляй лишнего.

---

## Главные принципы

Не предлагай агента там где хватит скрипта или n8n.
Не добавляй функции которых нет в blueprint.
Если blueprint неполный — задай вопросы, не угадывай.
Reviewer никогда не защищает работу Designer.
Builder никогда не запускается без явного одобрения.

---

## Структура проекта

```
agent-factory/
  CLAUDE.md
  PRD.md
  /agents
    /designer/system_prompt.md
    /reviewer/system_prompt.md
    /builder/system_prompt.md
  /templates
    blueprint_template.md
    review_template.md
    claude_md_template.md
    readme_template.md
    prompt_template.md
  /patterns
    research_agent.md
    monitoring_agent.md
    workflow_agent.md
    rag_agent.md
    sourcing_agent.md
  /libraries
    stack_decisions.md
    risk_library.md
    cost_library.md
    /components
  /projects
```

---

**Предложений в файле: 59**
