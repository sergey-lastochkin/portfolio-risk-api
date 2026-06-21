# Methodology

Portfolio Risk API uses simple historical risk calculations from portfolio holdings and historical prices.

## Portfolio Value and Weights

Portfolio value is calculated as:

```text
quantity * price
```

Asset weights are each asset value divided by total portfolio value.

Limitations:

- Prices are taken from the portfolio CSV, so stale input prices will create stale weights.
- Short positions and derivatives exposures are not modeled in Stage 2.

## Asset Classes

The portfolio CSV may include an optional `asset_class` column. If it is missing, the API infers a coarse class from simple asset names.

Examples:

- BTC, ETH, SOL are treated as crypto.
- EURUSD, GBPUSD, USDJPY are treated as FX.
- Other named assets are treated as equity by default.

Limitations:

- Asset class inference is a convenience for MVP stress tests.
- It is not a security master.
- Client or production use should provide explicit classification.

## Returns

Daily asset returns are simple percentage changes in historical prices.

Portfolio returns are calculated as weighted asset returns using the portfolio weights.

Limitations:

- Stage 2 uses static weights.
- Rebalancing, cash flows, dividends, fees, and FX conversion are not modeled.

## Volatility

Annualized volatility is calculated from daily portfolio returns:

```text
daily_return_std * sqrt(252)
```

Limitations:

- Volatility is backward-looking.
- It depends strongly on the selected historical window.
- Constant price series can produce near-zero volatility, which does not imply low future risk.

## Drawdown

Drawdown is calculated from the cumulative return curve. Max drawdown is the worst peak-to-trough loss in the sample.

Limitations:

- Drawdown is path-dependent.
- It only reflects losses observed in the supplied price history.

## VaR

Historical VaR is calculated from the lower tail of historical portfolio returns.

Sign convention:

```text
VaR is reported as a positive loss number.
```

For example, if the 5th percentile return is `-0.02`, the API reports `0.02`.

Limitations:

- Historical VaR is backward-looking.
- It does not estimate losses beyond the selected tail threshold.
- It can understate risk when the sample is short or calm.

## CVaR

Historical CVaR is the average loss in the tail beyond the VaR threshold.

Sign convention:

```text
CVaR is reported as a positive loss number.
```

Limitations:

- CVaR depends on tail observations in the supplied sample.
- With limited data, the tail estimate can be unstable.

## Correlation

The correlation matrix is calculated from asset return series.

Limitations:

- Correlation is unstable across regimes.
- Missing or synthetic data can make correlations misleading.

## Concentration

The richer report includes first-pass concentration metrics:

- top 1 position weight;
- top 3 position weight;
- effective number of positions, calculated as `1 / sum(weight^2)`.

Limitations:

- Concentration is based on static portfolio weights.
- It does not include liquidity, factor exposure, issuer mapping, or hidden derivatives exposure.

## Stress Tests

Stage 2 uses deterministic scenario shocks:

- all assets down 5%;
- all assets down 10%;
- equity down 10%;
- crypto down 20%;
- FX move 2%.

Each scenario returns total portfolio PnL, portfolio PnL percent, and per-asset impact.

Limitations:

- Shocks are simplified and deterministic.
- They are not forecasts.
- They are not trading signals.
- No liquidity liquidation model is included.
- No full margin, funding, tax, or transaction-cost model is included.

## Provenance and Coverage

Reports include basic metadata:

- portfolio source;
- prices source;
- data start and end date;
- observation count;
- assets in the portfolio;
- assets with price history;
- missing assets.

Limitations:

- Provenance is only as reliable as the inputs supplied to the API.
- Upload metadata identifies uploaded filenames, not an audited external data source.

## Limitations

- Historical estimates are backward-looking.
- Sample data is synthetic.
- No broker margin model is included.
- Liquidity, taxes, funding, and execution constraints are not modeled.
- The API does not provide investment advice.
