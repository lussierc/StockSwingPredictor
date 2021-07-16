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


@pytest.mark.parametrize(
    "stock_name, prev_close, date, period, swing_predictions, next_day_predictions, model_scores, figure, training_times, testing_times, new_predictions_times, prev_predictions_times",
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
            {
                "svr_lin": 1.419194729,
                "svr_poly": 0.017398838000000083,
                "svr_rbf": 0.0009485979999999117,
                "lr": 0.00044727600000005197,
                "en": 0.00033938900000052286,
                "lasso": 0.0002532669999997239,
                "knr": 0.0002626839999999575,
            },
            {
                "svr_lin": 0.00027037399999940703,
                "svr_poly": 0.00022543800000018877,
                "svr_rbf": 0.00023781600000027936,
                "lr": 0.00019492599999981763,
                "en": 0.00018125999999973885,
                "lasso": 0.00017680000000019902,
                "knr": 0.0006323699999999377,
            },
            {
                "svr_lin": 0.00011343500000027262,
                "svr_poly": 7.181300000080881e-05,
                "svr_rbf": 5.0917000000261226e-05,
                "lr": 3.609200000020962e-05,
                "en": 3.762399999995836e-05,
                "lasso": 3.350099999988032e-05,
                "knr": 0.00029530299999969145,
            },
            {
                "svr_lin": 9.268200000001059e-05,
                "svr_poly": 8.40960000001445e-05,
                "svr_rbf": 9.508499999988373e-05,
                "lr": 4.266499999960871e-05,
                "en": 4.0494999999474146e-05,
                "lasso": 3.730499999932135e-05,
                "knr": 0.0003003990000003398,
            },
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
    training_times,
    testing_times,
    new_predictions_times,
    prev_predictions_times,
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
        training_times,
        testing_times,
        new_predictions_times,
        prev_predictions_times,
    )

    assert prediction_results is not None
    assert prediction_results["next_day_predictions"] == next_day_predictions
    assert prediction_results["swing_predictions"] == swing_predictions
    assert prediction_results["date"] == "2021-05-09"
