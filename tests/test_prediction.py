"""Will test the functions of the stock price swing prediction feature."""

import pytest
import prediction


# @pytest.mark.parametrize(
#     "example_letters, expected_asciis",
#     [(["a", "A", "C", "z"], [65, 65, 67, 90])],
# )


# def test_run_predictor():
#     """Tests to see if all predictions are properly completed."""
#
#     stock_data =

# @pytest.mark.parametrize(
#     "example_letters, expected_asciis",
#     [(["a", "A", "C", "z"], [65, 65, 67, 90])],
# )
# def test_ml_predictions():
#     """Ensures ML predictions, scoring, and model creation are properly completed."""


def test_create_ml_models():
    svr_lin, svr_poly, svr_rbf, lr, en, lasso, knr = prediction.create_ml_models()

    assert svr_lin is not None
    assert svr_poly is not None
    assert svr_rbf is not None
    assert lr is not None
    assert en is not None
    assert lasso is not None
    assert knr is not None


# def test_train_ml_models():
# def test_testscore_ml_models():
# def test_make_new_predictions():
# def test_plot_predictions():
# def test_predict_indiv_model_swing():
# def test_predict_price_swing():
