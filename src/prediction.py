"""Creates a model and performs a stock price swing prediction using ML methods."""
import matplotlib.dates as mdates

def run_predictor(scraped_data):
    """Given scraped data, run the prediction models used by the tool."""

    print(scraped_data)

    for stock in scraped_data:
        print(stock['stock'])
        historical_data = stock['stock_historical_data']

        dates = historical_data['Date'].to_numpy()
        prices = historical_data['Close'].to_numpy()

        print(dates)
        print(prices)
