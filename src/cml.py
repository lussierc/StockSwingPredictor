"""Will house the Command Line Interface (CML) for the tool."""

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

def cml_startup_message():
    """CML Interface startup message."""
    print(
    "\n\n   -------------------------------------------\n"
    + color.BOLD
    + "   |      Starting the    CML version!       |"
    + color.END
    + "\n   -------------------------------------------\n\n"
    )
