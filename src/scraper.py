"""Will scrape the necessary real-time stock price and extraneous data for the tool."""

# import scraping libraries:
import bs4
import requests
from bs4 import BeautifulSoup
import yfinance as yf

def scrape_yahoo_finance_real_time():
    """Gathers real time stock prices and info from Yahoo! Finance."""

    # initialize scraper:
    link = 'https://finance.yahoo.com/quote/' + abbreviation + '?p=' + abbreviation
    url = requests.get(link)
    soup = bs4.BeautifulSoup(url.text, features="html.parser")

    # scrape the following data points for the given stock abbreviation:
    price = str(soup.find_all("div", {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text)
    previous_close = str(soup.find_all("td", {'class': 'Ta(end) Fw(600) Lh(14px)'})[0].find('span').text)
    open_price = str(soup.find_all("td", {'class': 'Ta(end) Fw(600) Lh(14px)'})[1].find('span').text)
    bid = str(soup.find_all("td", {'class': 'Ta(end) Fw(600) Lh(14px)'})[2].find('span').text)
    ask = str(soup.find_all("td", {'class': 'Ta(end) Fw(600) Lh(14px)'})[3].find('span').text)
    market_cap = str(soup.find_all("td", {'class': 'Ta(end) Fw(600) Lh(14px)'})[8].find('span').text)
    volume = str(soup.find_all("td", {'class': 'Ta(end) Fw(600) Lh(14px)'})[6].find('span').text)
    avg_volume = str(soup.find_all("td", {'class': 'Ta(end) Fw(600) Lh(14px)'})[7].find('span').text)

    return price, previous_close, open_price, bid, ask, market_cap, avg_volume, volume

def scrape_yahoo_finance_historical(stocks):
    """Scrape historical stock price data from Yahoo! Finanace."""

    msft = yf.Ticker(stocks)

    # get stock info
    msft.info

    # get historical market data
    hist = msft.history(period="1y")
    print(hist)
