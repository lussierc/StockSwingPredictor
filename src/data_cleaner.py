"""Contains data cleaning functions used throughout the project."""

import numpy as np
import pandas as pd


def reset_df_index(df):
    """Cleans data by fixing date column of scraped data."""

    df = df.reset_index()  # resets the df index so dates are a column
    return df


def clean_scraped_prediction_data(df):
    """Cleans a historical or current stock price df."""

    data = df.copy()
    data = reset_df_index(data)

    ### POTENTIAL TODO: FIX WAY DATES ARE CLEANED SO ACTUAL DATE INSTEAD OF INTEGER REP OF DATE IS USED

    dates_to_list = (
        data.index.tolist()
    )  # gets the number of dates, not actual date (0, 1, 2, etc.)
    dates = np.reshape(
        dates_to_list, (len(dates_to_list), 1)
    )  # convert to 1d dimension

    prices = data["Close"].tolist()

    return dates, prices


def organize_prediction_results(
    stock_data,
    next_day_predictions,
    swing_predictions,
    model_scores,
    prev_close,
    price_swing_prediction,
    period,
    date,
    figure,
):
    """Store results from stock prediction."""

    prediction_results = {
        "swing_predictions": {},
        "next_day_predictions": {},
        "prev_close": 0,
        "model_scores": {},
        "price_swing_prediction": "",
        "svr_knr_price_avg": 0,
        "multi_fold_price_avg": 0,
        "data_time_period": period,
        "date": str(date),
        "figure": "",
    }

    prediction_results["swing_predictions"] = swing_predictions
    prediction_results["next_day_predictions"] = next_day_predictions
    prediction_results["prev_close"] = prev_close
    prediction_results["model_scores"] = model_scores
    prediction_results["price_swing_prediction"] = price_swing_prediction

    prediction_results["svr_knr_price_avg"] = (
        next_day_predictions["knr"] + next_day_predictions["svr_rbf"]
    ) / 2  # calc & save avg price prediction for SVR-RBF and KNR

    prediction_results["multi_fold_price_avg"] = (
        next_day_predictions["knr"]
        + next_day_predictions["svr_rbf"]
        + next_day_predictions["en"]
        + next_day_predictions["lr"]
    ) / 4  # calc & save avg price prediction for 4 main prediction models

    prediction_results["figure"] = figure

    return prediction_results
