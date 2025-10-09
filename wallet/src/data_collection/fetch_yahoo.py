# src/data_collection/fetch_yahoo.py
import yfinance as yf
import pandas as pd
import os
from datetime import datetime

def fetch_yahoo_data(start="2015-01-01", end=None, interval="1mo"):
    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")

    tickers = {
        "Renda Fixa Prefixada": "IRFM11.SA",
        "Renda Fixa IPCA+": "IMAB11.SA",
        "Ações Brasil": "^BVSP",
        "Ações Globais": "^GSPC",
        "Dólar": "BRL=X",
        "Ouro": "GC=F",
        "Bitcoin": "BTC-USD",
    }

    all_data = pd.DataFrame()

    for nome, code in tickers.items():
        print(f"📥 Baixando {nome} ({code}) ...")
        try:
            # usa Close (ajustado automaticamente)
            df = yf.download(code, start=start, end=end, interval=interval, progress=False)
            
            if "Adj Close" in df.columns:
                series = df["Adj Close"]
            elif "Close" in df.columns:
                series = df["Close"]
            else:
                raise KeyError("Nenhuma coluna 'Close' ou 'Adj Close' encontrada.")
            
            series.name = nome
            all_data = pd.concat([all_data, series], axis=1)
        except Exception as e:
            print(f"Falha ao baixar {nome}: {e}")

    all_data = all_data.dropna(how="all")

    os.makedirs("data/raw", exist_ok=True)
    all_data.to_csv("data/raw/prices_raw.csv")

    valid = list(all_data.columns)
    missing = [k for k in tickers.keys() if k not in valid]

    print(f"\nDados válidos encontrados: {valid}")
    print(f"Tickers ausentes: {missing}")
    print("Arquivo salvo em data/raw/prices_raw.csv")

    return all_data

if __name__ == "__main__":
    fetch_yahoo_data()
