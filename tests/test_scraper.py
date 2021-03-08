"""Will test the functions of the scraper."""

import pytest
from src import scraper


def test_basic_scrape_stock_info():
    """Tests to ensure that a dictionary of stock information is scraped."""

    stock = "AAPL"

    info_list = scraper.scrape_stock_info(stock)

    assert info_list is not None


def test_basic_scrape_stock_current_data():
    """Tests to ensure that a dictionary of one-day stock price data is scraped."""

    stock = "DKNG"

    data_dicts = scraper.scrape_stock_info(stock)

    assert data_dicts is not None


def test_basic_scrape_historical_data():
    """Tests to ensure that a dictionary of historical stock price data is scraped."""

    stock = "DDOG"

    data_dicts = scraper.scrape_stock_info(stock)

    assert data_dicts is not None


def test_run_scraper():
    """Tests the run_scraper function to ensure data is scraped properly."""

    stocks = ['AAPL', 'DKNG', 'MSFT', 'DDOG']

    scraped_data = scraper.run_scraper(stocks)

    stock_list_1 = scraped_data[0]
    stock_list_3 = scraped_data[2]

    assert scraped_data is not None
    assert len(scraped_data) == 4
    
    assert stock_list_1[0] == 'AAPL'
    assert stock_list_3[0] == 'MSFT'
