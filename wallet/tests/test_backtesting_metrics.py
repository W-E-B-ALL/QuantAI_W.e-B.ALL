import pandas as pd
import numpy as np
import sys, os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from  src.backtests.metrics import PerformanceMetrics

def test_metrics_basic_values():
    dates = pd.date_range("2020-01-01", periods=6)
    curve = pd.Series([1.0, 1.02, 1.04, 1.03, 1.05, 1.06], index=dates)

    metrics = PerformanceMetrics(curve)
    summary = metrics.summary()

    # todas as métricas principais devem estar presentes
    expected_keys = [
        "Total Return", "Annualized Return", "Volatility",
        "Sharpe", "Sortino", "Max Drawdown", "Calmar"
    ]
    for key in expected_keys:
        assert key in summary, f"Métrica ausente: {key}"

    # total return positivo
    assert summary["Total Return"] > 0
