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

        stock_finalized_data = svr_prediction(stock_data)

        finalized_data.append(stock_finalized_data)


def svr_prediction(stock_data):
    """Uses an SVR to predict stock prices."""

    historical_data = stock_data["stock_historical_data"]

    df = historical_data[
        ["Close"]
    ]  # get the close price from the historical data (independent variable)

    dates, prices = data_cleaner.clean_scraped_prediction_data(df)

    forecast_out = 3  # how many days out in the future do we want to predict?

    # create another column to store the target/dependent variable (shifted days_out up):
    df["Prediction"] = historical_data[["Close"]].shift(-forecast_out)
    print(df)

    # create the independent data set (x):
    x = np.array(
        df.drop(["Prediction"], 1)
    )  # convert the df to a numpy array, drop the prediction array since this is the independent variable dataset (only use close)
    x = x[
        :-forecast_out
    ]  # remove the last 'days_out' rows, get all rows except for the forecasted ones
    print("X")
    print(x)

    # create the dependent data set (y):
    y = np.array(
        df["Prediction"]
    )  # convert the df to a numpy array with all of the values, including the NaNs
    y = y[
        :-forecast_out
    ]  # get all of the y values in the target column except for the last 'days_out'
    print("Y")
    print(y)

    # split the data into 80% training & 20% testing:
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    ########################
    # create and train the SVM (SVR):
    svr = SVR(
        kernel="rbf", C=1e3, gamma=0.1
    )  # creates an SVR using a radio basis kernel
    svr.fit(x_train, y_train)  # train the model using our training data

    # Create a testing model: (the score returns the coefficient of determination R^2 of the prediction (best score is 1.0)):
    svm_confidence = svr.score(x_test, y_test)
    print("SVM Confidence = ", svm_confidence)
    ########################
    # create and train the linear regression model:
    lr = LinearRegression()
    lr.fit(x_train, y_train)  # train the LR model
    # testing model:
    lr_confidence = lr.score(x_test, y_test)
    print("LR Confidence = ", lr_confidence)
    ########################

    # set x_forecast equal to last 30 rows of the original data set from the close column
    x_forecast = np.array(df.drop(["Prediction"], 1))[-forecast_out:]

    print("Today's Close Price = ", df["Close"][-forecast_out])
    print("Tomorrow's Predictions:")
    # print the predictions for the number of forecasted days:
    svr_prediction = svr.predict(x_forecast)
    print("  - SVR Prediction = ", svr_prediction)

    lr_prediction = lr.predict(x_forecast)
    print(x_forecast)
    print("  - LR Prediction = ", lr_prediction)

    if df["Close"][-forecast_out] >= svr_prediction:
        print("DOWN SWING")
    elif df["Close"][-forecast_out] <= svr_prediction:
        print("UP SWING")
    else:
        print("ERROR")
