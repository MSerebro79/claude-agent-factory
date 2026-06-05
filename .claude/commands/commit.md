# Commit to claude-agent-factory

Перед коммитом обязательно проверь и подтверди следующее:

## 1. Проверь remote

```bash
git remote -v
```

Единственный допустимый remote:
```
origin  https://github.com/MarinaSerebro/claude-agent-factory.git
```

Если remote отличается — **остановись** и сообщи пользователю. Не коммить.

## 2. Проверь ветку

```bash
git branch --show-current
```

Коммиты идут только в ветку `main` (или feature-ветку с последующим PR в `main` этого репо).

## 3. Проверь статус

```bash
git status
git diff --staged
```

Убедись что коммитятся только файлы, относящиеся к этому проекту.

## 4. Создай коммит

Используй осмысленное сообщение на русском или английском. Формат:

```
<тип>: <краткое описание>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

Типы: `feat`, `fix`, `docs`, `refactor`, `chore`

## Важно

Этот репозиторий (`MarinaSerebro/claude-agent-factory`) — единственное место для хранения Agent Factory.  
Не пушить в другие репозитории, форки или remote-адреса без явного подтверждения пользователя.
