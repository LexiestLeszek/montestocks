import yfinance as yf
import pandas as pd
import numpy as np

def monte_carlo_simulation(ticker, days=30, num_simulations=1000):
    # Fetch historical data
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    close_prices = hist['Close'].values

    # Calculate log returns
    log_returns = np.log(close_prices[1:] / close_prices[:-1])

    # Monte Carlo simulation
    future_returns = np.random.normal(loc=log_returns.mean(), scale=log_returns.std(), size=(days, num_simulations))
    price_path = np.zeros_like(future_returns)
    price_path[0] = close_prices[-1]

    for t in range(1, days):
        price_path[t] = price_path[t-1] * np.exp(future_returns[t])

    # Calculate the range of possible prices
    min_price = np.min(price_path)
    max_price = np.max(price_path)
    mean_price = np.mean(price_path)
    median_price = np.median(price_path)

    # Return the price prediction
    return {
        "min_price": min_price,
        "max_price": max_price,
        "mean_price": mean_price,
        "median_price": median_price
    }

ticker = "AMR"
days = 30 # Predict for the next 30 days
num_simulations = 1000 # Number of simulations to run

prediction = monte_carlo_simulation(ticker, days, num_simulations)
print(prediction)
