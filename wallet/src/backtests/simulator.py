import pandas as pd
import numpy as np
from typing import Dict, Tuple, List
from .rebalance import apply_rebalance


class PortfolioBacktester:
    def __init__(
        self,
        prices: pd.DataFrame,
        weights: Dict[str, float],
        rebalance: bool = False,
        rebalance_threshold: float = 0.05,
        rebalance_frequency: str = "M"
    ):
        """
        prices: DataFrame com colunas de ativos e índice de datas.
        weights: dicionário com pesos da carteira {'BTC-USD': 0.3, 'IMAB11.SA': 0.7}.
        rebalance: se True, ativa o rebalanceamento.
        rebalance_threshold: desvio percentual que aciona o rebalanceamento (±5%).
        rebalance_frequency: intervalo de rebalanceamento ('M', 'Q', 'Y').
        """
        self.prices = prices
        self.weights = weights
        self.rebalance = rebalance
        self.threshold = rebalance_threshold
        self.frequency = rebalance_frequency
        self.results = None
        self.log = []

    def compute_returns(self) -> pd.DataFrame:
        """Calcula retornos percentuais dos ativos."""
        return self.prices.pct_change().dropna()

    def run(self) -> Tuple[pd.Series, List[Dict]]:
        """Executa o backtest completo da carteira."""
        returns = self.compute_returns()
        weights_df = pd.DataFrame(self.weights, index=returns.index)
        portfolio_returns = (returns * weights_df).sum(axis=1)
        portfolio_value = (1 + portfolio_returns).cumprod()

        if self.rebalance:
            portfolio_value, self.log = apply_rebalance(
                prices=self.prices,
                weights=self.weights,
                threshold=self.threshold,
                frequency=self.frequency
            )

        self.results = portfolio_value
        return portfolio_value, self.log

    def get_summary(self):
        """Resumo simples do resultado."""
        total_return = self.results.iloc[-1] - 1
        annualized_return = (self.results.iloc[-1]) ** (252 / len(self.results)) - 1
        print(f"Retorno Total: {total_return:.2%}")
        print(f"Retorno Anualizado: {annualized_return:.2%}")
