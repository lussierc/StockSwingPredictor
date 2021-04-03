"""Will test the functions of the data cleaner."""

import pytest
import pandas as pd

from src import data_cleaner, scraper

def test_clean_scraped_prediction_data():
    """Tests to ensure dates and prices scraped by the tool are prepped for ML predictions."""

    data = scraper.scrape_stock_historical_data("AAPL", "1mo")

    dates, prices = data_cleaner.clean_scraped_prediction_data(data)

    assert prices is not None
    assert dates[0] == 0
    assert dates[1] == 1
    assert prices is not None
