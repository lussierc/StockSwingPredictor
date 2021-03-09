"""Contains data cleaning functions used throughout the project."""

import numpy as np

def scraped_df_cleaner(df):
    """Cleans data by fixing date column of scraped data."""

    #df = df.reset_index()  # resets the df index so dates are a column
    #print("TYPE", type(df))
    return df

def clean_historical_data(historical_data):
    """Prepares dates and prices for stock price prediction."""

    dates = historical_data['Date'].to_numpy()
    prices = historical_data['Close'].to_numpy()

    dates = np.reshape(dates, (len(dates), 1))  # convert dates to a 1-d vector
    prices = np.reshape(prices, (len(prices), 1))  # convert dates to a 1-d vector

    print(dates)
    print(prices)

    return dates, prices
