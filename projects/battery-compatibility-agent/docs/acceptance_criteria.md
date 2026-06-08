# Acceptance Criteria: Battery Compatibility Agent

## Критерии приёмки

### AC-1: Известный бренд — High confidence
**Дано:** `python3 src/main.py "BL1850B"`
**Ожидается:**
- Список содержит серию Makita 18V LXT
- Минимум 5 моделей устройств
- Confidence = High
- Хотя бы одна ссылка на источник
- Время выполнения < 15 секунд

### AC-2: Популярная потребительская батарея
**Дано:** `python3 src/main.py "iPhone 14 battery"`
**Ожидается:**
- Список содержит iPhone 14, iPhone 14 Plus
- Не содержит устройства других брендов
- Confidence = High или Medium
- Время < 15 секунд

### AC-3: Неизвестный артикул — Low confidence без падения
**Дано:** `python3 src/main.py "LP803048XYZ999"`
**Ожидается:**
- Агент не падает с ошибкой
- Confidence = Low
- Сообщение о недостаточности данных
- Предложение уточнить запрос

### AC-4: Структурированный вывод
**Дано:** любой валидный запрос
**Ожидается:**
- Поля: battery_name, brand (или null), compatible_devices, confidence, sources
- sources содержит хотя бы 1 ссылку при High/Medium confidence

### AC-5: Guardrails соблюдены
**Проверка:** в выводе нет устройств, которых нет в тексте источников
**Метод:** сравни вывод с контентом sources вручную на 3 примерах
