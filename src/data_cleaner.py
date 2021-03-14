"""Contains data cleaning functions used throughout the project."""

import numpy as np
import pandas as pd


def reset_df_index(df):
    """Cleans data by fixing date column of scraped data."""

    df = df.reset_index()  # resets the df index so dates are a column
    return df


def clean_historical_data(historical_data):
    """Prepares dates and prices for stock price prediction."""

    dates = historical_data["Date"].to_numpy()
    prices = historical_data["Close"].to_numpy()

    dates = np.reshape(dates, (len(dates), 1))  # convert dates to a 1-d vector
    prices = np.reshape(prices, (len(prices), 1))  # convert dates to a 1-d vector

    return dates, prices


def clean_scraped_prediction_data(df):
    """Cleans a historical or current stock price df."""

    data = df.copy()
    data = reset_df_index(data)

    # for date in data['Date']:
    #     date = str(date.date())
    #     date = date.split('-')[2]
    #
    # data['Date'] = pd.to_numeric(data['Date'])
    # i = 0
    # for date in data:
    #     #date['num_date'] += i
    #     i += 1

    dates_to_list = data.index.tolist()
    dates = np.reshape(
        dates_to_list, (len(dates_to_list), 1)
    )  # convert to 1d dimension

    prices = data["Close"].tolist()

    return dates, prices
