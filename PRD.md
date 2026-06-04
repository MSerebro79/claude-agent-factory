# PRD: Agent Factory
**Version:** 0.9
**Date:** June 4, 2026
**Status:** In Progress
**Owner:** Mary Silver

---

## 1. Problem

Каждый новый AI-проект начинается одинаково: сырая идея, размытое мышление, долгое додумывание. Нет стандарта — как проверить идею, нет структуры — как спроектировать систему, нет процесса — как быстро перейти к сборке.

Результат: хорошие идеи зависают или собираются хаотично без единого стандарта качества.

Дополнительная проблема: большую часть времени не создаются новые системы, а эволюционируют существующие. Нужен режим для аудита и рефакторинга, а не только для создания.

---

## 2. Solution

Система из трёх агентов с human-in-the-loop.

**Designer Agent** превращает сырую идею в Blueprint Contract.
**Reviewer Agent** критикует Blueprint как адвокат дьявола — ищет причины НЕ строить.
**Builder Agent** собирает структуру проекта строго по одобренному Blueprint.
**Человек** одобряет переход после Review.

---

## 3. Режимы работы

| Режим | Когда | Что делает Designer |
|---|---|---|
| NEW PROJECT | Новая идея с нуля | Задаёт вопросы, заполняет blueprint полностью |
| EXISTING PROJECT | Проект уже есть, нужна доработка | Читает существующие файлы, обновляет blueprint |
| PROJECT AUDIT | Аудит и рефакторинг без сборки | Передаёт сразу Reviewer, Builder не запускается |

Designer предлагает режим на основе входных данных пользователя.
Пользователь подтверждает или изменяет предложенный режим.
PROJECT AUDIT использует только Reviewer — без Designer и Builder.

**Audit Type** (только для PROJECT AUDIT):
- Architecture Audit — структура, агенты, разделение ответственности
- Product Audit — соответствие решения реальной проблеме
- Cost Audit — стоимость операций, избыточные API-вызовы
- Agent Audit — промпты, failure modes, качество LLM-шагов

---

## 4. Target User

Сейчас: только личное использование (Mary Silver).
Позже: возможно как инструмент для консалтинга.

Контекст:
- Работает в Claude Code
- Стек: Python, Supabase, Qdrant, n8n, Telegram
- Параллельно ведёт несколько проектов (MI/CI, GTM, Mimi Lingua Leo и другие)
- Нужна скорость проверки идей и независимая критика

---

## 5. Jobs To Be Done

| Job | Важность |
|---|---|
| Быстро проверить: стоит ли строить идею | Критично |
| Получить независимую критику до начала сборки | Критично |
| Не тратить время на идеи которые разваливаются | Высокая |
| Иметь единый стандарт для всех проектов | Высокая |
| Аудировать существующие проекты | Высокая |
| Получить готовую папку проекта для Claude Code | Средняя |

---

## 6. Non-Goals (v0.4)

- Telegram-интерфейс
- Сохранение blueprints в базу данных
- Сравнение нескольких идей между собой
- Веб-интерфейс
- Multi-agent инфраструктура (агенты работают последовательно через файлы)

---

## 7. Core Workflow

```
Старт: пользователь выбирает режим
  ↓
NEW PROJECT / EXISTING PROJECT:

  Idea Maturity Check
    ↓
  Designer Agent
    → выбирает паттерн из /patterns
    → заполняет blueprint по шаблону
    → сохраняет projects/<название>/blueprint.md
    ↓
  Reviewer Agent
    → читает blueprint.md
    → пишет projects/<название>/review.md
    → вердикт: APPROVE / APPROVE WITH RISKS / REJECT
    ↓
  ⏸ Human Approval
    ↓
  Builder Agent
    → проверяет Validation Checklist
    → создаёт Artifact Contract
    ↓
  Definition of Done Check
    ↓
  Claude Code-ready проект

PROJECT AUDIT:

  Reviewer Agent
    → читает существующие файлы проекта
    → пишет audit_report.md
    → без Builder
```

---

## 8. Idea Maturity

Designer определяет зрелость идеи до начала проектирования.

| Тип | Описание | Что делает Designer |
|---|---|---|
| Raw | Первая мысль, нет деталей | Задаёт уточняющие вопросы, заполняет blueprint с нуля |
| Refined | Есть понимание пользователя и процесса | Сразу заполняет blueprint, уточняет только пробелы |
| Existing Project | Проект уже существует, нужна доработка | Читает существующие файлы, обновляет blueprint |

---

## 9. Reviewer Agent

Reviewer — независимый агент с противоположной задачей по отношению к Designer.

**Designer:** сделать проект жизнеспособным.
**Reviewer:** найти причины НЕ строить проект.

Reviewer читает blueprint.md и проверяет по чеклисту:

| Критерий | Вопрос |
|---|---|
| Лишняя сложность | Можно ли решить задачу проще? |
| Неподтверждённые предположения | Какие допущения не проверены? |
| Скрытые зависимости | Что может сломаться извне? |
| ROI | Оправдана ли стоимость ценностью? |
| Автоматизация несуществующей боли | Боль реальна или придумана? |
| Данные | Данные доступны или их ещё нет? |
| Альтернативы | Хватит ли скрипта / n8n / GPT напрямую? |

**Вердикт + Confidence:**

- **APPROVE** — проект жизнеспособен
- **APPROVE WITH RISKS** — можно строить, риски выводятся явно перед approval
- **REJECT** — Builder заблокирован по умолчанию; пользователь может выполнить Human Override и запустить Builder несмотря на вердикт

**Confidence:**
- High — достаточно данных для уверенного вывода
- Medium — есть неопределённость
- Low — данных недостаточно, вывод предварительный

Пример: `Verdict: APPROVE WITH RISKS | Confidence: High`

При REJECT без Override — Reviewer пишет конкретные рекомендации для Designer.

---

## 10. Outcome & ROI Assessment

Обязательная секция в Blueprint.
Designer заполняет, Reviewer проверяет.

| Поле | Варианты |
|---|---|
| Value Type | Revenue / Cost Saving / Learning / Strategic Asset / Personal Productivity |
| Business Value | Low / Medium / High |
| Expected ROI | Low / Medium / High |
| Кто платит или экономит | описание |
| Альтернатива без агента | что делать вместо |
| Почему сейчас | зачем строить именно сейчас |

Примеры Value Type по проектам:

| Проект | Value Type |
|---|---|
| Mimi Lingua Leo | Learning |
| MI/CI Agent | Strategic Asset |
| GTM Agent | Revenue |
| Contractor Agent | Personal Productivity |

Если Business Value Low и ROI Low — Reviewer автоматически рекомендует REJECT.

---

## 11. Artifact Contract

Разделён на Universal (всегда) и Stack-Specific (зависит от решения).

**Universal — обязательны для любого проекта:**

| Артефакт | Путь |
|---|---|
| Blueprint | `/blueprint.md` |
| Review | `/review.md` |
| CLAUDE.md | `/CLAUDE.md` |
| README.md | `/README.md` |
| Acceptance Criteria | `/docs/acceptance_criteria.md` |
| Test Scenario | `/tests/test_scenario.md` |
| Sample Input | `/data/sample_input.json` |
| Sample Output | `/data/sample_output.json` |

**Stack-Specific — определяются в Blueprint:**

| Стек | Артефакты |
|---|---|
| Python | `/src/main.py`, `/src/config.py`, `/src/models.py` |
| n8n | `/workflows/main_workflow.json` |
| Telegram Bot | `/src/bot.py` |
| Supabase | `/db/schema.sql` |

Builder создаёт только то, что указано в секции Tools & Stack blueprint.

---

## 12. Definition of Done

Builder завершён только если:

- [ ] Все Universal артефакты созданы
- [ ] Stack-Specific артефакты соответствуют blueprint
- [ ] CLAUDE.md объясняет как запустить за 5 минут
- [ ] sample_input/output соответствуют blueprint
- [ ] Acceptance Criteria покрыты кодом или test_scenario
- [ ] Нет открытых blocking_questions
- [ ] README содержит: описание, требования, запуск, пример
- [ ] Reuse Check выполнен: Builder проверил `/libraries/components`; если создан новый компонент — объяснил почему существующий не подошёл

Если пункт не выполнен — Builder создаёт `TODO.md` с остатком.

---

## 13. Component Library

Builder сначала ищет готовый компонент в `/libraries/components`, затем генерирует новый.

Планируемые компоненты (накапливаются после каждых 5 проектов):

| Компонент | Описание |
|---|---|
| telegram_notifier | Отправка сообщений в Telegram |
| supabase_storage | CRUD операции с Supabase |
| web_search | Поиск через Exa / Tavily |
| scheduler | Запуск по расписанию через n8n |
| research_pipeline | Базовый Research Agent workflow |

После каждых 5 реализованных проектов — Pattern Review:
пересмотр паттернов и компонентов, добавление новых если появился повторяющийся блок.

---

## 14. File Structure

```
agent-factory/
  CLAUDE.md
  PRD.md

  /agents
    /designer
      system_prompt.md
    /reviewer
      system_prompt.md        ← новое в v0.4
    /builder
      system_prompt.md

  /templates
    blueprint_template.md
    review_template.md        ← новое в v0.4
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
    /components               ← накапливается со временем

  /projects
    /dacha-contractor-agent
    /mimi-lingua-leo
    /mi-ci-agent
```

---

## 15. Factory Metrics

Метрики самой фабрики — накапливаются в `/projects/factory_log.md` после каждого прогона.

| Метрика | Что показывает |
|---|---|
| Количество проектов всего | объём использования |
| Количество REJECT | качество входящих идей |
| Количество APPROVE WITH RISKS | частота сложных решений |
| Процент проектов дошедших до реализации | реальная ценность фабрики |
| Самые используемые паттерны | что реально строится |
| Самые переиспользуемые компоненты | что стоит развивать |
| Среднее время от идеи до Blueprint | скорость Designer |

Через 10–20 проектов это станет источником знаний о том, какие идеи стоит строить.

---

## 16. Success Metrics

| Метрика | Цель | Когда |
|---|---|---|
| Kill Decisions признаны правильными через 30 дней | > 70% | Ежемесячно |
| Проектов дошедших до реализации после Approval | > 50% | Через 2 недели после сборки |
| Перепроектирований после Approval | < 20% | После каждой сборки |
| Definition of Done с первого раза | > 80% | После каждой сборки |
| Reviewer REJECT до показа пользователю | видим паттерн через 10 проектов | Накопительно |

---

## 16. Roadmap

**v0.1 — done**
Designer + Builder, Blueprint template, базовый CLAUDE.md.

**v0.2 — done**
Blueprint как строгий контракт, Architecture Review, Kill Decision, Cost, Complexity, 5 паттернов.

**v0.3 — done**
Artifact Contract, Definition of Done, Architecture Review Checklist, Idea Maturity, метрики качества.

**v0.4 — done**
Reviewer Agent как независимая роль, режимы NEW / EXISTING / AUDIT, Universal + Stack-Specific артефакты, Outcome & ROI Assessment, Component Library структура.

**v0.5 — done**
Reviewer: независимая оценка, Confidence уровень, Human Override, Value Type, Designer предлагает режим, Audit Type, Reuse Check, Factory Metrics.

**v0.6 — done**
Blueprint: Guardrails + Non-goals + Evaluation Plan. Reviewer: структурированный чеклист + Agent Score. Версионирование во всех файлах.

**v0.7 — done**
Agent Qualification Test (6 вопросов). Fake Multi-Agent проверка. Automation ROI.

**v0.8 — done**
Solution Classification: Prompt / Script / n8n / Agent / Multi-Agent. Отдельный script_blueprint_template. Builder умеет Script и n8n.

**v0.9 — current**
Workflow как отдельный класс (Script ≠ Workflow). Alternative Solutions — Designer обязан обосновать почему нельзя проще. Future Evolution — ожидаемый путь развития решения. Builder разделён на 4 специализированных билдера внутри одного файла: Prompt / Script / Workflow / Agent / Multi-Agent.

**→ Следующий шаг: первый реальный прогон**
1. Mimi Lingua Leo (EXISTING PROJECT)
2. MI/CI Agent (NEW PROJECT)
3. Dacha Contractor Agent (NEW PROJECT)

**v0.5 — next**
Сохранение blueprints и review в Supabase, /libraries наполнение первыми компонентами.

**v1.0 — future**
Telegram-интерфейс, поиск по прошлым проектам через Qdrant, Pattern Review автоматизация.

---

## 17. Test Cases

**Test 1 — Research Agent / NEW PROJECT**
Dacha Contractor Agent.
Проверяет: полный цикл Designer → Reviewer → Builder.

**Test 2 — Monitoring Agent / NEW PROJECT**
Competitor Ad Monitor.
Проверяет: расписание + diff + алёрт.

**Test 3 — PROJECT AUDIT**
Mimi Lingua Leo (существующий проект).
Проверяет: Reviewer без Designer и Builder, audit_report.md.
