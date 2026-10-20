"""Execute every code cell of the notebook offline, against a synthetic market
with known betas, so the analysis is checked end to end without network."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import pytest  # noqa: E402
import yfinance as yf  # noqa: E402

NOTEBOOK = Path(__file__).resolve().parent.parent / "capm_analysis.ipynb"
TRUE_BETA = {"AAPL": 1.5, "KO": 0.5}  # the rest default to 1.0


def _fake_download(tickers, start=None, end=None, **kwargs):
    rng = np.random.default_rng(7)
    idx = pd.bdate_range(start, end)
    market = rng.normal(0.0004, 0.01, len(idx))
    rets = {}
    for t in tickers:
        if t == "SPY":
            rets[t] = market
        elif t == "LIN":
            rets[t] = np.full(len(idx), np.nan)  # a ticker with no history
        else:
            beta = TRUE_BETA.get(t, 1.0)
            rets[t] = beta * market + rng.normal(0, 0.004, len(idx))
    prices = 100 * (1 + pd.DataFrame(rets, index=idx)).cumprod()
    prices["LIN"] = np.nan
    cols = pd.MultiIndex.from_product([["Close", "Open"], prices.columns])
    return pd.DataFrame(
        np.hstack([prices.values, prices.values]), index=idx, columns=cols
    )


@pytest.fixture(scope="module")
def ns():
    mp = pytest.MonkeyPatch()
    mp.setattr(yf, "download", _fake_download)
    mp.setattr("matplotlib.pyplot.show", lambda *a, **k: None)
    namespace = {}
    cells = json.loads(NOTEBOOK.read_text())["cells"]
    for cell in cells:
        if cell["cell_type"] == "code":
            exec(compile("".join(cell["source"]), str(NOTEBOOK), "exec"), namespace)
    yield namespace
    mp.undo()


def test_notebook_runs_and_drops_empty_tickers(ns):
    assert "LIN" not in ns["data"].columns
    assert "LIN" not in ns["stocks"]
    assert len(ns["stocks"]) == len(ns["tickers"]) - 2  # minus SPY and LIN


def test_regression_recovers_known_betas(ns):
    for ticker, beta in TRUE_BETA.items():
        assert ns["results"][ticker]["beta"] == pytest.approx(beta, abs=0.05)
    assert ns["results"]["MSFT"]["beta"] == pytest.approx(1.0, abs=0.05)
    assert ns["results"]["AAPL"]["r_squared"] > 0.8


def test_summary_table_covers_every_stock_and_spy(ns):
    summary = ns["df_summary"]
    assert set(summary.index) == set(ns["stocks"]) | {"SPY (Market)"}
    assert summary.loc["AAPL", "Beta (Systematic Risk)"] == pytest.approx(1.5, abs=0.05)


def test_monte_carlo_var_is_ordered(ns):
    assert 0 < ns["var_95"] < ns["var_99"]
    assert ns["cvar_95"] >= ns["var_95"]
    assert ns["sim_horizon_returns"].shape == (ns["N_SIMULATIONS"],)
