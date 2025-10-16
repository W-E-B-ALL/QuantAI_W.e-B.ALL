import pandas as pd

prices = pd.read_csv("wallet/data/raw/prices_raw.csv", index_col=0)
returns = prices.pct_change().fillna(0)
cumulative_returns = (1 + returns).prod()

print(cumulative_returns.sort_values(ascending=False))
