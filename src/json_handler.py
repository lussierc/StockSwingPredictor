"""Handles JSON files for the project."""

import json

def import_json():
    """Imports a previously exported JSON file."""
    # TODO


def export_json(prediction_results):
    """Exports a JSON file of tool prediction results."""
    
    export_file = input("What file name do you want to export to?")

    prediction_results.pop('figure', None)

    with open(export_file, "w") as outfile:
        json.dump(prediction_results, outfile)
