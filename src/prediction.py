"""Creates a model and performs a stock price swing prediction using ML methods."""
import matplotlib.dates as mdates
import data_cleaner
from sklearn.svm import SVR
import numpy as np


def run_predictor(scraped_data):
    """Given scraped data, run the prediction models used by the tool."""

    print(scraped_data)

    finalized_data = []

    for stock_data in scraped_data:
        print(stock_data["stock"])

        stock_finalized_data = svr_prediction(stock_data)

        finalized_data.append(stock_finalized_data)


def svr_prediction(stock_data):
    """Uses an SVR to predict stock prices."""

    historical_data = stock_data["stock_historical_data"]

    data_cleaner.clean_historical_data(historical_data)

    return historical_data  # FIX THIS
