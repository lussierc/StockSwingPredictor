"""Will test the functions of the stock price swing prediction feature."""

import pytest
import prediction


from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import Lasso
from sklearn.neighbors import KNeighborsRegressor

# @pytest.mark.parametrize(
#     "example_letters, expected_asciis",
#     [(["a", "A", "C", "z"], [65, 65, 67, 90])],
# )


# def test_run_predictor():
#     """Tests to see if all predictions are properly completed."""
#
#     stock_data =

@pytest.mark.parametrize(
    "dates, prices, next_date, stock_name, period",
    [([[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22]], [68.58000183105469, 65.75, 61.90999984741211, 59.52000045776367, 60.5, 62.20000076293945, 69.29000091552734, 71.61000061035156, 71.75, 67.75, 67.13999938964844, 70.6500015258789, 67.61000061035156, 71.9800033569336, 71.72000122070312, 69.75, 66.62999725341797, 65.86000061035156, 63.599998474121094, 58.20000076293945, 61.0, 61.33000183105469, 62.880001068115234], [23], 'DKNG', '1mo')],
)
def test_ml_predictions(dates, prices, next_date, stock_name, period):
    """Ensures ML predictions, scoring, and model creation are properly completed."""

    next_day_predictions, model_swing_predictions, model_scores, prev_close, price_swing_prediction, figure = prediction.ml_predictions(dates, prices, next_date, stock_name, period)

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
    [([[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22]], [68.58000183105469, 65.75, 61.90999984741211, 59.52000045776367, 60.5, 62.20000076293945, 69.29000091552734, 71.61000061035156, 71.75, 67.75, 67.13999938964844, 70.6500015258789, 67.61000061035156, 71.9800033569336, 71.72000122070312, 69.75, 66.62999725341797, 65.86000061035156, 63.599998474121094, 58.20000076293945, 61.0, 61.33000183105469, 62.880001068115234], SVR(kernel="linear", C=1e3), SVR(kernel="poly", C=1e3, degree=2), SVR(kernel="rbf", C=1e3, degree=3, gamma="scale"), LinearRegression(), ElasticNet(), Lasso(), KNeighborsRegressor())],
)
def test_train_ml_models(dates, prices, svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr):
    """Tests to see if ML models are trained without issues."""

    svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr = prediction.train_ml_models(svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr, dates, prices)

    assert svr_lin is not None
    assert svr_poly is not None
    assert svr_rbf is not None
    assert lr is not None
    assert en is not None
    assert lasso is not None
    assert knr is not None


@pytest.mark.parametrize(
    "dates, prices, svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr",
    [([[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22]], [68.58000183105469, 65.75, 61.90999984741211, 59.52000045776367, 60.5, 62.20000076293945, 69.29000091552734, 71.61000061035156, 71.75, 67.75, 67.13999938964844, 70.6500015258789, 67.61000061035156, 71.9800033569336, 71.72000122070312, 69.75, 66.62999725341797, 65.86000061035156, 63.599998474121094, 58.20000076293945, 61.0, 61.33000183105469, 62.880001068115234], SVR(kernel="linear", C=1e3), SVR(kernel="poly", C=1e3, degree=2), SVR(kernel="rbf", C=1e3, degree=3, gamma="scale"), LinearRegression(), ElasticNet(), Lasso(), KNeighborsRegressor())],
)
def test_testscore_ml_models(dates, prices, svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr):
    """Tests to ensure that models are properly scored."""

    svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr = prediction.train_ml_models(svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr, dates, prices)

    model_scores = prediction.test_ml_models(dates, prices, svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr)

    assert model_scores is not None

    for key in model_scores.keys():
        assert model_scores[key] is not 0.0 # ensure dictionary keys are still not set at the defailt value

# def test_make_new_predictions():
# def test_plot_predictions():
# def test_predict_indiv_model_swing():
# def test_predict_price_swing():
