"""Will house the Command Line Interface (CML) for the tool."""

from prettytable import PrettyTable

import data_cleaner
import json_handler
import prediction
import scraper


class color:
    """Defines different colors and text formatting settings to be used for CML output printing."""

    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def welcome_message():
    """Prints the welcome message for the project."""

    print(
        "\n\n   -----------------------------------------------"
        + "\n   |                                             |\n"
        + color.BOLD
        + color.GREEN
        + "   | Welcome to the StockSwingPredictor Program! |"
        + color.END
        + "\n   |                                             |"
        + "\n   |  A tool that predicts stock price swings!   |"
        + "\n   |                                             |"
        + color.END
        + "\n   -----------------------------------------------\n\n"
    )


def user_UI_choice():
    """Gets the user's UI choice to run the program with."""

    user_choice = 0  # set default value for user UI choice

    while not (user_choice == 1 or user_choice == 2):
        user_choice = int(
            input(
                color.BOLD
                + color.UNDERLINE
                + "Would you like to run the program using the Command Line UI or the Web UI?"
                + color.END
                + "\n\t- Enter 1 to use the CML.\n\t- Enter 2 to use the Web App UI."
                + color.GREEN
                + "\n* Enter your choice: "
                + color.END
            )
        )

    return user_choice


def run_cml():
    """Runs the CML UI."""

    cml_startup_message()  # print the start-up message for the CML

    stocks = get_user_stocks()  # get the user's input of stock ticker symbols

    print()  # spacing purposes

    period = get_scraping_time_period()

    scraped_data = scraper.perform_scraping(
        stocks, period
    )  # scrape data for given stocks with the given historical time period

    finalized_data = prediction.run_predictor(scraped_data, period)

    display_results(finalized_data)  # allows users to interact with generated results


def cml_startup_message():
    """CML Interface startup message."""

    print(
        "\n\n   -------------------------------------------\n"
        + color.BOLD
        + "   |      Starting the    CML version!       |"
        + color.END
        + "\n   -------------------------------------------\n\n"
    )


def get_user_stocks():
    """Gets the user's stock ticker symbols."""

    print(
        color.BOLD
        + color.UNDERLINE
        + "Please enter your Stock Ticker Symbol(s) below:"
        + color.END
        + color.END
    )

    done = False
    stocks = []

    while done is not True:
        stock = input("* Enter your Stock Ticker Symbol: ")
        stocks.append(stock)

        print("\t* Would you like to add more stocks?")
        continue_dec = input(color.GREEN + "\t\t* Y or N?: " + color.END).upper()

        if continue_dec == "Y":
            pass
        else:
            done = True

    return stocks


def display_results(finalized_data):
    """Allow the user to interact with the scraped & predicted stock data."""

    for stock_data in finalized_data:
        stock_name = stock_data["stock"]
        predictions = stock_data["prediction_results"]
        swing_predictions = predictions["swing_predictions"]
        next_day_predictions = predictions["next_day_predictions"]
        training_times = predictions["training_times"]
        testing_times = predictions["testing_times"]
        new_predictions_times = predictions["new_predictions_times"]
        prev_predictions_times = predictions["prev_predictions_times"]
        figure = predictions["figure"]
        model_scores = predictions["model_scores"]
        models = ["svr_lin", "svr_poly", "svr_rbf", "lr", "en", "lasso", "knr"]
        stock_info = stock_data["stock_info"]

        print(
            "\n\n\n"
            + color.BOLD
            + color.UNDERLINE
            + color.YELLOW
            + "The Results of Scraping & Predicting for: "
            + stock_name
            + ":"
            + color.END
            + color.END
            + color.END,
        )

        print(
            color.UNDERLINE
            + " - Would you like to view the Plotly figure of model predictions for: "
            + stock_name
            + " ?"
            + color.END
        )
        print_res = input(color.GREEN + "\t* Y or N?: " + color.END).upper()
        if print_res == "Y":
            figure.show()
        else:
            pass

        print_tables(
            predictions,
            swing_predictions,
            next_day_predictions,
            model_scores,
            models,
            stock_info,
            stock_name,
            training_times,
            testing_times,
            new_predictions_times,
            prev_predictions_times,
        )

        print(
            "\n"
            + color.UNDERLINE
            + " - Would you like to export the generated results for: "
            + stock_name
            + " ?"
            + color.END
        )
        exp_dec = input(color.GREEN + "\t* Y or N?: " + color.END).upper()

        if exp_dec == "Y":
            print(
                "\n\t"
                + color.UNDERLINE
                + "- Do you have a previously exported file you want to append data to?"
                + color.END
            )
            imp_dec = input(color.GREEN + "\t\t* Y or N?: " + color.END).upper()

            if imp_dec == "Y":
                import_file = input(
                    color.GREEN
                    + "\t\t\t* What is your import file name (ex: 'myoldfile.json')?: "
                    + color.END
                )
                json_handler.append_json(predictions, import_file)

            else:
                export_file = input(
                    color.GREEN
                    + "\t\t\t* What is your export file name (ex: 'myfile.json')?: "
                    + color.END
                )
                json_handler.export_json(predictions, export_file)
        else:
            pass


def print_tables(
    predictions,
    swing_predictions,
    next_day_predictions,
    model_scores,
    models,
    stock_info,
    stock_name,
    training_times,
    testing_times,
    new_predictions_times,
    prev_predictions_times,
):
    """Prints out tables of generated results."""

    print(
        color.BOLD,
        "\nThe current/previous closing price for the given stock is: $",
        predictions["current_prev_close"],
        color.END,
    )
    ################################
    print(
        "\n"
        + color.UNDERLINE
        + " - Would you like to print out the model prediction results for: "
        + stock_name
        + " ?"
        + color.END
    )
    print_res = input(color.GREEN + "\t* Y or N?: " + color.END).upper()
    if print_res == "Y":
        table2 = PrettyTable()
        table2.field_names = [
            "ML Model",
            "Swing Prediction",
            "Price Prediction",
            "Model Score",
        ]  # define field names for table

        for model in models:
            table2.add_row(
                [
                    model,
                    swing_predictions[model],
                    next_day_predictions[model],
                    model_scores[model],
                ]
            )  # add data to table

        print(table2)  # print prettytable of scored stock info
    else:
        pass
    ################################
    print(
        "\n"
        + color.UNDERLINE
        + " - Would you like to print out the model efficiency timings for: "
        + stock_name
        + " ?"
        + color.END
    )
    print_res = input(color.GREEN + "\t* Y or N?: " + color.END).upper()
    if print_res == "Y":
        print(
            "Displaying the time in seconds it took models to complete certain tasks:"
        )
        table1 = PrettyTable()
        table1.field_names = [
            "Model",
            "Training",
            "Testing/Scoring",
            "Future Predictions",
            "Historical Prediction",
        ]  # define field names for table

        for model in models:
            table1.add_row(
                [
                    model,
                    training_times[model],
                    testing_times[model],
                    new_predictions_times[model],
                    prev_predictions_times[model],
                ]
            )  # add data to table

        print(table1)  # print prettytable of scored stock info
    else:
        pass
    ################################
    print(
        "\n"
        + color.UNDERLINE
        + " - Would you like to print out the stock information for: "
        + stock_name
        + " ?"
        + color.END
    )
    print_res = input(color.GREEN + "\t* Y or N?: " + color.END).upper()

    if print_res == "Y":
        table3 = PrettyTable()
        variables = [
            "longName",
            "symbol",
            "sector",
            "industry",
            "fullTimeEmployees",
            "open",
            "regularMarketPreviousClose",
            "fiftyDayAverage",
            "twoHundredDayAverage",
            "dayLow",
            "dayHigh",
            "fiftyTwoWeekLow",
            "fiftyTwoWeekHigh",
            "volume",
            "averageVolume",
            "averageVolume10days",
        ]  # define field names for table

        table3.field_names = ["Variable", "Information"]

        for variable in variables:
            table3.add_row([variable, stock_info[variable]])

        print(table3)
        print(
            color.BOLD
            + "\nBusiness Summary:   "
            + color.END
            + stock_info["longBusinessSummary"]
        )

    else:
        pass


def get_scraping_time_period():
    """Gets the user's decision for how many months worth of historical price data to scrape."""

    print(
        "\n"
        + color.BOLD
        + color.UNDERLINE
        + "Enter Y to scrape custom date ranges of data or enter N to use the recommend value:"
        + color.END
        + color.END
    )

    custom_range_choice = input(color.GREEN + "\t* Y or N?: " + color.END).upper()

    if custom_range_choice == "Y":
        custom_range_choice = 11
        while custom_range_choice >= 10:
            print(
                "\t\t"
                + color.BOLD
                + color.UNDERLINE
                + "Choose a date range of the past:"
                + color.END
                + color.END
            )
            print(
                "\t\t\t1) 5 days\n\t\t\t2) 1 month\n\t\t\t3) 3 months\n\t\t\t4) 6 months\n\t\t\t5) 1 year\n\t\t\t6) 2 years\n\t\t\t7) 5 years\n\t\t\t8) 10 Years\n\t\t\t9) Max\n\t\t\t10) YTD"
            )  # should use a slider for this in the Streamlit UI
            custom_range_choice = int(
                input(
                    color.GREEN
                    + color.BOLD
                    + color.UNDERLINE
                    + "Enter the corresponding number for your chosen range: "
                    + color.END
                    + color.END
                    + color.END
                )
            )
        if custom_range_choice == 1:
            return "5d"
        elif custom_range_choice == 2:
            return "1mo"
        elif custom_range_choice == 3:
            return "3mo"
        elif custom_range_choice == 4:
            return "6mo"
        elif custom_range_choice == 5:
            return "1y"
        elif custom_range_choice == 6:
            return "2y"
        elif custom_range_choice == 7:
            return "5y"
        elif custom_range_choice == 8:
            return "10y"
        elif custom_range_choice == 9:
            return "max"
        elif custom_range_choice == 10:
            return "ytd"
        else:
            return "3mo"
    else:
        return "3mo"  # recommended time period
