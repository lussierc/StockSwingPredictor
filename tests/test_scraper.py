"""Will test the functions of the scraper."""

import pytest
from src import scraper

def test_basic_scrape_stock_info():
    """Tests to ensure that a dictionary of stock information is scraped."""

    stocks = ['AAPL', 'DKNG', 'MSFT']

    info_list = scraper.scrape_stock_info(stocks)

    assert info_list is not None
    assert len(info_list) == 3

def test_basic_scrape_stock_current_data():
    """Tests to ensure that a dataframe of one-day stock price data is scraped."""

    stocks = ['AAPL', 'DKNG', 'MSFT', 'DDOG']

    data_list = scraper.scrape_stock_info(stocks)

    assert data_list is not None
    assert len(data_list) == 4

def test_basic_scrape_historical_data():
    """Tests to ensure that a dataframe of historical stock price data is scraped."""

    stocks = ['AAPL', 'DKNG', 'ZM']

    data_list = scraper.scrape_stock_info(stocks)

    assert data_list is not None
    assert len(data_list) != 2
