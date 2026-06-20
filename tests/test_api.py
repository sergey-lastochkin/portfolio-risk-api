from fastapi.testclient import TestClient

from portfolio_risk_api.app import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_metadata_endpoint():
    response = client.get("/metadata")

    assert response.status_code == 200
    assert response.json()["name"] == "Portfolio Risk API"


def test_risk_summary_endpoint():
    response = client.post(
        "/risk/summary",
        json={
            "portfolio_path": "data/sample_portfolio.csv",
            "prices_path": "data/sample_prices.csv",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["portfolio_value"] > 0
    assert "weights" in payload
    assert "var_95" in payload


def test_risk_summary_validation_error():
    response = client.post(
        "/risk/summary",
        json={
            "portfolio_path": "data/missing.csv",
            "prices_path": "data/sample_prices.csv",
        },
    )

    assert response.status_code == 400


def test_risk_report_endpoint_contract():
    response = client.post(
        "/risk/report",
        json={
            "portfolio_path": "data/sample_portfolio.csv",
            "prices_path": "data/sample_prices.csv",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "correlation_matrix" in payload
    assert "notes" in payload
    assert "limitations" in payload


def test_unknown_asset_error_is_clear(tmp_path):
    portfolio_path = tmp_path / "portfolio.csv"
    prices_path = tmp_path / "prices.csv"
    portfolio_path.write_text("asset,quantity,price\nAAPL,1,100\nMSFT,1,200\n", encoding="utf-8")
    prices_path.write_text(
        "date,AAPL\n2026-01-01,100\n2026-01-02,101\n2026-01-03,102\n",
        encoding="utf-8",
    )

    response = client.post(
        "/risk/summary",
        json={"portfolio_path": str(portfolio_path), "prices_path": str(prices_path)},
    )

    assert response.status_code == 400
    assert "missing portfolio assets" in response.json()["detail"]
