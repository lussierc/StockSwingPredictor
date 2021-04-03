"""Will test the functions of the JSON file handler."""

import pytest
import os.path
from os import path
from shutil import copyfile

from src import json_handler

def test_import_json():
    """Tests to see if a JSON file can be imported correctly."""

    import_file = "tests/testing_input_files/test_import.json"

    imported_file_data = json_handler.import_json(import_file)

    assert imported_file_data is not None

def test_export_json():
    """Tests to see if a JSON file can be exported correctly."""

    export_data = {"swing_predictions": {"svr_lin": "Up", "svr_poly": "Up", "svr_rbf": "Down", "lr": "Up", "en": "Up", "lasso": "Up", "knr": "Down"}, "next_day_predictions": {"svr_lin": 69.03999786514653, "svr_poly": 74.84891850687377, "svr_rbf": 59.70274381960691, "lr": 69.5740961208979, "en": 69.51023900808904, "lasso": 69.47573546516018, "knr": 61.402000427246094}, "prev_close": 62.880001068115234, "model_scores": {"svr_lin": 0.669390278607721, "svr_poly": 0.4707890315776885, "svr_rbf": 0.8576201173987886, "lr": 0.6729075190612774, "en": 0.6728768857836338, "lasso": 0.6728348385890528, "knr": 0.9306431524754305}, "price_swing_prediction": "Down (1)", "svr_knr_price_avg": 60.5523721234265, "multi_fold_price_avg": 65.04726984395998, "data_time_period": "3mo", "date": "2021-04-02"}
    export_file = "tests/testing_input_files/test_export.json"

    json_handler.export_json(export_data, export_file)

    assert path.exists('tests/testing_input_files/test_export.json') == True

    os.remove(export_file)

    assert path.exists('tests/testing_input_files/test_export.json') == False

def test_append_to_json():
    """Tests to see if a JSON file can be imported correctly and then appended to."""

    new_data = {"swing_predictions": {"svr_lin": "Down", "svr_poly": "Down", "svr_rbf": "Up", "lr": "Down", "en": "Down", "lasso": "Down", "knr": "Down"}, "next_day_predictions": {"svr_lin": 120.17706501172552, "svr_poly": 118.52845074304722, "svr_rbf": 123.97418079149483, "lr": 120.14958580658588, "en": 120.21123536097718, "lasso": 120.24794646232358, "knr": 121.53000030517578}, "prev_close": 123.0, "model_scores": {"svr_lin": 0.4523895926146947, "svr_poly": 0.5262019597177885, "svr_rbf": 0.8448432868159381, "lr": 0.4762592114122084, "en": 0.47623126623141654, "lasso": 0.4761880753418225, "knr": 0.9329122786743126}, "price_swing_prediction": "Down (1)", "svr_knr_price_avg": 122.7520905483353, "multi_fold_price_avg": 121.46625056605842, "data_time_period": "3mo", "date": "2021-04-03"}

    import_file = "tests/testing_input_files/test_append2.json"

    copyfile("tests/testing_input_files/test_append.json", import_file)

    file_list = json_handler.append_json(new_data, import_file)

    assert len(file_list) == 2
    assert path.exists('tests/testing_input_files/test_append.json') == True

    os.remove(import_file)

    assert path.exists(import_file) == False 
