# Capital Asset Pricing Model (CAPM) Stock Analysis

This repository contains a comprehensive **Python/Jupyter Notebook** implementation of the **Capital Asset Pricing Model (CAPM)** to analyze and benchmark risk-adjusted performance metrics across individual high-beta equities (AAPL, MSFT, GOOG, AMZN) and S&P 500 benchmark indices (SPY).

## Project Features

1. **Automated Stock Prices Loading**: Integrates `yfinance` to automatically query and cache historical adjusted daily closing prices over a 5-year timeframe.
2. **Returns & Volatility Forecasting**: Calculates daily log returns and annualized return volatility scales.
3. **OLS CAPM Regression**: Fits Ordinary Least Squares (OLS) regressions via `statsmodels` of stock daily excess returns against SPY index excess returns to derive:
   - **Beta ($\beta$)**: Measure of systematic market risk.
   - **Alpha ($\alpha$)**: Excess return (active alpha performance).
   - **R-squared ($R^2$)**: Goodness-of-fit statistic indicating correlation strength.
4. **Risk-Adjusted Performance Ratios**: Annualizes and derives:
   - **Sharpe Ratio** (reward-to-variability ratio).
   - **Treynor Ratio** (reward-to-systematic risk ratio).
5. **Security Characteristic Line (SCL)**: Generates detailed regression line plots with confidence intervals using `seaborn.regplot`.

---

## Directory Structure

```text
├── capm_analysis.ipynb # Main Jupyter Notebook
├── requirements.txt    # Python dependencies
├── .gitignore          # Git exclusion rules
└── README.md           # Documentation
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
