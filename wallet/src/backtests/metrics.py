import pandas as pd
import numpy as np
from typing import Dict, Optional


class PerformanceMetrics:
    """
    Calcula métricas de performance e risco para backtests de carteiras.
    """

    def __init__(self, equity_curve: pd.Series, benchmark: Optional[pd.Series] = None, risk_free: float = 0.0):
        """
        equity_curve: Série temporal do valor acumulado da carteira (ex: 1.0 → 1.25).
        benchmark: Série temporal do índice de referência (opcional).
        risk_free: Taxa livre de risco anual (ex: CDI = 0.11 = 11% a.a.).
        """
        self.equity = equity_curve.dropna()
        self.benchmark = benchmark
        self.rf = risk_free
        self.returns = self.equity.pct_change().dropna()

    def total_return(self) -> float:
        return self.equity.iloc[-1] / self.equity.iloc[0] - 1

    def annualized_return(self) -> float:
        days = (self.equity.index[-1] - self.equity.index[0]).days
        return (1 + self.total_return()) ** (252 / days) - 1

    def annualized_volatility(self) -> float:
        return self.returns.std() * np.sqrt(252)

    def sharpe_ratio(self) -> float:
        excess_ret = self.annualized_return() - self.rf
        vol = self.annualized_volatility()
        return excess_ret / vol if vol > 0 else np.nan

    def sortino_ratio(self) -> float:
        downside = self.returns[self.returns < 0].std() * np.sqrt(252)
        excess_ret = self.annualized_return() - self.rf
        return excess_ret / downside if downside > 0 else np.nan

    def max_drawdown(self) -> float:
        roll_max = self.equity.cummax()
        drawdown = self.equity / roll_max - 1
        return drawdown.min()

    def calmar_ratio(self) -> float:
        mdd = abs(self.max_drawdown())
        return self.annualized_return() / mdd if mdd > 0 else np.nan

    def tracking_error(self) -> float:
        if self.benchmark is None:
            return np.nan
        aligned = pd.concat([self.returns, self.benchmark.pct_change().dropna()], axis=1).dropna()
        aligned.columns = ["portfolio", "benchmark"]
        diff = aligned["portfolio"] - aligned["benchmark"]
        return diff.std() * np.sqrt(252)

    def information_ratio(self) -> float:
        if self.benchmark is None:
            return np.nan
        te = self.tracking_error()
        if te == 0 or np.isnan(te):
            return np.nan
        active_ret = self.annualized_return() - self.benchmark.pct_change().mean() * 252
        return active_ret / te

    def beta(self) -> float:
        if self.benchmark is None:
            return np.nan
        aligned = pd.concat([self.returns, self.benchmark.pct_change().dropna()], axis=1).dropna()
        cov = np.cov(aligned["portfolio"], aligned["benchmark"])[0, 1]
        var = np.var(aligned["benchmark"])
        return cov / var if var > 0 else np.nan

    def summary(self) -> Dict[str, float]:
        """Retorna um dicionário com todas as métricas principais."""
        return {
            "Total Return": self.total_return(),
            "Annualized Return": self.annualized_return(),
            "Volatility": self.annualized_volatility(),
            "Sharpe": self.sharpe_ratio(),
            "Sortino": self.sortino_ratio(),
            "Max Drawdown": self.max_drawdown(),
            "Calmar": self.calmar_ratio(),
            "Tracking Error": self.tracking_error(),
            "Information Ratio": self.information_ratio(),
            "Beta": self.beta(),
        }
