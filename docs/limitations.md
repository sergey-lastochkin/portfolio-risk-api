# Limitations

Portfolio Risk API is a Stage 2 local MVP.

- Included data is sample/synthetic.
- The API does not provide investment advice.
- The API does not send orders.
- The API does not connect to brokers.
- The API does not use live trading credentials.
- Historical metrics do not predict future losses.
- VaR and CVaR are simplified historical estimates.
- Stress tests are deterministic simplified shocks.
- Scenario results are diagnostics, not forecasts.
- Asset class inference is a simple fallback and should not replace a security master.
- Upload provenance identifies supplied files, not an audited external data source.
- No full margin, funding, tax, liquidity, or liquidation model is included.
- Results depend on input data quality.
- Position values are assumed to share one valuation currency; currency conversion is not modeled.
