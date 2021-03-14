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

    finalized_data = []

    for stock_data in scraped_data:
        print(stock_data["stock"])

        historical_data = stock_data["stock_historical_data"]

        df = historical_data[
            ["Close"]
        ]  # get the close price from the historical data (independent variable)

        dates, prices = data_cleaner.clean_scraped_prediction_data(df)

        next_date = len(dates) + 1

        svr_predict(dates, prices, [next_date])

        # finalized_data.append(stock_finalized_data) # TODO: FINALIZE STORAGE OF DATA WITH PREDICTIONS
    # return finalized_data

def svr_predict(dates, prices, x):
    """Performs SVR training and prediction of stock prices."""

    dates = np.reshape(dates,(len(dates), 1)) # convert to 1xn dimension
    x = np.reshape(x,(len(x), 1))

    svr_lin, svr_poly, svr_rbf = create_svr_models()
    svr_lin, svr_poly, svr_rbf = train_svr_models(svr_lin, svr_poly, svr_rbf, dates, prices)

    plt.scatter(dates, prices, c='k', label='Data')
    plt.plot(dates, svr_lin.predict(dates), c='g', label='Linear model')
    plt.plot(dates, svr_rbf.predict(dates), c='r', label='RBF model')
    plt.plot(dates, svr_poly.predict(dates), c='b', label='Polynomial model')

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Support Vector Regression')


    print("x", x)
    print(prices[-1])
    print("PREDICTIONS  :", svr_rbf.predict(x)[0], svr_lin.predict(x)[0], svr_poly.predict(x)[0])
    plt.scatter(x, svr_rbf.predict(x)[0], c='y', label='Next Day Prediction')

    plt.legend()
    plt.show()

    return svr_rbf.predict(x)[0], svr_lin.predict(x)[0], svr_poly.predict(x)[0]

def create_svr_models():
    """Creates SVR models."""

    svr_lin  = SVR(kernel='linear', C=1e3)
    svr_poly = SVR(kernel='poly', C=1e3, degree=2)
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.05)

    return svr_lin, svr_poly, svr_rbf

def train_svr_models(svr_lin, svr_poly, svr_rbf, dates, prices):
    """Trains/fits SVR models."""

    svr_lin.fit(dates, prices)     # Fit regression model
    svr_poly.fit(dates, prices)
    svr_rbf.fit(dates, prices)

    return svr_lin, svr_poly, svr_rbf
