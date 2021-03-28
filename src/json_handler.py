"""Handles JSON files for the project."""

import json

def append_json(prediction_results, import_file):
    """Imports a previously exported JSON file."""
    file_data = json.load(open(import_file))

    # convert data to list if not
    if type(file_data) is dict:
        file_data = [file_data]

    prediction_results.pop('figure', None) # remove the figure from the results to be exported

    file_data.append(prediction_results)

    with open(import_file, 'w') as outfile:
        json.dump(file_data, outfile)

def export_json(prediction_results, export_file):
    """Exports a JSON file of tool prediction results."""

    prediction_results.pop('figure', None) # remove the figure from the results to be exported

    with open(export_file, "w") as outfile:
        json.dump(prediction_results, outfile)
