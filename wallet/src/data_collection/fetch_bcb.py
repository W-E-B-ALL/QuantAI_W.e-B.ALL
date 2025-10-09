# src/data_collection/fetch_bcb.py
import requests
import pandas as pd
import os

def fetch_cdi():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados?formato=json&dataInicial=09/10/2015"
    data = pd.DataFrame(requests.get(url).json())
    data['data'] = pd.to_datetime(data['data'], format='%d/%m/%Y')
    data['valor'] = data['valor'].astype(float) / 100
    data = data.set_index('data').resample('M').last()
    
    os.makedirs("data/raw", exist_ok=True)
    data.to_csv("data/raw/cdi.csv")
    print("CDI salvo em data/raw/cdi.csv")
    return data

if __name__ == "__main__":
    fetch_cdi()
