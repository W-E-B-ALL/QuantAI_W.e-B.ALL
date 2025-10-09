# src/preprocessing/correlation_matrix.py
import pandas as pd
import os

def compute_correlation():
    # Caminho absoluto da raiz do projeto (sobe 3 níveis até a raiz)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

    # Caminho completo para o arquivo de entrada
    returns_path = os.path.join(base_dir, "wallet", "data", "processed", "returns.csv")

    if not os.path.exists(returns_path):
        raise FileNotFoundError(f"❌ Arquivo não encontrado: {returns_path}")

    # Detectar automaticamente o separador
    with open(returns_path, "r", encoding="utf-8") as f:
        first_line = f.readline()
    sep = ";" if ";" in first_line else ","
    print(f"📄 Separador detectado: '{sep}'")

    # Ler dados de retornos
    returns = pd.read_csv(returns_path, index_col=0, sep=sep)
    print(f"📊 Retornos carregados: {returns.shape[0]} linhas x {returns.shape[1]} colunas")

    if returns.empty or returns.shape[1] == 0:
        raise ValueError("❌ O arquivo returns.csv está vazio ou sem dados numéricos válidos.")

    # Converter tudo para numérico e eliminar colunas vazias
    returns = returns.apply(pd.to_numeric, errors="coerce").dropna(axis=1, how="all")

    # Calcular correlação
    correlation = returns.corr()

    # Caminho de saída (absoluto)
    output_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "correlation_matrix.csv")

    # Salvar matriz
    correlation.to_csv(output_file)
    print(f"✅ Matriz de correlação salva em: {output_file}")
    print(f"📈 Dimensão: {correlation.shape[0]} x {correlation.shape[1]}")

    return correlation


if __name__ == "__main__":
    compute_correlation()
