# Battery Compatibility Agent

CLI-агент для поиска совместимости аккумуляторов. Введи название батареи — получи список устройств и брендов, с которыми она совместима.

## Требования

- Python 3.10+
- Anthropic API key
- Exa API key

## Установка

```bash
pip install anthropic exa-py python-dotenv pydantic
```

Создай файл `.env` в корне проекта:

```
ANTHROPIC_API_KEY=sk-ant-...
EXA_API_KEY=...
```

## Запуск

```bash
python3 src/main.py "<название батареи>"
```

### Примеры

```bash
python3 src/main.py "BL1850B"
python3 src/main.py "iPhone 14 battery"
python3 src/main.py "18650 Samsung 30Q"
python3 src/main.py "LP803048"
```

## Пример вывода

```
Battery: BL1850B (Makita)

Compatible devices:
  Brand: Makita | Series: 18V LXT
  Models: DDF484, DHR242, DGA504, DTD154, DSS611, DJV182 (+38 more)

  Brand: Makita | Series: 18V Compact
  Models: DDF453, DTD148, DSS501

Additional compatibility (3rd party):
  - Hitachi/HiKOKI 18V tools (partial — verify model before purchase)

Confidence: High
Sources:
  - https://www.makitatools.com/products/details/BL1850B
  - https://www.amazon.com/...
```

## Уровни уверенности

| Уровень | Значение |
|---|---|
| High | Официальный сайт производителя или проверенный маркетплейс |
| Medium | Форумы, user manuals, косвенные источники |
| Low | Данных мало, проверь вручную перед покупкой |

## Ограничения

- Не предоставляет цены и ссылки на покупку
- Не сравнивает физические параметры (ёмкость, напряжение, размер)
- Не выполняет обратный поиск (устройство → батарея)
- Результаты зависят от доступности информации в вебе
