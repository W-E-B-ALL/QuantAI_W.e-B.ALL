import os
import pandas as pd
import numpy as np
import logging


# === CONFIGURAÇÃO DE LOG ===
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "wallet", "logs"))
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "monitoring.log"),
    level=logging.INFO,
    format="%(asctime)s [DRIFT_CHECKER] %(levelname)s: %(message)s"
)


def compute_drift(current_weights: pd.Series, target_weights: pd.Series, relative: bool = False) -> pd.Series:
    """Calcula o drift entre pesos atuais e pesos-alvo."""
    try:
        aligned = current_weights.reindex(target_weights.index, fill_value=0)
        aligned = aligned / aligned.sum()
        target_weights = target_weights / target_weights.sum()

        if relative:
            drift = (aligned - target_weights) / target_weights.replace(0, 1e-9)
        else:
            drift = aligned - target_weights
        return drift
    except Exception as e:
        logging.error(f"Erro ao calcular drift: {e}")
        raise


def check_drift(age: int = 40, threshold: float = 0.05, relative: bool = False, window_days: int = 90) -> pd.DataFrame:
    """Verifica o drift da carteira com validação e logging."""
    try:
        # Caminhos
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        results_dir = os.path.join(base_dir, "wallet", "data", "results")
        docs_dir = os.path.join(base_dir, "wallet", "data", "docs")
        raw_dir = os.path.join(base_dir, "wallet", "data", "raw")
        os.makedirs(docs_dir, exist_ok=True)

        # Arquivos
        target_path = os.path.join(results_dir, f"personalized_portfolio_{age}anos.csv")
        prices_path = os.path.join(raw_dir, "prices_raw.csv")

        if not os.path.exists(target_path):
            raise FileNotFoundError(f"Carteira alvo não encontrada: {target_path}")
        if not os.path.exists(prices_path):
            raise FileNotFoundError(f"Arquivo de preços não encontrado: {prices_path}")

        # === Leitura e validação ===
        target_df = pd.read_csv(target_path, index_col=0)
        target = target_df.squeeze("columns") / target_df.squeeze("columns").sum()

        prices = pd.read_csv(prices_path, index_col=0, parse_dates=True)
        prices = prices.ffill().bfill().replace(0, np.nan).dropna(axis=1, how="any")

        if prices.shape[0] < 60:
            raise ValueError("Histórico de preços insuficiente (<60 dias).")

        # Janela de 90 dias
        if isinstance(prices.index, pd.DatetimeIndex):
            cutoff = prices.index.max() - pd.Timedelta(days=window_days)
            prices = prices.loc[prices.index >= cutoff]

        returns = prices.pct_change(fill_method=None).fillna(0)
        cumulative_returns = (1 + returns).prod()
        cumulative_returns = cumulative_returns.reindex(target.index).fillna(1.0)

        current_value = target * cumulative_returns
        current_weights = current_value / current_value.sum()

        drift = compute_drift(current_weights, target, relative)

        drift_report = pd.DataFrame({
            "Peso_Alvo": target,
            "Peso_Atual": current_weights,
            "Drift": drift
        })

        drift_path = os.path.join(docs_dir, f"drift_report_{age}anos.csv")
        drift_report.to_csv(drift_path)

        max_drift = drift.abs().max()
        msg = f"Drift máximo {max_drift:.2%} (limite {threshold:.2%})"
        if max_drift > threshold:
            print(f"{msg}")
            logging.warning(msg)
        else:
            print(f"{msg}")
            logging.info(msg)

        return drift_report

    except Exception as e:
        logging.error(f"Erro geral em check_drift: {e}")
        raise


if __name__ == "__main__":
    check_drift(age=40, threshold=0.05, window_days=90)
