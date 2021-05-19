"""The StockSwingPredictor (SSP) tool."""

import cml
import os


def main():
    """Runs the tool."""

    cml.welcome_message()  # prints the welcome message in the CML

    choice = cml.user_UI_choice()  # gets the user choice of UI to use
    if choice == 1:
        cml.run_cml()  # run the CML
    elif choice == 2:
        # run the web UI to be implemented later
        print("\n\n*IMPORTANT: Here is the proper link if using the tool in DOCKER: http://localhost:8501")
        os.system("streamlit run src/web_app.py")

    else:
        print("Invalid option, running the CML...")
        cml.run_cml()  # run the CML


main()
