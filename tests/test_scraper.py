"""Will test the functions of the scraper."""

import pytest
from src import scraper

def test_basic_scrape_stock_info():
    """Tests to ensure that a dictionary of stock information is scraped."""

    stock = "AAPL"

    info_list = scraper.scrape_stock_info(stock)

    assert info_list is not None

def test_basic_scrape_stock_current_data():
    """Tests to ensure that a dataframe of one-day stock price data is scraped."""

    stock = "DKNG"

    data_dicts = scraper.scrape_stock_info(stock)

    assert data_dicts is not None

def test_basic_scrape_historical_data():
    """Tests to ensure that a dataframe of historical stock price data is scraped."""

    stock = "DDOG"

    data_dicts = scraper.scrape_stock_info(stock)

    assert data_dicts is not None
