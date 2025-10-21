import pandas as pd
import numpy as np
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.backtests.simulator import PortfolioBacktester

def test_simulation_without_rebalance():
    # cria série de preços simples e linear
    dates = pd.date_range("2020-01-01", periods=5)
    data = pd.DataFrame({
        "A": [100, 101, 102, 103, 104],
        "B": [50, 49, 48, 47, 46]
    }, index=dates)
    weights = {"A": 0.5, "B": 0.5}

    bt = PortfolioBacktester(data, weights, rebalance=False)
    curve, log = bt.run()

    # curva deve crescer ou cair de forma consistente
    assert isinstance(curve, pd.Series)
    assert len(curve) == len(data) - 1
    assert curve.iloc[-1] > 0

def test_simulation_with_rebalance():
    dates = pd.date_range("2020-01-01", periods=10)
    data = pd.DataFrame({
        "A": np.linspace(100, 200, 10),
        "B": np.linspace(100, 50, 10)
    }, index=dates)
    weights = {"A": 0.5, "B": 0.5}

    bt = PortfolioBacktester(data, weights, rebalance=True, rebalance_threshold=0.05)
    curve, log = bt.run()

    # deve haver pelo menos um rebalanceamento
    assert len(log) >= 1
    assert "date" in log[0]
