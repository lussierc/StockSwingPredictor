# StockSwingPredictor
The StockSwingPredictor (SSP) is a WIP tool that will predict stock price swings. Implemented in Python as apart of my Allegheny College Senior Thesis.

## Running the Project
Currently you can only run the project locally. To do this ensure you have Python3 installed and then from the main directory of the project, run the command: `python3 src/ssp.py`.

## Testing the Project
To test the project locally using Pytest, simply run the command: `pytest tests`.

To test the project and generate a code coverage report, run the command: `pytest --cov=src tests/`.

### Results of Testing/Code Coverage Report:
```
collected 4 items

tests/test_scraper.py ....                                                                                                                                                                           [100%]

---------- coverage: platform darwin, python 3.9.0-final-0 -----------
Name             Stmts   Miss  Cover
------------------------------------
src/cml.py          39     39     0%
src/scraper.py      29      0   100%
src/ssp.py           9      9     0%
------------------------------------
TOTAL               77     48    38%


============================================================================================ 4 passed in 13.57s ============================================================================================
```
