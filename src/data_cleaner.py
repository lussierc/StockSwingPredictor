"""Contains data cleaning functions used throughout the project."""

def scraped_df_cleaner(df):
    """Cleans data by fixing date column of scraped data."""

    df = df.reset_index()  # resets the df index so dates are a column
    print("TYPE", type(df))
    return df
