"""Will scrape the necessary real-time stock price and extraneous data for the tool."""

# import scraping libraries:
import yfinance as yf

def scrape_yahoo_finance_info(stocks):
    """Gathers real time stock prices and info from Yahoo! Finance."""

    for stock in stocks:
        ticker = yf.Ticker(stock)

        print(ticker.info)


def scrape_yahoo_finance_current(stocks):
    """Scrape 1day price info or last day's price info."""

    for stock in stocks:
        ticker = yf.Ticker(stock)

        # get historical market data
        current = ticker.history(period="1d")
        print(current)

def scrape_yahoo_finance_historical(stocks):
    """Scrape historical stock price data from Yahoo! Finanace."""

    for stock in stocks:
        ticker = yf.Ticker(stock)

        # get historical market data
        hist = ticker.history(period="1y")
        print(hist)
