"""Tests the functions of the stock price swing prediction feature."""

import pytest
import prediction

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import Lasso
from sklearn.neighbors import KNeighborsRegressor
from datetime import date
import pandas as pd


@pytest.mark.parametrize(
    "test1, test2, test3, test4, test5, test6, test7",
    [
        (
            {
                "svr_lin": "Up",
                "svr_poly": "Up",
                "svr_rbf": "Down",
                "lr": "Up",
                "en": "Up",
                "lasso": "Up",
                "knr": "Down",
            },
            {
                "svr_lin": "Up",
                "svr_poly": "Up",
                "svr_rbf": "Down",
                "lr": "Down",
                "en": "Up",
                "lasso": "Up",
                "knr": "Down",
            },
            {
                "svr_lin": "Up",
                "svr_poly": "Up",
                "svr_rbf": "Down",
                "lr": "Down",
                "en": "Down",
                "lasso": "Up",
                "knr": "Down",
            },
            {
                "svr_lin": "Up",
                "svr_poly": "Up",
                "svr_rbf": "Down",
                "lr": "Up",
                "en": "Up",
                "lasso": "Up",
                "knr": "Up",
            },
            {
                "svr_lin": "Up",
                "svr_poly": "Up",
                "svr_rbf": "Up",
                "lr": "Down",
                "en": "Up",
                "lasso": "Up",
                "knr": "Up",
            },
            {
                "svr_lin": "Up",
                "svr_poly": "Up",
                "svr_rbf": "Up",
                "lr": "Up",
                "en": "Up",
                "lasso": "Up",
                "knr": "Up",
            },
            {
                "svr_lin": "Up",
                "svr_poly": "Up",
                "svr_rbf": "Down",
                "lr": "Down",
                "en": "Up",
                "lasso": "Up",
                "knr": "Up",
            },
        )
    ],
)
def test_predict_price_swing(test1, test2, test3, test4, test5, test6, test7):
    """Tests if the tool can predict the expected price swing given a number of examples."""

    swing = prediction.predict_price_swing(test1)
    swing2 = prediction.predict_price_swing(test2)
    swing3 = prediction.predict_price_swing(test3)
    swing4 = prediction.predict_price_swing(test4)
    swing5 = prediction.predict_price_swing(test5)
    swing6 = prediction.predict_price_swing(test6)
    swing7 = prediction.predict_price_swing(test7)

    assert swing == "Down (1)"
    assert swing2 == "Down (2)"
    assert swing3 == "Down (3)"
    assert swing4 == "Up (1)"
    assert swing5 == "Up (2)"
    assert swing6 == "Up (3)"
    assert swing7 == "None"


@pytest.mark.parametrize(
    "scraped_data, period",
    [
        (
            [
                {
                    "stock": "AAPL",
                    "stock_info": {
                        "zip": "95014",
                        "sector": "Technology",
                        "fullTimeEmployees": 147000,
                        "longBusinessSummary": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. It also sells various related services. The company offers iPhone, a line of smartphones; Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories comprising AirPods, Apple TV, Apple Watch, Beats products, HomePod, iPod touch, and other Apple-branded and third-party accessories. It also provides AppleCare support services; cloud services store services; and operates various platforms, including the App Store, that allow customers to discover and download applications and digital content, such as books, music, video, games, and podcasts. In addition, the company offers various services, such as Apple Arcade, a game subscription service; Apple Music, which offers users a curated listening experience with on-demand radio stations; Apple News+, a subscription news and magazine service; Apple TV+, which offers exclusive original content; Apple Card, a co-branded credit card; and Apple Pay, a cashless payment service, as well as licenses its intellectual property. The company serves consumers, and small and mid-sized businesses; and the education, enterprise, and government markets. It sells and delivers third-party applications for its products through the App Store. The company also sells its products through its retail and online stores, and direct sales force; and third-party cellular network carriers, wholesalers, retailers, and resellers. Apple Inc. was founded in 1977 and is headquartered in Cupertino, California.",
                        "city": "Cupertino",
                        "phone": "408-996-1010",
                        "state": "CA",
                        "country": "United States",
                        "companyOfficers": [],
                        "website": "http://www.apple.com",
                        "maxAge": 1,
                        "address1": "One Apple Park Way",
                        "industry": "Consumer Electronics",
                        "previousClose": 122.15,
                        "regularMarketOpen": 123.66,
                        "twoHundredDayAverage": 123.17168,
                        "trailingAnnualDividendYield": 0.006606631,
                        "payoutRatio": 0.2177,
                        "volume24Hr": None,
                        "regularMarketDayHigh": 124.18,
                        "navPrice": None,
                        "averageDailyVolume10Day": 92095983,
                        "totalAssets": None,
                        "regularMarketPreviousClose": 122.15,
                        "fiftyDayAverage": 123.306366,
                        "trailingAnnualDividendRate": 0.807,
                        "open": 123.66,
                        "toCurrency": None,
                        "averageVolume10days": 92095983,
                        "expireDate": None,
                        "yield": None,
                        "algorithm": None,
                        "dividendRate": 0.82,
                        "exDividendDate": 1612483200,
                        "beta": 1.251354,
                        "circulatingSupply": None,
                        "startDate": None,
                        "regularMarketDayLow": 122.49,
                        "priceHint": 2,
                        "currency": "USD",
                        "trailingPE": 33.360455,
                        "regularMarketVolume": 75089134,
                        "lastMarket": None,
                        "maxSupply": None,
                        "openInterest": None,
                        "marketCap": 2064936337408,
                        "volumeAllCurrencies": None,
                        "strikePrice": None,
                        "averageVolume": 109579404,
                        "priceToSalesTrailing12Months": 7.020369,
                        "dayLow": 122.49,
                        "ask": 123.05,
                        "ytdReturn": None,
                        "askSize": 1400,
                        "volume": 75089134,
                        "fiftyTwoWeekHigh": 145.09,
                        "forwardPE": 26.170214,
                        "fromCurrency": None,
                        "fiveYearAvgDividendYield": 1.39,
                        "fiftyTwoWeekLow": 62.345,
                        "bid": 123,
                        "tradeable": False,
                        "dividendYield": 0.0067000003,
                        "bidSize": 2900,
                        "dayHigh": 124.18,
                        "exchange": "NMS",
                        "shortName": "Apple Inc.",
                        "longName": "Apple Inc.",
                        "exchangeTimezoneName": "America/New_York",
                        "exchangeTimezoneShortName": "EDT",
                        "isEsgPopulated": False,
                        "gmtOffSetMilliseconds": "-14400000",
                        "quoteType": "EQUITY",
                        "symbol": "AAPL",
                        "messageBoardId": "finmb_24937",
                        "market": "us_market",
                        "annualHoldingsTurnover": None,
                        "enterpriseToRevenue": 7.14,
                        "beta3Year": None,
                        "profitMargins": 0.21735,
                        "enterpriseToEbitda": 24.662,
                        "52WeekChange": 0.8744999,
                        "morningStarRiskRating": None,
                        "forwardEps": 4.7,
                        "revenueQuarterlyGrowth": None,
                        "sharesOutstanding": 16788100096,
                        "fundInceptionDate": None,
                        "annualReportExpenseRatio": None,
                        "bookValue": 3.936,
                        "sharesShort": 107011007,
                        "sharesPercentSharesOut": 0.0064,
                        "fundFamily": None,
                        "lastFiscalYearEnd": 1601078400,
                        "heldPercentInstitutions": 0.59769,
                        "netIncomeToCommon": 63929999360,
                        "trailingEps": 3.687,
                        "lastDividendValue": 0.205,
                        "SandP52WeekChange": 0.50914145,
                        "priceToBook": 31.25,
                        "heldPercentInsiders": 0.00075999997,
                        "nextFiscalYearEnd": 1664150400,
                        "mostRecentQuarter": 1608940800,
                        "shortRatio": 0.89,
                        "sharesShortPreviousMonthDate": 1613088000,
                        "floatShares": 16770804261,
                        "enterpriseValue": 2100152762368,
                        "threeYearAverageReturn": None,
                        "lastSplitDate": 1598832000,
                        "lastSplitFactor": "4:1",
                        "legalType": None,
                        "lastDividendDate": 1612483200,
                        "morningStarOverallRating": None,
                        "earningsQuarterlyGrowth": 0.293,
                        "dateShortInterest": 1615766400,
                        "pegRatio": 1.84,
                        "lastCapGain": None,
                        "shortPercentOfFloat": 0.0064,
                        "sharesShortPriorMonth": 88329668,
                        "impliedSharesOutstanding": None,
                        "category": None,
                        "fiveYearAverageReturn": None,
                        "regularMarketPrice": 123.66,
                        "logo_url": "https://logo.clearbit.com/apple.com",
                    },
                    "stock_current_data": "",
                    "stock_historical_data": "",
                }
            ],
            "3mo",
        )
    ],
)
def test_run_predictor(scraped_data, period):
    """Tests to see if all predictions are properly completed."""

    scraped_data[0]["stock_current_data"] = pd.read_csv(
        "tests/testing_input_files/current_data.csv"
    )  # read in current data DF
    scraped_data[0]["stock_historical_data"] = pd.read_csv(
        "tests/testing_input_files/hist_data.csv"
    )  # read in historical data DF

    finalized_data = prediction.run_predictor(scraped_data, period)

    assert finalized_data is not None


@pytest.mark.parametrize(
    "dates, prices, next_date, stock_name, period",
    [
        (
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
                [16],
                [17],
                [18],
                [19],
                [20],
                [21],
                [22],
            ],
            [
                68.58000183105469,
                65.75,
                61.90999984741211,
                59.52000045776367,
                60.5,
                62.20000076293945,
                69.29000091552734,
                71.61000061035156,
                71.75,
                67.75,
                67.13999938964844,
                70.6500015258789,
                67.61000061035156,
                71.9800033569336,
                71.72000122070312,
                69.75,
                66.62999725341797,
                65.86000061035156,
                63.599998474121094,
                58.20000076293945,
                61.0,
                61.33000183105469,
                62.880001068115234,
            ],
            [23],
            "DKNG",
            "1mo",
        )
    ],
)
def test_ml_predictions(dates, prices, next_date, stock_name, period):
    """Ensures ML predictions, scoring, and model creation are properly completed."""

    (
        next_day_predictions,
        model_swing_predictions,
        model_scores,
        prev_close,
        price_swing_prediction,
        figure,
    ) = prediction.ml_predictions(dates, prices, next_date, stock_name, period)

    assert next_day_predictions is not None
    assert model_swing_predictions is not None
    assert model_scores is not None
    assert prev_close == prices[-1]
    assert price_swing_prediction is not None
    assert figure is not None


def test_create_ml_models():
    """Ensures that ML models are properly created."""

    svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr = prediction.create_ml_models()

    assert svr_lin is not None
    assert svr_poly is not None
    assert svr_rbf is not None
    assert lr is not None
    assert en is not None
    assert lasso is not None
    assert knr is not None


@pytest.mark.parametrize(
    "dates, prices, svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr",
    [
        (
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
                [16],
                [17],
                [18],
                [19],
                [20],
                [21],
                [22],
            ],
            [
                68.58000183105469,
                65.75,
                61.90999984741211,
                59.52000045776367,
                60.5,
                62.20000076293945,
                69.29000091552734,
                71.61000061035156,
                71.75,
                67.75,
                67.13999938964844,
                70.6500015258789,
                67.61000061035156,
                71.9800033569336,
                71.72000122070312,
                69.75,
                66.62999725341797,
                65.86000061035156,
                63.599998474121094,
                58.20000076293945,
                61.0,
                61.33000183105469,
                62.880001068115234,
            ],
            SVR(kernel="linear", C=1e3),
            SVR(kernel="poly", C=1e3, degree=2),
            SVR(kernel="rbf", C=1e3, degree=3, gamma="scale"),
            LinearRegression(),
            ElasticNet(),
            Lasso(),
            KNeighborsRegressor(),
        )
    ],
)
def test_train_ml_models(dates, prices, svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr):
    """Tests to see if ML models are trained without issues."""

    svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr = prediction.train_ml_models(
        svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr, dates, prices
    )

    assert svr_lin is not None
    assert svr_poly is not None
    assert svr_rbf is not None
    assert lr is not None
    assert en is not None
    assert lasso is not None
    assert knr is not None


@pytest.mark.parametrize(
    "dates, prices, svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr",
    [
        (
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
                [16],
                [17],
                [18],
                [19],
                [20],
                [21],
                [22],
            ],
            [
                68.58000183105469,
                65.75,
                61.90999984741211,
                59.52000045776367,
                60.5,
                62.20000076293945,
                69.29000091552734,
                71.61000061035156,
                71.75,
                67.75,
                67.13999938964844,
                70.6500015258789,
                67.61000061035156,
                71.9800033569336,
                71.72000122070312,
                69.75,
                66.62999725341797,
                65.86000061035156,
                63.599998474121094,
                58.20000076293945,
                61.0,
                61.33000183105469,
                62.880001068115234,
            ],
            SVR(kernel="linear", C=1e3),
            SVR(kernel="poly", C=1e3, degree=2),
            SVR(kernel="rbf", C=1e3, degree=3, gamma="scale"),
            LinearRegression(),
            ElasticNet(),
            Lasso(),
            KNeighborsRegressor(),
        )
    ],
)
def test_testscore_ml_models(
    dates, prices, svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr
):
    """Tests to ensure that models are properly scored."""

    svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr = prediction.train_ml_models(
        svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr, dates, prices
    )  # train models for scoring

    model_scores = prediction.test_ml_models(
        dates, prices, svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr
    )  # score models

    assert model_scores is not None

    for key in model_scores.keys():
        assert (
            model_scores[key] is not 0.0
        )  # ensure dictionary keys are still not set at the defailt value


@pytest.mark.parametrize(
    "dates, prices, svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr, next_date",
    [
        (
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
                [16],
                [17],
                [18],
                [19],
                [20],
                [21],
                [22],
            ],
            [
                68.58000183105469,
                65.75,
                61.90999984741211,
                59.52000045776367,
                60.5,
                62.20000076293945,
                69.29000091552734,
                71.61000061035156,
                71.75,
                67.75,
                67.13999938964844,
                70.6500015258789,
                67.61000061035156,
                71.9800033569336,
                71.72000122070312,
                69.75,
                66.62999725341797,
                65.86000061035156,
                63.599998474121094,
                58.20000076293945,
                61.0,
                61.33000183105469,
                62.880001068115234,
            ],
            SVR(kernel="linear", C=1e3),
            SVR(kernel="poly", C=1e3, degree=2),
            SVR(kernel="rbf", C=1e3, degree=3, gamma="scale"),
            LinearRegression(),
            ElasticNet(),
            Lasso(),
            KNeighborsRegressor(),
            [23],
        )
    ],
)
def test_make_new_predictions(
    dates, prices, svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr, next_date
):
    """Tests if new predictions can be properly made."""

    svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr = prediction.train_ml_models(
        svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr, dates, prices
    )  # train models

    next_date = np.reshape(
        next_date, (len(next_date), 1)
    )  # format the next_data var for prediction purposes

    next_day_predictions = prediction.make_new_predictions(
        svr_rbf, svr_lin, svr_poly, lr, en, lasso, knr, next_date
    )  # make new predictions

    assert next_day_predictions is not None


@pytest.mark.parametrize(
    "pred1, prev_close1, pred2, prev_close2, pred3, prev_close3",
    [(11, 10, 9, 10, 10, 10)],
)
def test_predict_indiv_model_swing(
    pred1, prev_close1, pred2, prev_close2, pred3, prev_close3
):
    """Ensures that model price swing predictions are made correctly."""

    price_swing1 = prediction.predict_indiv_model_swing(pred1, prev_close1)
    price_swing2 = prediction.predict_indiv_model_swing(pred2, prev_close2)
    price_swing3 = prediction.predict_indiv_model_swing(pred3, prev_close3)

    assert price_swing1 == "Up"
    assert price_swing2 == "Down"
    assert price_swing3 == "No Movement"
