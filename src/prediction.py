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
        historical_data = stock_data["stock_historical_data"]

        df = historical_data[
            ["Close"]
        ]  # get the close price from the historical data (independent variable)

        dates, prices = data_cleaner.clean_scraped_prediction_data(df)

        next_date = len(dates) + 1

        price_prediction, prev_close = svr_predict(dates, prices, [next_date])

        swing_prediction = predict_price_swing(price_prediction, prev_close)

        stock_data["prediction_results"] = store_prediction_results(
            stock_data, price_prediction, prev_close, swing_prediction
        )

        finalized_data.append(stock_data)  # store prediction results

    return finalized_data


def svr_predict(dates, prices, next_date):
    """Performs SVR training and prediction of stock prices."""

    next_date = np.reshape(next_date, (len(next_date), 1))

    svr_lin, svr_poly, svr_rbf = create_svr_models()  # creates and sets up SVR models
    svr_lin, svr_poly, svr_rbf = train_svr_models(
        svr_lin, svr_poly, svr_rbf, dates, prices
    )  # trains SVR models with previous price/date data

    plt.scatter(
        dates, prices, c="k", label="Data"
    )  # print original data points that the model will try to predict
    plt.plot(
        dates, svr_lin.predict(dates), c="g", label="Linear model"
    )  # predict given dates prices with a linear SVR model
    plt.plot(
        dates, svr_rbf.predict(dates), c="r", label="RBF model"
    )  # predict given dates prices with a rbf SVR model
    plt.plot(
        dates, svr_poly.predict(dates), c="b", label="Polynomial model"
    )  # predict given dates prices with a poly SVR model

    # print labels for plot:
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Support Vector Regression")

    print(
        " - Current/today's closing price: ",
        prices[-1],
        "\n - Date in sequence being predicted (tomorrow):",
        next_date,
    )
    print(
        " - Tomorrow's Predictions:",
        svr_rbf.predict(next_date)[0],
        svr_lin.predict(next_date)[0],
        svr_poly.predict(next_date)[0],
    )

    plt.scatter(
        next_date, svr_rbf.predict(next_date)[0], c="y", label="Next Day Prediction"
    )  # print the next day's prediction on the plot

    plt.legend()  # define plot legend
    plt.show()  # display the plot

    return svr_rbf.predict(next_date)[0], prices[-1]


def create_svr_models():
    """Creates SVR models."""

    svr_lin = SVR(kernel="linear", C=1e3)
    svr_poly = SVR(kernel="poly", C=1e3, degree=2)
    svr_rbf = SVR(kernel="rbf", C=1e3, gamma=0.05)

    return svr_lin, svr_poly, svr_rbf


def train_svr_models(svr_lin, svr_poly, svr_rbf, dates, prices):
    """Trains/fits SVR models."""

    svr_lin.fit(dates, prices)  # Fit regression model
    svr_poly.fit(dates, prices)
    svr_rbf.fit(dates, prices)

    return svr_lin, svr_poly, svr_rbf


def predict_price_swing(prediction, prev_close):
    """Performs the program's price swing prediction."""

    if prediction > prev_close:
        price_swing = "Up"
    elif prediction < prev_close:
        price_swing = "Down"
    elif prediction == prev_close:
        price_swing = "None"
    else:
        price_swing = "Error"

    return price_swing


def store_prediction_results(
    stock_data, price_prediction, prev_close, swing_prediction
):
    """Store results from stock prediction."""

    prediction_results = {
        "swing_prediction": "",
        "price_prediction": 0,
        "prev_close": 0,
    }

    prediction_results["swing_prediction"] = swing_prediction
    prediction_results["price_prediction"] = price_prediction
    prediction_results["prev_close"] = prev_close

    return prediction_results
