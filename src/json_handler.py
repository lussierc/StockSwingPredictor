"""Handles JSON files for the project."""

import json


def append_json(prediction_results, import_file):
    """Imports and appends new results to a previously exported JSON file."""

    try:
        file_data = json.load(open(import_file))

        if type(file_data) is dict:  # convert imported data to list if not
            file_data = [file_data]

        prediction_results.pop(
            "figure", None
        )  # remove the figure from the results to be exported

        file_data.append(prediction_results)

        with open(import_file, "w") as outfile:
            json.dump(file_data, outfile)
    except:
        # if no file is found, create and export a new one:
        export_json(prediction_results, import_file)


def export_json(prediction_results, export_file):
    """Exports to a new JSON file of generated tool prediction results."""

    prediction_results.pop(
        "figure", None
    )  # remove the figure from the results to be exported

    with open(export_file, "w") as outfile:
        json.dump(prediction_results, outfile)
