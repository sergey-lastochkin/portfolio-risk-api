"""English and Russian copy for the public HTML demo."""

from typing import Any

SUPPORTED_LANGUAGES = {"en", "ru"}


def normalize_language(value: str | None) -> str:
    """Return a supported UI language, defaulting to English."""

    return value if value in SUPPORTED_LANGUAGES else "en"


UI_TEXT: dict[str, dict[str, Any]] = {
    "en": {
        "meta_description": "Portfolio risk calculations from portfolio and price CSV data.",
        "nav": {"overview": "Overview", "upload": "Upload CSV", "api": "API"},
        "footer": ("Research tool. No investment advice, trading signals, or order execution."),
        "report": {
            "title": "Portfolio risk",
            "ready": "CALCULATION READY",
            "subtitle": (
                "Historical volatility, drawdown, tail-risk, and concentration diagnostics "
                "from supplied data."
            ),
            "upload": "Upload your CSVs",
            "data": "DATA",
            "sample": "Synthetic sample",
            "uploaded": "Uploaded CSVs",
            "period": "PERIOD",
            "coverage": "COVERAGE",
            "assets": "assets",
            "method": "METHOD",
            "method_value": "Historical, 95%",
            "sample_title": "Demonstration data.",
            "sample_note": (
                "Prices and positions are synthetic and used only to demonstrate the API "
                "and interface."
            ),
            "portfolio_value": "Portfolio value",
            "units": "arbitrary units",
            "volatility": "Annualized volatility",
            "daily_returns": "from daily returns",
            "drawdown": "Maximum drawdown",
            "peak_to_trough": "peak to trough",
            "var": "VaR 95%",
            "var_note": "historical loss threshold",
            "cvar": "CVaR 95%",
            "cvar_note": "average loss beyond VaR",
            "observations": "Observations",
            "observations_note": "daily returns",
            "structure": "STRUCTURE",
            "positions": "Positions and weights",
            "concentration": "CONCENTRATION",
            "capital_distribution": "Capital distribution",
            "largest_position": "Largest position",
            "top_three": "Top three positions",
            "effective_positions": "Effective positions",
            "concentration_note": (
                "Concentration describes the current portfolio structure and does not "
                "model exit liquidity."
            ),
            "scenario_analysis": "SCENARIO ANALYSIS",
            "stress_scenarios": "Simplified stress scenarios",
            "stress_note": (
                "Fixed shocks are applied to current positions. This is a diagnostic, "
                "not a forecast."
            ),
            "value_change": "Value change",
            "dependencies": "DEPENDENCIES",
            "correlation": "Return correlation",
            "correlation_note": (
                "Historical linear relationships between assets over the supplied window."
            ),
            "asset": "Asset",
            "how_to_read": "HOW TO READ",
            "shows": "What the report shows",
            "notes": [
                "Metrics are calculated from the supplied price history.",
                "VaR and CVaR are shown as positive loss numbers.",
                "Stress scenarios use predetermined price shocks.",
            ],
            "limitations_label": "LIMITATIONS",
            "outside_scope": "What remains outside the scope",
            "limitations": [
                "Historical metrics do not predict future losses.",
                "Scenarios do not model liquidation, margin, or market impact.",
                "The service has no broker connection and provides no investment advice.",
            ],
            "portfolio": "PORTFOLIO",
            "prices": "PRICE HISTORY",
            "price_rows": "PRICE ROWS",
        },
        "upload": {
            "eyebrow": "YOUR DATA",
            "title": "Build a report from two CSV files",
            "subtitle": (
                "Upload a portfolio and price history. Files are validated and processed "
                "for this request and are not stored by the demo."
            ),
            "files": "Files for calculation",
            "portfolio": "Portfolio",
            "portfolio_note": ("Required columns: asset, quantity, price. Optional: asset_class."),
            "prices": "Price history",
            "prices_note": (
                "Requires date and positive numeric prices for every asset. Minimum three rows."
            ),
            "submit": "Calculate risk",
            "sample_eyebrow": "READY SAMPLE",
            "sample_title": "Review without uploading",
            "sample_text": (
                "Open a ready report or download the synthetic CSV files used to build it."
            ),
            "open_sample": "Open sample report",
            "download_portfolio": "Download portfolio",
            "download_prices": "Download price history",
            "api_docs": "API documentation",
            "notice": (
                "The sample is fully synthetic. It demonstrates the input format and report "
                "structure, not real market research."
            ),
        },
        "error": {
            "eyebrow": "INPUT ERROR",
            "title": "Check the uploaded CSV files",
            "schema": (
                "The portfolio requires asset, quantity, and price. Price history requires "
                "date and one column for every asset."
            ),
            "back": "Return to upload",
            "sample": "Open sample report",
            "missing_files": "Select both a portfolio CSV and a price history CSV.",
            "sample_unavailable": "Sample file is unavailable",
        },
    },
    "ru": {
        "meta_description": "Расчёт риска портфеля по CSV с позициями и историей цен.",
        "nav": {"overview": "Обзор", "upload": "Загрузить CSV", "api": "API"},
        "footer": ("Исследовательский инструмент. Без торговых рекомендаций и отправки заявок."),
        "report": {
            "title": "Риск портфеля",
            "ready": "РАСЧЁТ ГОТОВ",
            "subtitle": (
                "Историческая оценка волатильности, просадки, хвостового риска и "
                "концентрации по переданным данным."
            ),
            "upload": "Загрузить свои CSV",
            "data": "ДАННЫЕ",
            "sample": "Синтетический пример",
            "uploaded": "Загруженные CSV",
            "period": "ПЕРИОД",
            "coverage": "ПОКРЫТИЕ",
            "assets": "активов",
            "method": "МЕТОД",
            "method_value": "Исторический, 95%",
            "sample_title": "Демонстрационные данные.",
            "sample_note": ("Цены и позиции созданы только для проверки работы API и интерфейса."),
            "portfolio_value": "Стоимость портфеля",
            "units": "условные единицы",
            "volatility": "Годовая волатильность",
            "daily_returns": "по дневным доходностям",
            "drawdown": "Максимальная просадка",
            "peak_to_trough": "от пика до минимума",
            "var": "VaR 95%",
            "var_note": "порог исторического убытка",
            "cvar": "CVaR 95%",
            "cvar_note": "средний убыток за порогом",
            "observations": "Наблюдения",
            "observations_note": "дневные доходности",
            "structure": "СТРУКТУРА",
            "positions": "Позиции и веса",
            "concentration": "КОНЦЕНТРАЦИЯ",
            "capital_distribution": "Распределение капитала",
            "largest_position": "Крупнейшая позиция",
            "top_three": "Три крупнейшие",
            "effective_positions": "Эффективное число позиций",
            "concentration_note": (
                "Показатель концентрации описывает структуру текущего портфеля и не "
                "учитывает ликвидность выхода из позиций."
            ),
            "scenario_analysis": "СЦЕНАРНЫЙ АНАЛИЗ",
            "stress_scenarios": "Упрощённые стресс-сценарии",
            "stress_note": (
                "Фиксированные шоки применяются к текущим позициям. Это диагностический "
                "расчёт, а не прогноз."
            ),
            "value_change": "Изменение стоимости",
            "dependencies": "ЗАВИСИМОСТИ",
            "correlation": "Корреляция доходностей",
            "correlation_note": ("Историческая линейная связь между активами на выбранном окне."),
            "asset": "Актив",
            "how_to_read": "КАК ЧИТАТЬ",
            "shows": "Что показывает отчёт",
            "notes": [
                "Метрики рассчитаны по загруженной истории цен.",
                "VaR и CVaR показаны как положительные величины возможного убытка.",
                "Стресс-сценарии используют заранее заданные изменения цен.",
            ],
            "limitations_label": "ОГРАНИЧЕНИЯ",
            "outside_scope": "Что остаётся за рамками",
            "limitations": [
                "Исторические показатели не предсказывают будущие потери.",
                "Сценарии не моделируют ликвидацию, маржу и рыночный импакт.",
                "Сервис не подключён к брокеру и не формирует торговые рекомендации.",
            ],
            "portfolio": "ПОРТФЕЛЬ",
            "prices": "ИСТОРИЯ ЦЕН",
            "price_rows": "СТРОК ЦЕН",
        },
        "upload": {
            "eyebrow": "СВОИ ДАННЫЕ",
            "title": "Собрать отчёт по двум CSV-файлам",
            "subtitle": (
                "Загрузите состав портфеля и историю цен. Файлы проверяются и "
                "обрабатываются в рамках запроса, демо их не сохраняет."
            ),
            "files": "Файлы для расчёта",
            "portfolio": "Портфель",
            "portfolio_note": (
                "Обязательные колонки: asset, quantity, price. Дополнительно можно "
                "передать asset_class."
            ),
            "prices": "История цен",
            "prices_note": (
                "Нужны date и положительные числовые цены для каждого актива. "
                "Минимум три наблюдения."
            ),
            "submit": "Рассчитать риск",
            "sample_eyebrow": "ГОТОВЫЙ ПРИМЕР",
            "sample_title": "Посмотреть без загрузки",
            "sample_text": (
                "Откройте готовый отчёт или скачайте синтетические CSV, на которых он рассчитан."
            ),
            "open_sample": "Открыть готовый отчёт",
            "download_portfolio": "Скачать портфель",
            "download_prices": "Скачать историю цен",
            "api_docs": "Документация API",
            "notice": (
                "Пример полностью синтетический. Он показывает формат входных данных и "
                "структуру отчёта, а не результат реального исследования рынка."
            ),
        },
        "error": {
            "eyebrow": "ОШИБКА ВХОДНЫХ ДАННЫХ",
            "title": "Проверьте загруженные CSV",
            "schema": (
                "В портфеле нужны asset, quantity и price. В истории цен нужны date и "
                "отдельная колонка для каждого актива."
            ),
            "back": "Вернуться к загрузке",
            "sample": "Открыть готовый пример",
            "missing_files": "Выберите CSV портфеля и CSV с историей цен.",
            "sample_unavailable": "Файл примера недоступен",
        },
    },
}


def ui_text(language: str) -> dict[str, Any]:
    """Return UI copy for a normalized language."""

    return UI_TEXT[normalize_language(language)]
