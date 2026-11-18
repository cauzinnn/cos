import json
import yfinance as yf
import pandas as pd
import numpy as np

# Load assets
with open('carteira_extraida.json', 'r', encoding='utf-8') as f:
    assets = json.load(f)

print(f"Loaded {len(assets)} assets from carteira_extraida.json")

# Map tickers to yfinance tickers
# IBIT39 is recent BDR on B3, we use QBTC11.SA (Bitcoin ETF on B3) as direct proxy
ticker_map = {}
for a in assets:
    t = a['ticker']
    if t == 'IBIT39':
        ticker_map[t] = 'QBTC11.SA'
    else:
        ticker_map[t] = f"{t}.SA"

all_sa_tickers = list(set(ticker_map.values()))
print(f"Fetching {len(all_sa_tickers)} unique series from Yahoo Finance...")

data = yf.download(all_sa_tickers, period="1y", interval="1d", auto_adjust=True)
close = data['Close']

# Reconstruct DataFrame matching original tickers
df_prices = pd.DataFrame(index=close.index)
for a in assets:
    t = a['ticker']
    sa_t = ticker_map[t]
    df_prices[t] = close[sa_t]

# Forward fill and backward fill any small market holidays/gaps
df_prices = df_prices.ffill().bfill()
print(f"Prices matrix shape: {df_prices.shape}")
print(f"Missing values remaining: {df_prices.isna().sum().sum()}")

# Calculate daily simple returns
df_returns = df_prices.pct_change().dropna()
print(f"Daily returns shape: {df_returns.shape}")

# Annualized mean returns and covariance matrix (252 trading days)
mean_returns = df_returns.mean() * 252
cov_matrix = df_returns.cov() * 252

# Save to disk as clean CSVs and JSON for the notebook
df_prices.to_csv('precos_historicos.csv')
df_returns.to_csv('retornos_diarios.csv')
mean_returns.to_csv('retornos_esperados.csv')
cov_matrix.to_csv('matriz_covariancia.csv')

# Also compute initial weights vector w0
total_val = sum(a['value'] for a in assets)
w0_series = pd.Series({a['ticker']: a['value'] / total_val for a in assets})
w0_series.to_csv('pesos_iniciais.csv')

print("All financial data successfully processed and saved:")
print(f"- precos_historicos.csv")
print(f"- retornos_diarios.csv")
print(f"- retornos_esperados.csv")
print(f"- matriz_covariancia.csv")
print(f"- pesos_iniciais.csv")
