"""Creates a model and performs a stock price swing prediction using ML methods."""

import matplotlib.dates as mdates
import data_cleaner
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split


def run_predictor(scraped_data):
    """Given scraped data, run the prediction models used by the tool."""

    print(scraped_data)

    finalized_data = []

    for stock_data in scraped_data:
        print(stock_data["stock"])

        stock_finalized_data = predict(stock_data)

        finalized_data.append(stock_finalized_data)


def predict(stock_data):
    """Uses an SVR to predict stock prices."""

    historical_data = stock_data["stock_historical_data"]

    df = historical_data[
        ["Close"]
    ]  # get the close price from the historical data (independent variable)

    print(df)

    dates, prices = data_cleaner.clean_scraped_prediction_data(df)
    test = len(dates) + 1
    svr_predict(dates, prices, [test])

def svr_predict(dates, prices, x):
    dates = np.reshape(dates,(len(dates), 1)) # convert to 1xn dimension
    x = np.reshape(x,(len(x), 1))

    svr_lin  = SVR(kernel='linear', C=1e3)
    svr_poly = SVR(kernel='poly', C=1e3, degree=2)
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.05)

    # Fit regression model
    svr_lin .fit(dates, prices)
    svr_poly.fit(dates, prices)
    svr_rbf.fit(dates, prices)

    plt.scatter(dates, prices, c='k', label='Data')
    plt.plot(dates, svr_lin.predict(dates), c='g', label='Linear model')
    plt.plot(dates, svr_rbf.predict(dates), c='r', label='RBF model')
    plt.plot(dates, svr_poly.predict(dates), c='b', label='Polynomial model')

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Support Vector Regression')
    plt.legend()
    plt.show()

    print("x", x)
    print(prices[-1])
    print("PREDICTIONS  :", svr_rbf.predict(x)[0], svr_lin.predict(x)[0], svr_poly.predict(x)[0])

    return svr_rbf.predict(x)[0], svr_lin.predict(x)[0], svr_poly.predict(x)[0]
