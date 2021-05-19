"""Creates a model and performs a stock price swing prediction using ML methods."""

import data_cleaner

from datetime import date
from timeit import default_timer as timer
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import Lasso
from sklearn.neighbors import KNeighborsRegressor


def run_predictor(scraped_data, period):
    """Given scraped data, run the prediction models used by the tool."""

    finalized_data = []

    for stock_data in scraped_data:
        print("\n* Making predictions for", stock_data["stock"], "....")

        historical_data = stock_data["stock_historical_data"]

        df = historical_data[
            ["Close"]
        ]  # get the close price from the historical data (independent variable)

        dates, prices = data_cleaner.clean_scraped_prediction_data(df)

        next_date = len(dates)  # the next day that will be used in the prediction

        (
            next_day_predictions,
            prev_predictions,
            swing_predictions,
            model_scores,
            prev_close,
            figure,
            plot_dates,
            training_times,
            testing_times,
            new_predictions_times,
            prev_predictions_times,
        ) = ml_predictions(dates, prices, [next_date], stock_data["stock"], period)

        stock_data["prediction_results"] = data_cleaner.organize_prediction_results(
            stock_data["stock"],
            next_day_predictions,
            swing_predictions,
            model_scores,
            prev_close,
            period,
            date.today(),
            figure,
            training_times,
            testing_times,
            new_predictions_times,
            prev_predictions_times,
        )

        stock_data["plot_dates"] = plot_dates
        stock_data["prev_predictions"] = prev_predictions

        finalized_data.append(stock_data)  # store prediction results

    return finalized_data


def ml_predictions(dates, prices, next_date, stock_name, period):
    """Performs SVR training and prediction of stock prices."""

    next_date = np.reshape(next_date, (len(next_date), 1))

    models = create_ml_models()  # creates and sets up SVR models

    trained_models, training_times = train_ml_models(
        models, dates, prices
    )  # trains SVR models with previous price/date data

    model_scores, testing_times = test_ml_models(
        dates, prices, trained_models
    )

    next_day_predictions, new_predictions_times = make_new_predictions(
        trained_models, next_date
    )

    prev_predictions, prev_predictions_times = make_prev_predictions(
        dates, prices, trained_models
    )

    figure, plot_dates = plot_predictions(
        dates,
        prices,
        next_day_predictions,
        prev_predictions,
        next_date,
        stock_name,
        period,
    )

    prev_close = prices[-1]
    model_swing_predictions = {}
    for price_prediction in next_day_predictions:
        swing_prediction = predict_indiv_model_swing(
            next_day_predictions[price_prediction], prev_close
        )
        model_swing_predictions[price_prediction] = swing_prediction

    return (
        next_day_predictions,
        prev_predictions,
        model_swing_predictions,
        model_scores,
        prev_close,
        figure,
        plot_dates,
        training_times,
        testing_times,
        new_predictions_times,
        prev_predictions_times,
    )


def create_ml_models():
    """Creates SVR models."""

    svr_lin = SVR(kernel="linear", C=1e3)
    svr_poly = SVR(kernel="poly", C=1e3, degree=2)
    svr_rbf = SVR(kernel="rbf", C=1e3, degree=3, gamma="scale")
    lr = LinearRegression()
    en = ElasticNet()
    lasso = Lasso()
    knr = KNeighborsRegressor()

    models = {'svr_lin': svr_lin, 'svr_poly': svr_poly, 'svr_rbf': svr_rbf, 'lr': lr, 'en': en, 'lasso': lasso, 'knr': knr}

    return models

def train_ml_models(models, dates, prices):
    """Trains/fits SVR models."""

    trained_models = {}
    training_times = {}

    for key in models.keys():
        start = timer()
        trained_models[key] = models[key].fit(dates, prices)
        end = timer()

        time_elapsed = end - start
        training_times[key] = time_elapsed

    return trained_models, training_times


def test_ml_models(dates, prices, trained_models):
    """Test models and determine a confidence score rating of the predictions generated."""

    model_scores = {
        "svr_lin": 0.0,
        "svr_poly": 0.0,
        "svr_rbf": 0.0,
        "lr": 0.0,
        "en": 0.0,
        "lasso": 0.0,
        "knr": 0.0,
    }
    testing_times = {}

    for key in trained_models.keys():
        start = timer()
        model_scores[key] = trained_models[key].score(dates, prices)
        end = timer()

        time_elapsed = end - start
        testing_times[key] = time_elapsed

    return model_scores, testing_times


def make_new_predictions(trained_models, next_date):
    """Makes predictions for the next day's stock price."""

    price_predictions = {
        "svr_lin": 0.0,
        "svr_poly": 0.0,
        "svr_rbf": 0.0,
        "lr": 0.0,
        "en": 0.0,
        "lasso": 0.0,
        "knr": 0.0,
    }
    new_predictions_times = {}


    for key in trained_models.keys():
        start = timer()
        price_predictions[key] = trained_models[key].predict(next_date)[0]
        end = timer()

        time_elapsed = end - start
        new_predictions_times[key] = time_elapsed


    return price_predictions, new_predictions_times


def make_prev_predictions(
    dates, prices, trained_models
):
    """Makes predictions on previous days of data, which the models were trained on."""

    prev_price_predictions = {
        "svr_lin": [],
        "svr_poly": [],
        "svr_rbf": [],
        "lr": [],
        "en": [],
        "lasso": [],
        "knr": [],
        "prices": prices,
    }
    prev_predictions_times = {}

    for key in trained_models.keys():
        start = timer()
        prev_price_predictions[key] = list(trained_models[key].predict(dates))
        end = timer()

        time_elapsed = end - start
        prev_predictions_times[key] = time_elapsed

    return prev_price_predictions, prev_predictions_times


def plot_predictions(
    dates,
    prices,
    next_day_predictions,
    prev_predictions,
    next_date,
    stock_name,
    period,
):
    """Plot predictions generated by the tool."""

    plot_dates = (
        []
    )  # will hold dates specifically for plotting, not to be used in prediction
    for today in dates:
        plot_dates.append(today[0])

    fig = go.Figure()  # create Plotly graph figure
    # types of traces: markers, lines+markers, lines

    fig.add_trace(
        go.Scatter(
            x=plot_dates,
            y=prices,
            mode="lines+markers",
            name="Original Data",
            marker_color="rgba(0, 0, 0, 1)",
        )
    )  # plot original data

    # plot historical predictions:
    fig.add_trace(
        go.Scatter(
            x=plot_dates,
            y=prev_predictions["svr_rbf"],
            name="SVR-RBF",
            marker_color="rgba(248, 42, 42, 1)",
        )
    )  # display SVR RBF historical prediction

    fig.add_trace(
        go.Scatter(
            x=plot_dates,
            y=prev_predictions["svr_lin"],
            name="SVR-LIN",
            marker_color="rgba(42, 248, 248, 1)",
        )
    )  # display SVR LIN historical prediction
    fig.add_trace(
        go.Scatter(
            x=plot_dates,
            y=prev_predictions["svr_poly"],
            name="SVR-POLY",
            marker_color="rgba(42, 248, 145, 1)",
        )
    )  # display SVR POLY historical prediction
    fig.add_trace(
        go.Scatter(
            x=plot_dates,
            y=prev_predictions["lr"],
            name="LR",
            marker_color="rgba(230, 145, 59, 1)",
        )
    )  # display LR historical prediction
    fig.add_trace(
        go.Scatter(
            x=plot_dates,
            y=prev_predictions["en"],
            name="EN",
            marker_color="rgba(145, 59, 230, 1)",
        )
    )  # display EN historical prediction
    fig.add_trace(
        go.Scatter(
            x=plot_dates,
            y=prev_predictions["lasso"],
            name="LASSO",
            marker_color="rgba(230, 59, 230, 1)",
        )
    )  # display LASSO historical prediction
    fig.add_trace(
        go.Scatter(
            x=plot_dates,
            y=prev_predictions["knr"],
            name="KNR",
            marker_color="rgba(244, 212, 0, 1)",
        )
    )  # display KNR historical prediction

    # plot new predictions:
    temp_plotter_list = []
    temp_plotter_list.append(next_day_predictions["svr_rbf"])
    fig.add_trace(
        go.Scatter(
            x=next_date[0],
            y=temp_plotter_list,
            mode="markers",
            name="SVR-RBF Prediction",
            marker_color="rgba(248, 42, 42, 1)",
        )
    )  # display SVR RBF next day prediction
    temp_plotter_list = []
    temp_plotter_list.append(next_day_predictions["svr_poly"])
    fig.add_trace(
        go.Scatter(
            x=plot_dates,
            y=temp_plotter_list,
            name="SVR-POLY",
            marker_color="rgba(42, 248, 145, 1)",
        )
    )  # display SVR POLY next day prediction
    temp_plotter_list = []
    temp_plotter_list.append(next_day_predictions["knr"])
    fig.add_trace(
        go.Scatter(
            x=next_date[0],
            y=temp_plotter_list,
            mode="markers",
            name="KNR Prediction",
            marker_color="rgba(244, 212, 0, 1)",
        )
    )  # display KNR next day prediction
    temp_plotter_list = []
    temp_plotter_list.append(next_day_predictions["en"])
    fig.add_trace(
        go.Scatter(
            x=next_date[0],
            y=temp_plotter_list,
            mode="markers",
            name="EN Prediction",
            marker_color="rgba(145, 59, 230, 1)",
        )
    )  # display EN next day prediction
    temp_plotter_list = []
    temp_plotter_list.append(next_day_predictions["lr"])
    fig.add_trace(
        go.Scatter(
            x=next_date[0],
            y=temp_plotter_list,
            mode="markers",
            name="LR Prediction",
            marker_color="rgba(230, 145, 59, 1)",
        )
    )  # display LR next day prediction

    make_title = (
        "ML Predictions "
        + stock_name
        + " for "
        + str(date.today())
        + " (Data Period: "
        + period
        + ")"
    )
    fig.update_layout(
        title=make_title,
        xaxis_title="Days",
        yaxis_title="Price ($)",
        legend_title="Model Legend",
    )

    return fig, plot_dates


def predict_indiv_model_swing(prediction, prev_close):
    """Performs a price swing prediction for an indvidual model."""

    if prediction > prev_close:
        price_swing = "Up"
    elif prediction < prev_close:
        price_swing = "Down"
    else:
        price_swing = "No Movement"

    return price_swing
