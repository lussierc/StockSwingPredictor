"""Will scrape the necessary real-time stock price and extraneous data for the tool."""

# import scraping libraries:
import yfinance as yf


def run_scraper(stocks):
    """Runs the scraper and stores the scraped data."""

    scraped_data = []

    for stock in stocks:
        stock_data = {'stock': '', 'stock_info': {}, 'stock_current_data': '', 'stock_historical_data': ''}
        stock_data['stock'] = stock
        stock_data['stock_info'] = scrape_stock_info(stock)
        stock_data['stock_current_data'] = scrape_stock_current_data(stock)
        stock_data['stock_historical_data'] = scrape_stock_historical_data(stock)
        scraped_data.append(stock_data)
    print(scraped_data)

    return scraped_data


def scrape_stock_info(stock):
    """Gathers real time stock info from Yahoo! Finance."""

    ticker = yf.Ticker(stock)

    return ticker.info


def scrape_stock_current_data(stock):
    """Scrape 1day price info or last day's price info. Real-time price info"""

    ticker = yf.Ticker(stock)

    # get historical market data
    current = ticker.history(period="1d")

    current_dict = data_cleaner(current)

    return current_dict


def scrape_stock_historical_data(stock):
    """Scrape historical stock price data from Yahoo! Finance."""

    ticker = yf.Ticker(stock)

    # get historical market data
    hist = ticker.history(period="1y")

    hist_dict = data_cleaner(hist)

    return hist_dict


def data_cleaner(df):
    """Cleans data by fixing date column of scraped data."""

    df = df.reset_index()

    return df
