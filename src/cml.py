"""Will house the Command Line Interface (CML) for the tool."""

import prediction, scraper, data_cleaner
from prettytable import PrettyTable


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


def print_tables(finalized_data):
    """Given scraped and predicted stock data, print a table of major attributes."""

    for stock_data in finalized_data:
        print("\n\n\n" + color.BOLD + color.UNDERLINE + color.YELLOW + "The Results of Scraping & Predicting for: ", stock_data["stock"], ":" + color.END + color.END + color.END)

        predictions = stock_data["prediction_results"]
        swing_predictions = predictions["swing_predictions"]
        next_day_predictions = predictions["next_day_predictions"]
        model_scores = predictions["model_scores"]
        models = ["svr_lin", "svr_poly", "svr_rbf", "lr", "en", "lasso", "knr"]

        print(
            color.UNDERLINE
            + " - Would you like to print out the overall results for: "
            + stock_data["stock"]
            + " ?"
            + color.END
        )
        print_res = input(color.GREEN + "\t* Y or N?: " + color.END).upper()
        if print_res == "Y":
            table = PrettyTable()
            table.field_names = [
                "Price Swing Prediction",
                "KNR & SVR Avg Price Prediction",
                "Multi-Fold Avg Price Prediction",
                "Current Price (or Closing if AH)",
            ]  # define field names for table


            table.add_row(
                [
                    predictions["price_swing_prediction"],
                    predictions["svr_knr_price_avg"],
                    predictions["multi_fold_price_avg"],
                    predictions["prev_close"],
                ]
            )  # add data to table

            print(table)  # print prettytable of scored stock info
        else:
            pass
        ################################
        print(
            "\n"
            + color.UNDERLINE
            + " - Would you like to print out the model prediction results for: "
            + stock_data["stock"]
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
                predictions = stock_data["prediction_results"]
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
            + " - Would you like to print out the stock information for: "
            + stock_data["stock"]
            + " ?"
            + color.END
        )
        print_res = input(color.GREEN + "\t* Y or N?: " + color.END).upper()

        if print_res == "Y":
            table3 = PrettyTable()
            stock_info = stock_data["stock_info"]
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
        "\n\n\n"
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
                "\t\t\t1) 5 days\n\t\t\t2) 1 month\n\t\t\t3) 6 months\n\t\t\t4) 1 year\n\t\t\t5) 2 years\n\t\t\t6) 5 years\n\t\t\t7) 10 years\n\t\t\t8) Max\n\t\t\t9) YTD"
            )  # should use a slider for this in the Streamlit UI
            custom_range_choice = int(
                input(
                    color.GREEN
                    + color.BOLD
                    + color.UNDERLINE
                    + "Enter the corresponding number for your chosen range:"
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
        else:
            return "3mo"
    else:
        return "3mo"  # recommended time period


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

    print_tables(finalized_data)  # prints out tables of finalized data & predictions
