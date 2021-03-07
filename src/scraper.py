"""Will scrape the necessary real-time stock price and extraneous data for the tool."""

# import scraping libraries:
import yfinance as yf


def scrape_stock_info(stocks):
    """Gathers real time stock prices and info from Yahoo! Finance."""

    info_list = []

    for stock in stocks:
        ticker = yf.Ticker(stock)

        info_list.append(ticker.info)

    return info_list


def scrape_stock_current_data(stocks):
    """Scrape 1day price info or last day's price info."""

    current_data = []

    for stock in stocks:
        ticker = yf.Ticker(stock)

        # get historical market data
        current = ticker.history(period="1d")

        current_data.append(current)

    return current_data



def scrape_historical_data(stocks):
    """Scrape historical stock price data from Yahoo! Finanace."""

    historical_data = []

    for stock in stocks:
        ticker = yf.Ticker(stock)

        # get historical market data
        hist = ticker.history(period="1y")

        historical_data.append(hist)

    return historical_data
