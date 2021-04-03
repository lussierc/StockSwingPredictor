"""Will test the functions of the data cleaner."""

import pytest
import pandas as pd

from src import data_cleaner, scraper

def test_clean_scraped_prediction_data():
    """Tests to ensure dates and prices scraped by the tool are prepped for ML predictions."""

    data = scraper.scrape_stock_historical_data("AAPL", "1mo")

    dates, prices = data_cleaner.clean_scraped_prediction_data(data)

    assert prices is not None
    assert dates[0] == 0
    assert dates[1] == 1
    assert prices is not None


# @pytest.mark.parametrize(
#     "example_letters, expected_asciis",
#     [(["a", "A", "C", "z"], [65, 65, 67, 90])],
# )
@pytest.mark.parametrize(
    "next_day_predictions, swing_predictions, model_scores, prev_close, price_swing_prediction, period, date, figure",
    [({'svr_lin': 239.85058050250257, 'svr_poly': 237.41112033051695, 'svr_rbf': 237.81455809022657, 'lr': 240.68089689015713, 'en': 240.61815636002072, 'lasso': 240.58253623441942, 'knr': 236.33800354003907}, {'svr_lin': 'Down', 'svr_poly': 'Down', 'svr_rbf': 'Down', 'lr': 'Down', 'en': 'Down', 'lasso': 'Down', 'knr': 'Down'}, {'svr_lin': 0.2689262776060758, 'svr_poly': 0.1076795952496774, 'svr_rbf': 0.9067067740227178, 'lr': 0.2941381697991622, 'en': 0.294123040276283, 'lasso': 0.29410098446443833, 'knr': 0.9294954784877686}, 242.35000610351562, "Down (3)", "3mo", "2021-04-03", "testing_figure")],
)
def test_organize_prediction_results(next_day_predictions, swing_predictions, model_scores, prev_close, price_swing_prediction, period, date, figure):
    """Tests to ensure the function can correctly store and format prediction results."""

    prediction_results = data_cleaner.organize_prediction_results(next_day_predictions, swing_predictions, model_scores, prev_close, price_swing_prediction, period, date, figure)


    assert prediction_results is not None
