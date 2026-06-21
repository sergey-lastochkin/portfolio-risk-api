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
    assert "concentration" in payload
    assert "top_positions" in payload
    assert "provenance" in payload
    assert "coverage" in payload
    assert "notes" in payload
    assert "limitations" in payload


def test_old_summary_endpoint_still_works():
    response = client.post("/risk/summary", json={})

    assert response.status_code == 200
    assert response.json()["portfolio_value"] > 0


def test_upload_summary_endpoint_works():
    with (
        open("data/sample_portfolio.csv", "rb") as portfolio_file,
        open("data/sample_prices.csv", "rb") as prices_file,
    ):
        response = client.post(
            "/risk/summary/upload",
            files={
                "portfolio_file": ("portfolio.csv", portfolio_file, "text/csv"),
                "prices_file": ("prices.csv", prices_file, "text/csv"),
            },
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["portfolio_value"] > 0
    assert payload["stress_tests"][0]["scenario_name"]


def test_upload_report_endpoint_works():
    with (
        open("data/sample_portfolio.csv", "rb") as portfolio_file,
        open("data/sample_prices.csv", "rb") as prices_file,
    ):
        response = client.post(
            "/risk/report/upload",
            files={
                "portfolio_file": ("portfolio.csv", portfolio_file, "text/csv"),
                "prices_file": ("prices.csv", prices_file, "text/csv"),
            },
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["concentration"]["top_1_weight"] > 0
    assert payload["coverage"]["assets_in_portfolio"] == 4
    assert payload["provenance"]["portfolio_source"] == "upload:portfolio.csv"


def test_upload_missing_file_returns_error():
    with open("data/sample_portfolio.csv", "rb") as portfolio_file:
        response = client.post(
            "/risk/summary/upload",
            files={"portfolio_file": ("portfolio.csv", portfolio_file, "text/csv")},
        )

    assert response.status_code == 422


def test_upload_wrong_file_type_returns_clear_error():
    with open("data/sample_prices.csv", "rb") as prices_file:
        response = client.post(
            "/risk/summary/upload",
            files={
                "portfolio_file": (
                    "portfolio.txt",
                    b"asset,quantity,price\nAAPL,1,100\n",
                    "text/plain",
                ),
                "prices_file": ("prices.csv", prices_file, "text/csv"),
            },
        )

    assert response.status_code == 400
    assert "must be a CSV" in response.json()["detail"]


def test_upload_var_level_is_validated():
    with (
        open("data/sample_portfolio.csv", "rb") as portfolio_file,
        open("data/sample_prices.csv", "rb") as prices_file,
    ):
        response = client.post(
            "/risk/summary/upload?var_level=0.99",
            files={
                "portfolio_file": ("portfolio.csv", portfolio_file, "text/csv"),
                "prices_file": ("prices.csv", prices_file, "text/csv"),
            },
        )

    assert response.status_code == 422


def test_path_based_var_level_is_fixed_at_95_percent():
    response = client.post("/risk/summary", json={"var_level": 0.99})

    assert response.status_code == 422


def test_path_based_malformed_csv_returns_clear_error(tmp_path):
    portfolio_path = tmp_path / "portfolio.csv"
    portfolio_path.write_text(
        'asset,quantity,price\nAAPL,"1,100\n',
        encoding="utf-8",
    )

    response = client.post(
        "/risk/summary",
        json={
            "portfolio_path": str(portfolio_path),
            "prices_path": "data/sample_prices.csv",
        },
    )

    assert response.status_code == 400
    assert "Invalid portfolio CSV" in response.json()["detail"]


def test_top_positions_sorted_by_weight():
    response = client.post("/risk/report", json={})

    assert response.status_code == 200
    top_positions = response.json()["top_positions"]
    weights = [item["weight"] for item in top_positions]
    assert weights == sorted(weights, reverse=True)


def test_concentration_metrics_are_sane():
    response = client.post("/risk/report", json={})

    assert response.status_code == 200
    concentration = response.json()["concentration"]
    assert 0 < concentration["top_1_weight"] <= concentration["top_3_weight"] <= 1
    assert concentration["effective_number_of_positions"] > 0


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
