from src.data_collection.fetch_yahoo import fetch_yahoo_data
from src.preprocessing.returns_calc import compute_returns
from src.optimization.markowitz_optimizer import optimize_portfolio
from src.allocation.portfolio_profiles import get_profile_constraints
from src.visualization.reports import generate_report

def main():

    data = fetch_yahoo_data(start="2015-01-01")
    
    returns, stats = compute_returns(data)
    
    for perfil in ["Conservador", "Moderado", "Arrojado"]:
        constraints = get_profile_constraints(perfil)
        carteira = optimize_portfolio(returns, stats, constraints)
        generate_report(carteira, perfil)
    
    print("Carteiras geradas ")

if __name__ == "__main__":
    main()
