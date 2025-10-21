import pandas as pd
import numpy as np
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.backtests.rebalance import apply_rebalance

def test_rebalance_triggers_on_drift():
    dates = pd.date_range("2020-01-01", periods=6)
    data = pd.DataFrame({
        "A": [100, 105, 110, 120, 130, 140],
        "B": [100, 95, 90, 85, 80, 75]
    }, index=dates)
    weights = {"A": 0.5, "B": 0.5}

    portfolio_value, log = apply_rebalance(data, weights, threshold=0.05)
    assert isinstance(portfolio_value, pd.Series)
    assert len(log) >= 1, "O drift deve acionar pelo menos um rebalanceamento"
