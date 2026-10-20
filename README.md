# Capital Asset Pricing Model (CAPM) Stock Analysis

<p align="center">
  <img src="docs/logo.svg" alt="capm-analysis logo" width="128" />
</p>

This repository contains a comprehensive **Python/Jupyter Notebook** implementation of the **Capital Asset Pricing Model (CAPM)** to analyze and benchmark risk-adjusted performance across a 54-stock universe spanning all 11 GICS sectors, against the S&P 500 (SPY) as the market benchmark, plus a Monte Carlo Value at Risk for an equal-weight portfolio of those stocks.

## Project Features

1. **Automated Stock Prices Loading**: Integrates `yfinance` to download adjusted daily closing prices from 2019 through 2023. Tickers that return no history are dropped instead of breaking the analysis.
2. **Returns & Volatility**: Calculates daily simple returns and annualized return and volatility.
3. **OLS CAPM Regression**: Fits Ordinary Least Squares (OLS) regressions via `statsmodels` of stock daily excess returns against SPY index excess returns to derive:
   - **Beta ($\beta$)**: Measure of systematic market risk.
   - **Alpha ($\alpha$)**: Excess return (active alpha performance).
   - **R-squared ($R^2$)**: Goodness-of-fit statistic indicating correlation strength.
4. **Risk-Adjusted Performance Ratios**: Annualizes and derives:
   - **Sharpe Ratio** (reward-to-variability ratio).
   - **Treynor Ratio** (reward-to-systematic risk ratio).
5. **Security Characteristic Line (SCL)**: Plots regression lines with confidence intervals using `seaborn.regplot` for a representative low-to-high beta spread of four stocks.
6. **Monte Carlo Value at Risk**: Draws 10,000 correlated 21-day return paths from the stocks' multivariate normal distribution and reports 95% and 99% VaR and 95% CVaR for an equal-weight portfolio.

## Results

The committed notebook was executed on 2026-10-19 over 55 tickers (54 stocks plus SPY) and 1,258 trading days. For a $1,000,000 equal-weight portfolio over a 21-day horizon:

| Measure  | Loss     | Share of portfolio |
| -------- | -------- | ------------------ |
| 95% VaR  | $83,291  | 8.33%              |
| 99% VaR  | $122,603 | 12.26%             |
| 95% CVaR | $107,213 | 10.72%             |

The simulation is seeded, so rerunning reproduces these numbers as long as the downloaded prices are unchanged.

---

## Directory Structure

```text
├── capm_analysis.ipynb   # Main Jupyter Notebook, committed with outputs
├── tests/                # Offline test that runs every notebook cell
├── requirements.txt      # Python dependencies
├── .gitignore            # Git exclusion rules
└── README.md             # Documentation
```

---

## Installation & Usage

### 1. Dependencies
Setup your local python environment:

```bash
pip install -r requirements.txt
```

### 2. Execute Jupyter Notebook
Start the Jupyter interface:

```bash
jupyter notebook capm_analysis.ipynb
```

Run all cells to download live market data, execute CAPM regressions, calculate risk-adjusted performance tables, and view the SCL regression plots.

### 3. Run the tests

```bash
pip install -r requirements.txt pytest
pytest -q tests
```

The test executes every code cell against a synthetic market with known betas, with `yfinance` stubbed out, so it needs no network. It checks that the regressions recover those betas and that the VaR figures are ordered sensibly.

---

## Model Rationale & Formulas

### Capital Asset Pricing Model (CAPM)
$$E(R_i) = R_f + \beta_i \left(E(R_m) - R_f\right)$$

Where:
- $E(R_i)$ is expected stock return.
- $R_f$ is risk-free return rate (assumed $4.0\%$ annualized).
- $\beta_i$ is systematic risk coefficient: $\beta_i = \frac{\text{Cov}(R_i, R_m)}{\text{Var}(R_m)}$.
- $E(R_m)$ is market return rate.

### Performance Indicators
- **Sharpe Ratio**:
  $$\text{Sharpe} = \frac{R_i - R_f}{\sigma_i}$$
- **Treynor Ratio**:
  $$\text{Treynor} = \frac{R_i - R_f}{\beta_i}$$
