"""Handles JSON files for the project."""

import json

def import_json():
    """Imports a previously exported JSON file."""
    # TODO


def export_json(prediction_results, export_file):
    """Exports a JSON file of tool prediction results."""

    prediction_results.pop('figure', None) # remove the figure from the results to be exported

    with open(export_file, "w") as outfile:
        json.dump(prediction_results, outfile)
