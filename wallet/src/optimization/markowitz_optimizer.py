# src/optimization/markowitz_optimizer.py
import os
import numpy as np
import pandas as pd
import cvxpy as cp

def load_inputs():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    proc = os.path.join(base_dir, "wallet", "data", "processed")

    stats = pd.read_csv(os.path.join(proc, "stats.csv"), index_col=0)
    corr  = pd.read_csv(os.path.join(proc, "correlation_matrix.csv"), index_col=0)

    # Alinhar ordem dos ativos
    corr = corr.loc[stats.index, stats.index]

    # Vetor de retornos (ANUAL) e vol (ANUAL)
    mu  = stats["Retorno_Esperado"].values.astype(float)      # shape (n,)
    vol = stats["Volatilidade"].values.astype(float)          # shape (n,)

    # Sigma anual = D * Corr * D, onde D = diag(vol)
    D = np.diag(vol)
    Sigma = D @ corr.values @ D

    # Simetrizar e estabilizar
    Sigma = 0.5 * (Sigma + Sigma.T)
    Sigma += 1e-8 * np.eye(Sigma.shape[0])

    return stats.index.tolist(), mu, Sigma, base_dir
# Alterar máximo risco permitido conforme perfil
def max_vol_for_profile(profile: str) -> float:
    if profile == "Conservador":
        return 0.05   # 5% a.a. 
    elif profile == "Moderado":
        return 0.10   # 10% a.a.
    else:
        return 0.18   # 18% a.a. (Arrojado)

def optimize_portfolio(profile: str, long_only: bool = True):
    names, mu, Sigma, base_dir = load_inputs()
    n = len(mu)

    w = cp.Variable(n)

    # Objetivo: maximizar retorno esperado anual
    objective = cp.Maximize(mu @ w)

    # Risco (variância anual)
    var = cp.quad_form(w, Sigma)

    constraints = [cp.sum(w) == 1]
    if long_only:
        constraints.append(w >= 0)

    # >>> CORREÇÃO DCP: restringir VARIÂNCIA, não a RAIZ <<<
    max_risk = max_vol_for_profile(profile)
    constraints.append(var <= (max_risk ** 2))

    prob = cp.Problem(objective, constraints)
    # Escolha de solver robusto (SCS é bem tolerante); ECOS também funciona
    prob.solve(solver=cp.SCS, verbose=False)

    if w.value is None:
        # fallback: resolver como média-variância (ret - gamma * var)
        gamma = 10.0
        prob = cp.Problem(cp.Maximize(mu @ w - gamma * var), constraints)
        prob.solve(solver=cp.SCS, verbose=False)

    if w.value is None:
        raise RuntimeError("O problema não pôde ser resolvido. Verifique Sigma/mu e restrições.")

    weights = pd.Series(np.clip(w.value, 0, None), index=names)
    weights = weights / weights.sum()

    outdir = os.path.join(base_dir,"wallet",  "data", "results")
    os.makedirs(outdir, exist_ok=True)
    weights.to_csv(os.path.join(outdir, f"portfolio_{profile}.csv"))

    print(f"Carteira {profile} gerada (máx vol = {max_risk:.2%}).")
    return weights

if __name__ == "__main__":
    for p in ["Conservador", "Moderado", "Arrojado"]:
        optimize_portfolio(p)
