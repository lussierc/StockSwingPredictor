"""Will test the functions of the JSON file handler."""

import pytest
from src import json_handler

def test_import_json():
    """Tests to see if a JSON file can be imported correctly."""

    import_file = "tests/testing_input_files/test_import.json"

    imported_file_data = json_handler.import_json(import_file)

    assert imported_file_data is not None
