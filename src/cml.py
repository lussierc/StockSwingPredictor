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
                + "\n   - Enter 1 to use the CML. \n   - Enter 2 to use the Web App UI."
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

        print("     * Would you like to add more stocks?")
        continue_dec = input(color.GREEN + "       * Y or N?: " + color.END).upper()

        if continue_dec == "Y":
            pass
        else:
            done = True

    return stocks


def print_tables(finalized_data):
    """Given scraped and predicted stock data, print a table of major attributes."""

    for stock_data in finalized_data:
        print("\n\n\n" + color.BOLD + color.UNDERLINE +
            "Would you like to print out the prediction results for: " +
            stock_data["stock"] +
            " ?" + color.END + color.END
        )
        print_res = input(color.GREEN + "   * Y or N?: " + color.END).upper()
        if print_res == "Y":
            table = PrettyTable()
            table.field_names = [
                "swing_prediction",
                "price_prediction",
                "prev_close/current_price",
                "svr_rbf_score",
            ]  # define field names for table

            predictions = stock_data["prediction_results"]
            table.add_row(
                [
                    predictions["swing_prediction"],
                    predictions["price_prediction"],
                    predictions["prev_close"],
                    predictions["svr_rbf_score"],
                ]
            )  # add data to table

            print(table)  # print prettytable of scored stock info
        else:
            pass

        print("\n\n\n" + color.BOLD + color.UNDERLINE +
            "Would you like to print out the stock information for: " +
            stock_data["stock"] +
            " ?" + color.END + color.END
        )
        print_res = input(color.GREEN + "   * Y or N?: " + color.END).upper()

        if print_res == "Y":
            table2 = PrettyTable()
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

            table2.field_names = ["Variable", "Information"]

            for variable in variables:
                table2.add_row([variable, stock_info[variable]])

            print(table2)
            print(
                color.BOLD
                + "\nBusiness Summary:   "
                + color.END
                + stock_info["longBusinessSummary"]
            )

        else:
            pass


def run_cml():
    """Runs the CML UI."""

    cml_startup_message()  # print the start-up message for the CML

    stocks = get_user_stocks()  # get the user's input of stock ticker symbols

    print() # spacing purposes

    scraped_data = scraper.perform_scraping(stocks)  # scrape data for given stocks

    finalized_data = prediction.run_predictor(scraped_data)

    print_tables(finalized_data) # prints out tables of finalized data & predictions
