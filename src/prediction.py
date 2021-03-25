"""Creates a model and performs a stock price swing prediction using ML methods."""

import matplotlib.dates as mdates
import data_cleaner
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import Lasso
from sklearn.neighbors import KNeighborsRegressor


def run_predictor(scraped_data):
    """Given scraped data, run the prediction models used by the tool."""

    finalized_data = []

    for stock_data in scraped_data:
        print("* Making predictions for ", stock_data["stock"], " ....")
        historical_data = stock_data["stock_historical_data"]

        df = historical_data[
            ["Close"]
        ]  # get the close price from the historical data (independent variable)

        dates, prices = data_cleaner.clean_scraped_prediction_data(df)

        next_date = len(dates) + 1  # the next day that will be used in the prediction

        (
            next_day_predictions,
            swing_predictions,
            model_scores,
            prev_close,
        ) = ml_predictions(dates, prices, [next_date], stock_data["stock"])

        stock_data["prediction_results"] = data_cleaner.organize_prediction_results(
            stock_data,
            next_day_predictions,
            swing_predictions,
            model_scores,
            prev_close,
        )

        print("prediction_results", stock_data["prediction_results"])
        finalized_data.append(stock_data)  # store prediction results

    return finalized_data


def ml_predictions(dates, prices, next_date, stock_name):
    """Performs SVR training and prediction of stock prices."""

    next_date = np.reshape(next_date, (len(next_date), 1))

    (
        svr_lin,
        svr_poly,
        svr_rbf,
        lr,
        en,
        lasso,
        knr,
    ) = create_ml_models()  # creates and sets up SVR models

    svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr = train_ml_models(
        svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr, dates, prices
    )  # trains SVR models with previous price/date data

    model_scores = test_ml_models(
        dates, prices, svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr
    )

    plot_predictions(
        dates,
        prices,
        svr_rbf,
        svr_lin,
        svr_poly,
        lr,
        en,
        lasso,
        knr,
        next_date,
        stock_name,
    )

    next_day_predictions = make_new_predictions(
        svr_rbf, svr_lin, svr_poly, lr, en, lasso, knr, next_date
    )

    prev_close = prices[-1]
    model_swing_predictions = {}
    for price_prediction in next_day_predictions:
        swing_prediction = predict_indiv_model_swing(
            next_day_predictions[price_prediction], prev_close
        )
        model_swing_predictions[price_prediction] = swing_prediction

    price_swing_prediction = predict_price_swing(model_swing_predictions)

    return next_day_predictions, model_swing_predictions, model_scores, prev_close


def create_ml_models():
    """Creates SVR models."""

    svr_lin = SVR(kernel="linear", C=1e3)
    svr_poly = SVR(kernel="poly", C=1e3, degree=2)
    svr_rbf = SVR(kernel="rbf", C=1e3, gamma=0.05)
    lr = LinearRegression()
    en = ElasticNet()
    lasso = Lasso()
    knr = KNeighborsRegressor()

    return svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr


def train_ml_models(svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr, dates, prices):
    """Trains/fits SVR models."""

    svr_lin.fit(dates, prices)  # Fit regression model
    svr_poly.fit(dates, prices)
    svr_rbf.fit(dates, prices)
    lr.fit(dates, prices)
    en.fit(dates, prices)
    lasso.fit(dates, prices)
    knr.fit(dates, prices)

    return svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr


def test_ml_models(dates, prices, svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr):
    """Test models and determine a confidence score rating of the predictions generated."""

    model_scores = {
        "svr_lin_score": 0.0,
        "svr_poly_score": 0.0,
        "svr_rbf_score": 0.0,
        "lr_score": 0.0,
        "en_score": 0.0,
        "lasso_score": 0.0,
        "knr_score": 0.0,
    }

    # Create a testing model: (the score returns the coefficient of determination R^2 of the prediction (best score is 1.0)):
    model_scores["svr_lin_score"] = svr_lin.score(dates, prices)
    model_scores["svr_poly_score"] = svr_poly.score(dates, prices)
    model_scores["svr_rbf_score"] = svr_rbf.score(dates, prices)
    model_scores["lr_score"] = lr.score(dates, prices)
    model_scores["en_score"] = en.score(dates, prices)
    model_scores["lasso_score"] = lasso.score(dates, prices)
    model_scores["knr_score"] = knr.score(dates, prices)

    return model_scores


def make_new_predictions(
    svr_rbf, svr_lin, svr_poly, lr, en, lasso, knr, next_date
):
    """Makes predictions for the next day's stock price."""

    price_predictions = {
        "svr_lin_price": 0.0,
        "svr_poly_price": 0.0,
        "svr_rbf_price": 0.0,
        "lr_price": 0.0,
        "en_price": 0.0,
        "lasso_price": 0.0,
        "knr_price": 0.0,
    }

    price_predictions["svr_lin_price"] = svr_lin.predict(next_date)[0]
    price_predictions["svr_poly_price"] = svr_poly.predict(next_date)[0]
    price_predictions["svr_rbf_price"] = svr_rbf.predict(next_date)[0]
    price_predictions["lr_price"] = lr.predict(next_date)[0]
    price_predictions["en_price"] = en.predict(next_date)[0]
    price_predictions["lasso_price"] = lasso.predict(next_date)[0]
    price_predictions["knr_price"] = knr.predict(next_date)[0]

    return price_predictions


def plot_predictions(
    dates,
    prices,
    svr_rbf,
    svr_lin,
    svr_poly,
    lr,
    en,
    lasso,
    knr,
    next_date,
    stock_name,
):
    """Plot predictions generated by the tool."""

    # print labels for plot:
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.title("ML Predictions " + stock_name)

    plt.scatter(
        dates, prices, c="k", label="Data"
    )  # print original data points that the model will try to predict
    # plot and run SVR (SVM) predictions:
    plt.plot(
        dates, svr_lin.predict(dates), c="g", label="Linear model"
    )  # predict given dates prices with a linear SVR model
    plt.plot(
        dates, svr_rbf.predict(dates), c="yellow", label="RBF model"
    )  # predict given dates prices with a rbf SVR model
    plt.plot(
        dates, svr_poly.predict(dates), c="blue", label="Polynomial model"
    )  # predict given dates prices with a poly SVR model
    # plot and run other ML predictions:
    plt.plot(
        dates, lr.predict(dates), c="orange", label="LR"
    )  # predict given dates prices with a Linear Regression model
    plt.plot(
        dates, en.predict(dates), c="red", label="EN"
    )  # predict given dates prices with a ElasticNet model
    plt.plot(
        dates, lasso.predict(dates), c="brown", label="Lasso"
    )  # predict given dates prices with a LASSO model
    plt.plot(
        dates, knr.predict(dates), c="blue", label="KNR"
    )  # predict given dates prices with a KNR model

    # predict and plot the next day stock price projection:
    plt.scatter(
        next_date, svr_rbf.predict(next_date)[0], c="y", label="RBF Next Day Prediction"
    )  # print the next day's prediction on the plot
    plt.scatter(
        next_date, knr.predict(next_date)[0], c="teal", label="KNR Next Day Prediction"
    )  # print the next day's prediction on the plot
    plt.scatter(
        next_date,
        lasso.predict(next_date)[0],
        c="brown",
        label="Lasso Next Day Prediction",
    )  # print the next day's prediction on the plot

    # plot extraneous graph details:
    plt.legend()  # define plot legend
    plt.show()  # display the plot


def predict_indiv_model_swing(prediction, prev_close):
    """Performs a price swing prediction for an indvidual model."""

    if prediction > prev_close:
        price_swing = "Up"
    elif prediction < prev_close:
        price_swing = "Down"
    elif prediction == prev_close:
        price_swing = "None"
    else:
        price_swing = "Error"

    return price_swing

def predict_price_swing(next_day_predictions):
    """Performs the final price swing prediction for a stock."""
    print("HERE",next_day_predictions)

    #   Weights:
    #svr_rbf_price 35%
    #knr_price 35%
    #en_price 15%
    #lr_price 15%

    up_score = 0
    down_score = 0

    if next_day_predictions["svr_rbf_price"] == "Up":
        up_score += 2
    else:
        down_score += 2

    if next_day_predictions["knr_price"] == "Up":
        up_score += 2
    else:
        down_score += 2

    if next_day_predictions["en_price"] == "Up":
        up_score += 1
    else:
        down_score += 1

    if next_day_predictions["lr_price"] == "Up":
        up_score += 1
    else:
        down_score += 1

    if up_score >= down_score:
        print("GOES UP")
        if up_score == 6:
            "PERFECT 6"
    elif down_score >= up_score:
        print("GOES Down")
    else:
        print("ERROR")
