"""Tests the functions of the data cleaner."""

import pytest
import pandas as pd

import data_cleaner, scraper


def test_clean_scraped_prediction_data():
    """Tests to ensure dates and prices scraped by the tool are prepped for ML predictions."""

    data = scraper.scrape_stock_historical_data("AAPL", "1mo")

    dates, prices = data_cleaner.clean_scraped_prediction_data(data)

    assert prices is not None
    assert dates[0] == 0
    assert dates[1] == 1
    assert prices is not None


@pytest.mark.parametrize(
    "stock_name, prev_close, date, period, swing_predictions, next_day_predictions, model_scores, figure",
    [
        (
            "DKNG",
            48.41999816894531,
            "2021-05-09",
            "5d",
            {
                "svr_lin": "Down",
                "svr_poly": "Down",
                "svr_rbf": "Up",
                "lr": "Down",
                "en": "Up",
                "lasso": "Up",
                "knr": "Up",
            },
            {
                "svr_lin": 47.54999771118153,
                "svr_poly": 43.448746109008795,
                "svr_rbf": 50.59113328256789,
                "lr": 47.47199745178223,
                "en": 49.36559799194336,
                "lasso": 48.97199745178223,
                "knr": 53.94000015258789,
            },
            {
                "svr_lin": 0.8549982220416815,
                "svr_poly": 0.9627131160195981,
                "svr_rbf": 0.9990760565942345,
                "lr": 0.8553194958036401,
                "en": 0.7820092418872298,
                "lasso": 0.8093181535221026,
                "knr": 0.0,
            },
            None,
        )
    ],
)
def test_organize_prediction_results(
    stock_name,
    prev_close,
    date,
    period,
    swing_predictions,
    next_day_predictions,
    model_scores,
    figure,
):
    """Tests to ensure the function can correctly store and format prediction results."""

    prediction_results = data_cleaner.organize_prediction_results(
        stock_name,
        next_day_predictions,
        swing_predictions,
        model_scores,
        prev_close,
        period,
        date,
        figure,
    )

    assert prediction_results is not None
    assert prediction_results["next_day_predictions"] == next_day_predictions
    assert prediction_results["swing_predictions"] == swing_predictions
    assert prediction_results["date"] == "2021-05-09"
