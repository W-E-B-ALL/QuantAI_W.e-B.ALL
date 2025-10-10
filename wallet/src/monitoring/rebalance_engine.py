import os
import pandas as pd
import numpy as np
import logging
from src.monitoring.drift_checker import compute_drift


# === CONFIGURAÇÃO DE LOG ===
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "wallet", "logs"))
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "monitoring.log"),
    level=logging.INFO,
    format="%(asctime)s [REBALANCE_ENGINE] %(levelname)s: %(message)s"
)


def should_rebalance(drift: pd.Series, threshold: float = 0.05) -> bool:
    """Retorna True se o drift máximo exceder a tolerância."""
    max_drift = drift.abs().max()
    print(f"Drift máximo observado: {max_drift:.2%}")
    logging.info(f"Drift máximo observado: {max_drift:.2%}")
    return max_drift > threshold


def rebalance_portfolio(target_weights: pd.Series) -> pd.Series:
    """Retorna os pesos rebalanceados iguais ao alvo."""
    new_weights = (target_weights / target_weights.sum()).copy()
    new_weights.name = "Peso_Rebalanceado"
    return new_weights


def auto_rebalance(age: int = 40, threshold: float = 0.05, window_days: int = 90):
    """Executa o rebalanceamento proporcional com validação e logging."""
    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        results_dir = os.path.join(base_dir, "wallet", "data", "results")
        raw_dir = os.path.join(base_dir, "wallet", "data", "raw")
        os.makedirs(results_dir, exist_ok=True)

        target_path = os.path.join(results_dir, f"personalized_portfolio_{age}anos.csv")
        prices_path = os.path.join(raw_dir, "prices_raw.csv")

        if not os.path.exists(target_path):
            raise FileNotFoundError(f"Carteira alvo não encontrada: {target_path}")
        if not os.path.exists(prices_path):
            raise FileNotFoundError(f"Arquivo de preços não encontrado: {prices_path}")

        target = pd.read_csv(target_path, index_col=0).squeeze("columns")
        target = target / target.sum()

        prices = pd.read_csv(prices_path, index_col=0, parse_dates=True)
        prices = prices.ffill().bfill().replace(0, np.nan).dropna(axis=1, how="any")

        if prices.shape[0] < 60:
            raise ValueError("Histórico de preços insuficiente (<60 dias).")

        # Limitar aos últimos N dias
        cutoff = prices.index.max() - pd.Timedelta(days=window_days)
        prices = prices.loc[prices.index >= cutoff]
        print(f"Usando dados dos últimos {window_days} dias ({prices.index.min().date()} → {prices.index.max().date()})")

        returns = prices.pct_change(fill_method=None).fillna(0)
        cumulative_returns = (1 + returns).prod()
        cumulative_returns = cumulative_returns.reindex(target.index).fillna(1.0)

        current_value = target * cumulative_returns
        current_weights = current_value / current_value.sum()

        drift = compute_drift(current_weights, target)

        if should_rebalance(drift, threshold):
            print(f"⚠️  Drift excedeu tolerância ({threshold:.0%}). Rebalanceando...")
            logging.warning(f"Drift excedeu tolerância ({threshold:.0%})")

            new_portfolio = rebalance_portfolio(target)
            output_file = os.path.join(results_dir, f"rebalanced_portfolio_{age}anos.csv")
            new_portfolio.to_csv(output_file)

            post_drift = compute_drift(new_portfolio, target).abs().max()
            print(f"Carteira reequilibrada salva em: {output_file}")
            print(f"Drift após rebalanceamento: {post_drift:.2%}")
            logging.info(f"Carteira rebalanceada. Drift final: {post_drift:.2%}")

            return new_portfolio
        else:
            print(f"Nenhum rebalanceamento necessário (drift ≤ {threshold:.0%}).")
            logging.info("Drift dentro da faixa, rebalanceamento não necessário.")
            return target

    except Exception as e:
        logging.error(f"Erro geral no rebalanceamento: {e}")
        raise


if __name__ == "__main__":
    auto_rebalance(age=40, threshold=0.05, window_days=90)
