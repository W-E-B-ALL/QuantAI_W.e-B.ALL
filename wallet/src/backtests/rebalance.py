import pandas as pd
import numpy as np
from typing import Dict, Tuple, List


def apply_rebalance(
    prices: pd.DataFrame,
    weights: Dict[str, float],
    threshold: float = 0.05,
    frequency: str = "M"
) -> Tuple[pd.Series, List[Dict]]:
    """
    Simula o rebalanceamento da carteira com base em drift de pesos
    ou periodicidade fixa.

    Parameters
    ----------
    prices : pd.DataFrame
        DataFrame com preços ajustados dos ativos.
    weights : dict
        Pesos-alvo iniciais da carteira (ex: {'BTC-USD': 0.3, 'IMAB11.SA': 0.7}).
    threshold : float, optional
        Banda de tolerância para desvio de peso (default = 0.05 → ±5%).
    frequency : str, optional
        Frequência de rebalanceamento (default = 'M' → mensal).

    Returns
    -------
    portfolio_value : pd.Series
        Série temporal com valor acumulado da carteira.
    log : list
        Lista de dicionários com histórico de rebalanceamentos.
    """

    returns = prices.pct_change().dropna()
    dates = returns.index
    assets = list(weights.keys())
    log = []

    # valores iniciais
    portfolio_value = pd.Series(index=dates, dtype=float)
    current_weights = weights.copy()
    capital = 1.0
    capital_alloc = {a: capital * w for a, w in current_weights.items()}

    last_rebalance = dates[0]
    portfolio_value.iloc[0] = capital

    for i, date in enumerate(dates[1:], start=1):
        # atualiza capital de cada ativo
        for a in assets:
            capital_alloc[a] *= (1 + returns.loc[date, a])
        capital = sum(capital_alloc.values())
        portfolio_value.iloc[i] = capital

        # cálculo dos pesos atuais
        current_alloc = {a: capital_alloc[a] / capital for a in assets}

        # check rebalanceamento por tempo
        time_to_rebalance = (date - last_rebalance).days >= pd.Timedelta(f"30D").days \
            if frequency == "M" else False

        # check rebalanceamento por drift
        drift_detected = any(
            abs(current_alloc[a] - weights[a]) > threshold for a in assets
        )

        if drift_detected or time_to_rebalance:
            log.append({
                "date": date,
                "event": "rebalance",
                "weights_before": current_alloc.copy(),
                "capital_before": capital,
            })

            # rebalanceia aos pesos originais
            for a in assets:
                capital_alloc[a] = capital * weights[a]

            last_rebalance = date

    portfolio_value.ffill(inplace=True)
    return portfolio_value, log
