import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Gathering data
stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'META']
data = yf.download(stocks, start='2020-01-01', end='2025-01-01', auto_adjust=True)
data.dropna(inplace=True)
monthly_returns = data.resample('ME').last().pct_change()

# Function for executing strategies
def strategy_results(strategy='momentum', lookback=3, n=2):
    """Takes a strategy, lookback period, and the top/bottom n stocks to use for the strategy and returns the 
    total returns. Defaults to momentum strategy, a lookback period of 3 months, and top/bottom 2 stocks"""
    if strategy not in ['momentum', 'mean_reversion']:
        return 'Strategy must be either "momentum" or "mean_reversion"'
    all_returns = []
    for i in range(lookback, len(monthly_returns)-1):
        past_returns = monthly_returns.iloc[i-lookback:i].sum()
        if strategy == 'momentum':
            picks = past_returns.nlargest(n).index
        elif strategy == 'mean_reversion':
            picks = past_returns.nsmallest(n).index
        next_month_return = monthly_returns.iloc[i+1][picks].mean()
        all_returns.append(next_month_return)
    return pd.Series(all_returns)

momentum_returns = strategy_results('momentum')
mean_reversion_returns = strategy_results('mean_reversion')

def plot_strategy_results(momentum, reversion):
    plt.figure(figsize=(12, 6))
    (1 + momentum).cumprod().plot(label='Momentum')
    (1 + reversion).cumprod().plot(label='Mean Reversion')
    plt.title('Strategy Performance Over Time')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.grid(True)
    plt.show()

plot_strategy_results(momentum_returns, mean_reversion_returns)

def summarize(returns, name):
    total_return = (1 + returns).prod() - 1
    sharpe = returns.mean() / returns.std() * np.sqrt(12)  # Monthly returns
    print(f'{name} Strategy:')
    print(f'  Total Return: {total_return:.2%}')
    print(f'  Sharpe Ratio: {sharpe:.2f}\n')

summarize(momentum_returns, 'Momentum')
summarize(mean_reversion_returns, 'Mean Reversion')