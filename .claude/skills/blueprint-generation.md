# Blueprint Generation

Справочник по выбору шаблона и правилам заполнения Blueprint Contract.

## Какой шаблон использовать

| Solution Type | Шаблон |
|---|---|
| Agent / Multi-Agent | `blueprint_template.md` (в корне проекта) |
| Script / Workflow | `templates/script_blueprint_template.md` |
| Prompt | Только `projects/<название>/prompt.md` с текстом промпта |

> Примечание: `blueprint_template.md` находится в корне проекта, не в `templates/`.
> Ссылка `templates/blueprint_template.md` в других местах — известная несогласованность.

## Ключевые правила

1. Все секции `[REQUIRED]` обязательны — Builder не запускается без них.
2. Предположения помечай: `[ASSUMPTION]`. Собирай в секцию `## Assumptions`.
3. Нет противоречий между секциями (Use Cases ↔ Workflow, Criteria ↔ MVP Scope).
4. Kill Decision = СТРОИТЬ обязателен для запуска Builder.
5. После заполнения: сохрани `projects/<название>/blueprint.md`, обнови статус на `in progress`.

## Blueprint Validation Checklist

Builder запускается только если все пункты выполнены:

- [ ] Все секции [REQUIRED] заполнены
- [ ] Kill Decision = СТРОИТЬ
- [ ] Complexity указана (S/M/L/XL)
- [ ] Cost Estimation заполнена
- [ ] Acceptance Criteria ≥ 2 пункта
- [ ] Non-goals заполнены
- [ ] Guardrails заполнены
- [ ] Evaluation Plan конкретный
- [ ] Agent Justification заполнен (для Agent/Multi-Agent)
- [ ] Stack level выбран (Minimal / Standard / Advanced)
- [ ] Assumptions явно помечены если есть

## Жизненный цикл статуса

`draft` → `approved` → `in progress` → `done`

Обновляй поле `**Статус:**` при переходе между этапами.
