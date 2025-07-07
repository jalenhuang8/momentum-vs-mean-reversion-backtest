import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Gathering data
stocks = ["AAPL", "MSFT", "AMZN", "GOOG", "META"]
data = yf.download(stocks,start="2020-01-01",end="2025-01-01")["Close"]
data.dropna(inplace=True)
print(data.head())

def monthly_returns(prices):
    return prices.resample("ME").last().pct_change()
strategy_returns = monthly_returns(data)
print(strategy_returns.head())

# Function for executing strategies
def strategy_results(prices, strategy, top_n=2):
    strategy_returns = monthly_returns(data)
    monthly_results = []
    for i in range(3, len(strategy_returns)-1):
        past_returns = strategy_returns.iloc[i-3:i].sum()
        if strategy == "momentum":
            picks = past_returns.nlargest(top_n).index
        elif strategy == "mean_reversion":
            picks = past_returns.nsmallest(top_n).index
        else:
            return "Strategy must be 'momentum' or 'mean_reversion'"
        next_month_return = strategy_returns.iloc[i+1][picks].mean()
        monthly_results.append(next_month_return)
    return pd.Series(monthly_results)

momentum_returns = strategy_results(data, "momentum")
mean_reversion_returns = strategy_results(data, "mean_reversion")

def plot_strategy_results(momentum, reversion):
    plt.figure(figsize=(12, 6))
    (1 + momentum).cumprod().plot(label="Momentum")
    (1 + reversion).cumprod().plot(label="Mean Reversion")
    plt.title("Strategy Performance Over Time")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.grid(True)
    plt.show()

plot_strategy_results(momentum_returns, mean_reversion_returns)

def summarize(returns, name):
    total_return = (1 + returns).prod() - 1
    sharpe = returns.mean() / returns.std() * np.sqrt(12)  # Monthly returns
    print(f"{name} Strategy:")
    print(f"  Total Return: {total_return:.2%}")
    print(f"  Sharpe Ratio: {sharpe:.2f}\n")

summarize(momentum_returns, "Momentum")
summarize(mean_reversion_returns, "Mean Reversion")