# src/preprocessing/returns_calc.py
import pandas as pd
import numpy as np
import os

def compute_returns():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    raw_path = os.path.join(base_dir, "data", "raw", "prices_raw.csv")
    # Verificação
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {raw_path}")
    # Leitura dos preços
    prices = pd.read_csv(raw_path, index_col=0, parse_dates=True)
    # Cálculo dos retornos mensais
    returns = prices.pct_change().dropna()
    if returns.empty :
        raise ValueError("Nenhum retorno pôde ser calculado (talvez faltam dados históricos.")
    annual_returns = returns.mean() * 12
    annual_volatility = returns.std() * np.sqrt(12)
    
    stats = pd.DataFrame({
        "Retorno_Esperado": annual_returns,
        "Volatilidade": annual_volatility
    })
    
    processed_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)
    returns.to_csv(os.path.join(processed_dir, "returns.csv"))
    stats.to_csv(os.path.join(processed_dir, "stats.csv"))
    
    print("Retornos e estatísticas salvos em data/processed/")
    print(f"returns.csv → {returns.shape[0]} linhas x {returns.shape[1]} colunas")
    print(f"stats.csv → {stats.shape[0]} ativos")
    return returns, stats


if __name__ == "__main__":
    compute_returns()
