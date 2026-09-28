# Portfolio Risk API

[![CI](https://github.com/sergey-lastochkin/portfolio-risk-api/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/sergey-lastochkin/portfolio-risk-api/actions/workflows/ci.yml)

**FastAPI-сервис риск-метрик портфеля: загрузите два CSV — позиции и цены — и
получите волатильность, просадку, VaR/CVaR, корреляции, концентрацию и
стресс-сценарии в JSON или HTML-отчёте.**

**Живое демо:** [portfolio-risk-api-eb40.onrender.com](https://portfolio-risk-api-eb40.onrender.com/?lang=ru) ·
[загрузка CSV](https://portfolio-risk-api-eb40.onrender.com/demo) ·
[пример отчёта](https://portfolio-risk-api-eb40.onrender.com/demo/sample-report) ·
[Swagger](https://portfolio-risk-api-eb40.onrender.com/docs)
<sub>(бесплатный хостинг: первый запрос после простоя будит сервис около 30–60 с)</sub>

## Какую проблему решает

Риск портфеля часто считают в разрозненных ноутбуках и таблицах с разной
методикой. Здесь одни и те же метрики доступны через API с зафиксированной
методикой, валидацией входных файлов и описанием происхождения данных в каждом
ответе — их можно подключить к дашборду, отчёту по расписанию или внутреннему
инструменту.

## Для кого

- Аналитики и студенты, которым нужен готовый бэкенд риск-метрик.
- Команды, которые встраивают расчёт риска в свои отчёты через HTTP.

## Запуск за 2 минуты

```bash
git clone https://github.com/sergey-lastochkin/portfolio-risk-api.git
cd portfolio-risk-api
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn portfolio_risk_api.app:app --reload     # http://127.0.0.1:8000/docs
```

Или в Docker: `docker build -t portfolio-risk-api . && docker run --rm -p 8000:8000 portfolio-risk-api`.

## Пример результата

```bash
curl -X POST http://127.0.0.1:8000/risk/summary/upload \
  -F "portfolio_file=@data/sample_portfolio.csv" \
  -F "prices_file=@data/sample_prices.csv"
```

```json
{
  "portfolio_value": 27800.0,
  "weights": {"AAPL": 0.0683, "MSFT": 0.0755, "BTC": 0.4676, "EURUSD": 0.3885},
  "annualized_volatility": 0.0987,
  "max_drawdown": -0.006,
  "var_95": 0.0052,
  "cvar_95": 0.0057,
  "observations": 29,
  "stress_tests": [{"scenario_name": "all_assets_down_5pct", "portfolio_pnl": -1390.0}]
}
```

`var_95` и `cvar_95` — положительные числа потерь при уровне 95 %. Полный отчёт
(`/risk/report`, `/risk/report/upload`) добавляет корреляционную матрицу,
метрики концентрации, крупнейшие позиции, покрытие активов и метаданные окна
данных. `asset_class` в CSV необязателен: BTC определяется как крипта, EURUSD —
как валюта, AAPL — как акция.

Все эндпоинты — в Swagger (`/docs`); методика — [docs/methodology.md](docs/methodology.md),
примеры метрик — [docs/risk_metric_examples.md](docs/risk_metric_examples.md),
деплой на Render — [docs/deployment_render.md](docs/deployment_render.md).

## Ограничения

- Данные в `data/` синтетические — это пример формата, а не исследование рынка.
- Исторические метрики смотрят назад; VaR и CVaR не предсказывают будущие потери.
- Стресс-тесты — упрощённые детерминированные шоки; моделей маржи, ликвидности,
  налогов и конвертации валют нет (все позиции в одной валюте).
- Эндпоинты с путями к файлам — только для локального запуска; на Render они
  отключены, используйте загрузку (до 5 МБ на файл).
- Не инвестиционная рекомендация и не торговая система: нет подключения к брокеру
  и отправки заявок.

## Разработка

```bash
make test && make lint
python -m compileall -q src tests
```

CI запускает эти проверки на локальных примерах данных и не обращается к рынку.

## Автор

Сергей Ласточкин · Telegram [@metaanswer](https://t.me/metaanswer) ·
[другие проекты](https://github.com/sergey-lastochkin)
