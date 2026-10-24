# Portfolio Risk API

[![CI](https://github.com/sergey-lastochkin/portfolio-risk-api/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/sergey-lastochkin/portfolio-risk-api/actions/workflows/ci.yml)

кидаете два CSV, позиции и цены, а получаете риск портфеля: волатильность, просадку, VaR и CVaR, корреляции, концентрацию и стресс-сценарии. в JSON или сразу HTML-отчётом.

можно потыкать вживую: [демо](https://portfolio-risk-api-eb40.onrender.com/?lang=ru), [загрузить свои CSV](https://portfolio-risk-api-eb40.onrender.com/demo), [готовый отчёт](https://portfolio-risk-api-eb40.onrender.com/demo/sample-report), [Swagger](https://portfolio-risk-api-eb40.onrender.com/docs). хостинг бесплатный, поэтому после простоя первый запрос будит сервис секунд 30-60.

сделал, потому что риск обычно считают кто во что горазд, в разных ноутбуках и табличках, и у каждого своя методика. а тут одни и те же метрики через API, методика зафиксирована, входные файлы проверяются, и в каждом ответе написано, на каких данных посчитано. подключается к дашборду, отчёту по расписанию или внутреннему инструменту.

```bash
git clone https://github.com/sergey-lastochkin/portfolio-risk-api.git
cd portfolio-risk-api
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn portfolio_risk_api.app:app --reload     # http://127.0.0.1:8000/docs
```

или в Docker: `docker build -t portfolio-risk-api . && docker run --rm -p 8000:8000 portfolio-risk-api`.

## как выглядит ответ

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

`var_95` и `cvar_95` - потери при уровне 95%, положительным числом. полный отчёт (`/risk/report`, `/risk/report/upload`) добавляет корреляции, концентрацию, крупнейшие позиции, покрытие активов и окно данных. колонку `asset_class` в CSV можно не заполнять: BTC сам поймёт как крипту, EURUSD как валюту, AAPL как акцию.

методика - в [methodology.md](docs/methodology.md), примеры метрик - в [risk_metric_examples.md](docs/risk_metric_examples.md), как задеплоить на Render - в [deployment_render.md](docs/deployment_render.md).

## о чём помнить

данные в `data/` выдуманные, это пример формата. метрики смотрят назад, VaR и CVaR будущие потери не предсказывают. стресс-тесты простые, фиксированные шоки, без маржи, ликвидности, налогов и пересчёта валют, все позиции в одной валюте. эндпоинты с путями к файлам работают только локально, на Render они выключены, там загружайте файлы, до 5 МБ каждый. и это не инвестсовет и не торговая система, к брокеру ничего не подключено.

для разработки: `make test && make lint` и `python -m compileall -q src tests`, CI гоняет то же самое на локальных примерах.

Сергей Ласточкин · [t.me/metaanswer](https://t.me/metaanswer) · [другие проекты](https://github.com/sergey-lastochkin)
