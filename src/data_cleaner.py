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

    print(dates)
    print(prices)

    return dates, prices

def clean_full_dates(date):
    """Converts a timestamp object to a date."""

    date = date.date()

    return str(date)

def clean_scraped_prediction_data(df):
    """Cleans a historical or current stock price df."""

    data = df.copy()
    data = reset_df_index(data)

    # for date in data['Date']:
    #     date = clean_full_dates(date)
    #     date = date.split('-')[2]
    #
    # data['Date'] = pd.to_numeric(data['Date'])
    # i = 0
    # for date in data:
    #     #date['num_date'] += i
    #     i += 1

    return [ data.index.tolist(), data['Close'].tolist() ]
