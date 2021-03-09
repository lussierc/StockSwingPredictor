"""Will scrape the necessary real-time stock price and extraneous data for the tool."""

# import scraping library:
import yfinance as yf
import data_cleaner

def run_scraper(stocks):
    """Runs the scraper and stores the scraped data."""

    scraped_data = []  # this list will hold the dictionaries of scraped stock data

    for stock in stocks:
        stock_data = {'stock': '', 'stock_info': {}, 'stock_current_data': '', 'stock_historical_data': ''}  # define dict to store individual stock's data
        stock_data['stock'] = stock
        stock_data['stock_info'] = scrape_stock_info(stock)
        stock_data['stock_current_data'] = scrape_stock_current_data(stock)
        stock_data['stock_historical_data'] = scrape_stock_historical_data(stock)
        scraped_data.append(stock_data)

    return scraped_data


def scrape_stock_info(stock):
    """Gathers real time stock info from Yahoo! Finance."""

    ticker = yf.Ticker(stock)

    return ticker.info


def scrape_stock_current_data(stock):
    """Scrape 1day price info or last day's price info. Real-time price info"""

    ticker = yf.Ticker(stock)

    current = ticker.history(period="1d")  # get current market data

    current_dict = data_cleaner.scraped_df_cleaner(current)

    return current_dict


def scrape_stock_historical_data(stock):
    """Scrape historical stock price data from Yahoo! Finance."""

    ticker = yf.Ticker(stock)

    hist = ticker.history(period="1y")  # get historical market data

    hist_dict = data_cleaner.scraped_df_cleaner(hist)

    return hist_dict
