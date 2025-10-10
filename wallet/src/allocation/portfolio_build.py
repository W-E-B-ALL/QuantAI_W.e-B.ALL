# src/allocation/portfolio_builder.py
import os
import pandas as pd
import numpy as np


# ============================================================
# Funções auxiliares
# ============================================================

def load_portfolio(profile: str, base_dir: str) -> pd.Series:
    """
    Carrega o portfólio otimizado de um perfil (Conservador, Moderado, Arrojado).
    Corrige índices numéricos (ex: '0.0'), remove NaNs e normaliza pesos.
    """
    file_path = os.path.join(base_dir,"wallet", "data", "results", f"portfolio_{profile}.csv")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Portfólio não encontrado: {file_path}")
    
    # Lê o CSV como Series
    df = pd.read_csv(file_path, index_col=0, header=None)

    # Converte o índice para string e remove entradas não textuais
    df.index = df.index.astype(str)
    df = df[~df.index.str.replace('.', '', 1).str.isnumeric()]  # remove índices numéricos como "0.0"
    df = df[df.index.notna()]
    df = df.dropna()

    s = df.squeeze()
    s.name = profile

    # Normaliza (garante soma = 1)
    if s.sum() != 0:
        s = s / s.sum()

    # Checagem
    soma = s.sum()
    if abs(soma - 1) > 1e-6:
        print(f" Aviso: a soma dos pesos em {profile} não é 1 (soma = {soma:.4f}). Corrigindo automaticamente.")
        s = s / soma

    return s


def adjust_by_age(age: int) -> dict:
    """
    Define os pesos entre perfis conforme a idade do investidor.
    """
    if age <= 35:
        return {"Arrojado": 0.8, "Moderado": 0.2, "Conservador": 0.0}
    elif 36 <= age <= 50:
        return {"Arrojado": 0.4, "Moderado": 0.5, "Conservador": 0.1}
    elif 51 <= age <= 60:
        return {"Arrojado": 0.2, "Moderado": 0.6, "Conservador": 0.2}
    else:
        return {"Arrojado": 0.0, "Moderado": 0.3, "Conservador": 0.7}

# ============================================================
# Função principal
# ============================================================

def build_personalized_portfolio(age: int):
    """
    Combina os portfólios otimizados em uma carteira personalizada por idade.
    Salva o resultado em data/results/personalized_portfolio_<idade>anos.csv
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    print(f"📂 Diretório base: {base_dir}")

    # Carregar os portfólios otimizados
    portfolios = {
        "Conservador": load_portfolio("Conservador", base_dir),
        "Moderado": load_portfolio("Moderado", base_dir),
        "Arrojado": load_portfolio("Arrojado", base_dir),
    }

    # Ponderação entre perfis conforme idade
    profile_weights = adjust_by_age(age)
    print(f"🎯 Pesos entre perfis para idade {age}: {profile_weights}")

    # Unir todos os ativos envolvidos
    all_assets = set().union(*[p.index for p in portfolios.values()])
    combined = pd.Series(0.0, index=sorted(all_assets))

    # Combinar carteiras
    for profile, weight in profile_weights.items():
        combined += portfolios[profile].reindex(combined.index, fill_value=0) * weight

    # Normalizar e checar soma final
    combined = combined / combined.sum()
    soma_total = combined.sum()

    results_dir = os.path.join(base_dir,"wallet", "data", "results")
    os.makedirs(results_dir, exist_ok=True)
    output_path = os.path.join(results_dir, f"personalized_portfolio_{age}anos.csv")
    combined.to_csv(output_path)

    print(f" Carteira personalizada para idade {age} salva em: {output_path}")
    print(f"Alocação total: {soma_total:.2f} (esperado ≈ 1.00)")
    return combined


# ============================================================
# Execução direta
# ============================================================

if __name__ == "__main__":
    build_personalized_portfolio(age=40)
