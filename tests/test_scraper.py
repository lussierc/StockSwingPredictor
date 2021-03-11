"""Will test the functions of the scraper."""

import pytest
from src import scraper


def test_basic_scrape_stock_info():
    """Tests to ensure that a dictionary of stock information is scraped."""

    stock = "AAPL"

    info = scraper.scrape_stock_info(stock)

    assert info is not None


def test_scrape_stock_specific_info():
    """Tests to ensure that specific stock info is properly scraped."""

    stock = "MSFT"

    info = scraper.scrape_stock_info(stock)

    assert info is not None
    assert info["sector"] == "Technology"
    assert info["country"] == "United States"
    assert info["city"] == "Redmond"


def test_basic_scrape_stock_current_data():
    """Tests to ensure that a dictionary of one-day stock price data is scraped."""

    stock = "DKNG"

    data = scraper.scrape_stock_current_data(stock)

    assert data is not None


def test_basic_scrape_historical_data():
    """Tests to ensure that a dictionary of historical stock price data is scraped."""

    stock = "DDOG"

    data = scraper.scrape_stock_historical_data(stock)

    assert data is not None


def test_run_scraper():
    """Tests the run_scraper function to ensure data is scraped properly."""

    stocks = ["AAPL", "DKNG", "MSFT", "DDOG"]

    scraped_data = scraper.perform_scraping(stocks)

    stock_list_1 = scraped_data[0]
    stock_list_3 = scraped_data[2]

    assert scraped_data is not None
    assert len(scraped_data) == 4

    assert stock_list_1["stock"] == "AAPL"
    assert stock_list_3["stock"] == "MSFT"
