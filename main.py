import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Fetching S&P 500 tickers from Wikipedia
sp500df = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
tickers = sp500df['Symbol'].to_list()
tickers = [ticker.replace('.', '-') for ticker in tickers]
tickers_subset = tickers[:100]  # Limit to first 100 tickers
data = yf.download(tickers_subset, start='2015-01-01', end='2025-01-01')

def 