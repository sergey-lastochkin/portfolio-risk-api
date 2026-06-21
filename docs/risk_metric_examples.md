# Risk Metric Examples

Small examples for explaining the project in conversation.

## Portfolio Value

If the portfolio has:

```text
AAPL: 10 shares * 190 = 1,900
MSFT: 5 shares * 420 = 2,100
```

Total portfolio value is:

```text
1,900 + 2,100 = 4,000
```

## Weights

Using the same portfolio:

```text
AAPL weight = 1,900 / 4,000 = 47.5%
MSFT weight = 2,100 / 4,000 = 52.5%
```

Weights show how much each asset contributes to the total portfolio value.

## Returns

If AAPL goes from `100` to `102`, the return is:

```text
(102 / 100) - 1 = 2%
```

Portfolio return is the weighted average of asset returns.

## Annualized Volatility

Volatility measures how much returns move around.

The API calculates daily return volatility and annualizes it:

```text
daily volatility * sqrt(252)
```

It is backward-looking. Low historical volatility does not guarantee low future risk.

## Max Drawdown

Drawdown is the fall from a previous high.

Example:

```text
Portfolio rises to 100
Then falls to 85
Drawdown = -15%
```

Max drawdown is the worst fall in the provided history.

## VaR as Positive Loss Number

VaR looks at bad historical days.

If the 5th percentile return is:

```text
-2%
```

The API reports:

```text
VaR 95% = 2%
```

So VaR is shown as a positive loss number, not as a negative return.

## CVaR as Positive Loss Number

CVaR looks at the average of the bad tail days beyond VaR.

If the worst tail days average:

```text
-3%
```

The API reports:

```text
CVaR 95% = 3%
```

CVaR is usually larger than or equal to VaR because it looks deeper into the tail.

## Correlation Matrix

Correlation shows how assets moved together in the supplied history.

Example:

```text
1.0 means two assets moved almost together
0.0 means no clear linear relationship
-1.0 means they moved in opposite directions
```

Correlations can change quickly across market regimes.

## Stress Tests

Stress tests apply simple shocks.

Example:

```text
Portfolio value = 100,000
Shock = -10%
Estimated PnL = -10,000
```

Stage 2 uses simple deterministic shocks. It is a diagnostic, not a full scenario engine.
