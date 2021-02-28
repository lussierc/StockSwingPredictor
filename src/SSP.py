"""The StockSwingPredictor (SSP) tool."""

import cml


def main():
    """Runs the tool."""

    cml.welcome_message()  # prints the welcome message in the CML

    choice = cml.user_UI_choice()  # gets the user choice of UI to use
    if choice == 1:
        cml.run_cml()  # run the CML
    elif choice == 2:
        # run the web UI to be implemented later
        print("This feature is not currently active.")


main()
