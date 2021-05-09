"""Contains data cleaning functions used throughout the project."""

import numpy as np
import pandas as pd

def clean_scraped_prediction_data(df):
    """Cleans a historical or current stock price df."""

    data = df.copy()
    data = df.reset_index()

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
    stock_name,
    next_day_predictions,
    swing_predictions,
    model_scores,
    prev_close,
    period,
    date,
    figure,
):
    """Store results from stock prediction."""

    prediction_results = {
        "stock_name": stock_name,
        "current_prev_close": prev_close,
        "date": str(date),
        "training_data_time_period": period,
        "swing_predictions": swing_predictions,
        "next_day_predictions": next_day_predictions,
        "model_scores": model_scores,
        "figure": figure,
    }

    return prediction_results
