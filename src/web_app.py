"""Web App user interface for the project using Streamlit."""

# imports:
import sys

import pandas as pd
import streamlit as st
from PIL import Image
from streamlit.hashing import _CodeHasher

import data_cleaner
import json_handler
import prediction
import scraper

if len(sys.argv) > 1:
    run_location = sys.argv[
        1
    ]  # determine whether it was run online or locally by system args
else:
    run_location = "web"

try:
    # Before Streamlit 0.65
    from streamlit.ReportThread import get_report_ctx
    from streamlit.server.Server import Server
except ModuleNotFoundError:
    # After Streamlit 0.65
    from streamlit.report_thread import get_report_ctx
    from streamlit.server.server import Server


def main():
    """Runs the web UI."""

    state = _get_state()
    pages = {
        "Home": page_home,
        "Dashboard": page_dashboard,
        "Settings": page_settings,
    }

    st.sidebar.title(":mag: Pages")
    page = st.sidebar.radio("Select your page:", tuple(pages.keys()))

    # Display the selected page with the session state
    pages[page](state)

    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()


def page_home(state):
    """The home page of the web app."""

    st.title(":house: Welcome to Stock Swing Predictor (SSP)")

    image = Image.open("ssp.png")  # load logo
    st.image(image, use_column_width=True)
    st.markdown("*Note:* This is a conceptual tool and should not be used to make real/serious trading decisions.")
    st.markdown("## Tool Overview:")
    st.markdown(
        "The Stock Swing Predictor makes future stock price swing predictions for any stock for the next day. Price swings are simply whether or not a price goes up or down, so with this the tool predicts which way a stocks price will move or swing for the upcoming day.\nPredictions are made using seven different models and with the user's choice of dataset size. The models are trained using the stock price data of previous days."
    )

    st.markdown("## Using the Tool:")
    st.markdown(
        "Using the tool is simple once you are in the Web Interface! To run the tool, go to the `Run Settings` page."
    )
    st.markdown(
        "After filling out the data fields for your chosen option, you can than click the button below to run the tool. After this, wait until the tool prompts you to `Go to the Prediction Dashboard to view your data`. Once prompted, you can then go to the Prediction Dashboard page and view your data."
    )

    st.markdown("## Experimental Results and Optimal Settings:")
    st.markdown(
        "Extensive experimentation was completed on the tool, the results of which are detailed in the README."
    )
    st.markdown("### Settings Recommendations:")
    st.markdown(
        "- It is recommended that one runs the tool with as much data as possible, as results are generally more accurate for all models. 1 or 2 years is the optimal amount of training data it seems, any more of that and you will be waiting for your results for a while."
    )
    st.markdown(
        "- With this, the most accurate model seems to be the SVR-POLY model (Support Vector Regression with a Polynomial kernel), especially when trained with 1 year of data. Experimental results show future prediction accuracy results of almost 80%. The SVR-RBF model is also quite accurate, when trained with one month of data."
    )

    st.markdown("### Some Experimental Results:")
    image2 = Image.open("results.png")  # load logo
    st.image(image2, use_column_width=True)

    st.markdown(
        "This shows how accurate models are and which amount of training data they are most accuate with. \n This table displays the predictions on 9 different stocks over 5 different days for each time period of data. This was done from 3/30/2021-4/6/2021. With this, the percentage represents the number of predictions that were correct, out of a total 45 predictions that were made for each time period of data."
    )
    st.markdown("## Get in Touch & Learn More:")
    st.markdown("- View source code on the [Project GitHub](https://github.com/lussierc/StockSwingPredictor). Consider contributing.")
    st.markdown("- View my personal website and get contact information [here](https://christianlussier.com).")
    st.markdown("## Disclaimer:")
    st.markdown("We are not responsible for any investment losses incurred by users. This tool is by no means, a be-all-end all for stock prediction and while it offers promise it should not be used to make serious trading decisons. It is a conceptual tool that is somewhat accurate and is meant give users insights into the potential uses of ML for stock prediction.")

def page_dashboard(state):
    """The prediction results dashboard page, where users can view generated results."""

    st.title(":chart_with_upwards_trend: Prediction Results Dashboard")

    st.markdown("# Select Stocks to View Results:")
    if state.finalized_data:
        for stock_data in state.finalized_data:
            st.write("---")
            st.markdown("## " + stock_data["stock"])
            if st.checkbox("View Results for " + stock_data["stock"]):

                ############################################

                st.markdown("### Historical Predictions:")

                df2 = pd.DataFrame.from_dict(stock_data["prev_predictions"])

                select_lbl = (
                    "Enter the names of models for " + stock_data["stock"] + ":"
                )
                models_selections = st.multiselect(
                    label=select_lbl,
                    options=df2.columns,
                )  # allow users to display specific model results on dataframe graph

                if not models_selections:  # if nothing is selected show all models!
                    st.line_chart(df2)
                else:
                    st.line_chart(df2[models_selections])

                st.markdown(
                    "*Note:* 'Prices' are the actual prices for those days. The rest are model predictions for those days.\nPrices (in USD) are on the y-axis, the day number in the data is on the x-axis."
                )

                ############################################

                st.markdown("### Future (Next-Day) Predictions:")

                df = pd.DataFrame()
                df = df.append(
                    pd.DataFrame(
                        [stock_data["prediction_results"]["swing_predictions"]]
                    )
                )
                df = df.append(
                    pd.DataFrame(
                        [stock_data["prediction_results"]["next_day_predictions"]]
                    )
                )
                df = df.append(
                    pd.DataFrame([stock_data["prediction_results"]["model_scores"]])
                )

                df.index = [
                    "Swing Predicton",
                    "Price Prediction ($)",
                    "Model Fit Score",
                ]
                df = df.transpose()
                df  # display chart

                st.markdown(
                    "- The current price of the stock is *$"
                    + str(
                        round(stock_data["prediction_results"]["current_prev_close"], 2)
                    )
                    + "*."
                )

                if state.period == "1mo":
                    st.markdown("- *Recommended Model (for 1mo):* SVR-RBF")
                    st.markdown(
                        "- *View the homescreen for more model & dataset size combination recommendations.*"
                    )
                elif state.period == "6mo":
                    st.markdown(
                        "- *Recommended Model (for 6mo):* SVR-Poly (most recommended), LR, EN, or Lasso."
                    )
                    st.markdown(
                        "- *View the homescreen for more model & dataset size combination recommendations.*"
                    )
                elif state.period == "1y":
                    st.markdown("- *Recommended Model (for 1yr):* SVR-Poly")
                    st.markdown(
                        "- *View the homescreen for more model & dataset size combination recommendations.*"
                    )
                else:
                    st.markdown(
                        "- *Note:* View the home screen for information about the best models and training data size combinations."
                    )

                ############################################
                st.markdown("### View Other Information:")

                if st.checkbox(
                    "View " + stock_data["stock"] + "'s Model Efficiency Timings"
                ):
                    st.markdown("#### Model Efficiencies:")
                    st.markdown(
                        "Shows the time in seconds it took models to complete specific tasks:"
                    )
                    df3 = pd.DataFrame()
                    df3 = df3.append(
                        pd.DataFrame(
                            [stock_data["prediction_results"]["training_times"]]
                        )
                    )
                    df3 = df3.append(
                        pd.DataFrame(
                            [stock_data["prediction_results"]["testing_times"]]
                        )
                    )
                    df3 = df3.append(
                        pd.DataFrame(
                            [stock_data["prediction_results"]["new_predictions_times"]]
                        )
                    )
                    df3 = df3.append(
                        pd.DataFrame(
                            [stock_data["prediction_results"]["prev_predictions_times"]]
                        )
                    )
                    df3.index = [
                        "Training",
                        "Testing/Scoring",
                        "Future Predictions",
                        "Historical Predictions",
                    ]
                    df3 = df3.transpose()
                    df3

                ############################################

                if st.checkbox("View " + stock_data["stock"] + "'s Information"):
                    st.markdown("#### Company Information:")
                    for key in stock_data["stock_info"].keys():
                        st.write("*", key + ":", stock_data["stock_info"][key])
    else:
        st.markdown(
            "## Generate data to populate and initialize this page by going to the 'Settings' page and running the tool!"
        )


def page_settings(state):
    """Settings page where user configures their options and runs the tool."""

    st.title(":wrench: Settings")
    st.markdown("## **Your chosen settings:**")
    display_state_values(state)

    st.write("---")
    st.markdown("#### Enter Stock Ticker Symbols:")
    state.stocks = st.text_input(
        "Enter Stock Symbols Separated by Commas (EX: AAPL, MSFT):",
        state.stocks or "",
    )

    state.stocks = state.stocks
    state.stocks_list = state.stocks.split(", ")

    st.markdown("#### Choose dataset size to train models with:")
    options = ["5d", "1mo", "3mo", "6mo", "1y", "5y", "10y", "max"]

    state.period = st.radio(
        "Choose amount of historical training data. 1 year is recommended, find more recommendations on homepage.",
        options,
        options.index(state.radio) if state.radio else 0,
    )

    if st.button("Run the Tool", state.run_button):
        state.run_button_checked = True
        st.markdown(
            "### *PLEASE WAIT! Scraping data, training models, and generating prediction results NOW!*"
        )
        state.scraped_data = scraper.perform_scraping(state.stocks_list, state.period)
        state.finalized_data = prediction.run_predictor(
            state.scraped_data, state.period
        )

    if state.run_button_checked == True:
        st.markdown("## *Go to the dashboard to view your newly scraped data data.*")

        if run_location == "local":
            st.markdown("### Export Options")
            if st.checkbox("Would you like to export results?", state.export_checkbox):
                state.export_checkbox = True
                st.markdown(
                    "#### Enter New or Existing Export File Name (filename.json):"
                )
                state.file_name = st.text_input(
                    "Enter the export filename.", state.input or ""
                )
                if state.file_name:
                    for data in state.finalized_data:
                        json_handler.append_json(
                            data["prediction_results"], state.file_name
                        )
                    st.markdown("Your data has been exported!")
                else:
                    st.markdown("Enter a file name to export data!")


def display_state_values(state):
    """Displays setting state values."""

    st.write("Ticker Symbols:", state.stocks)
    st.write("Tickers List:", state.stocks_list)
    st.write("Time Period:", state.period)
    st.write("Export Checkbox state:", state.export_checkbox)
    st.write("Export/Append file name:", state.file_name)

    if st.button("Clear state"):  # resets the state
        state.clear()


class _SessionState:
    """Adds session state capabilities to Streamlit."""

    def __init__(self, session, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(hash_funcs),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()

    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops caused by a constantly changing state value at each run.
        # Example: state.value += 1

        if self._state["is_rerun"]:
            self._state["is_rerun"] = False

        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(
                self._state["data"], None
            ):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)


def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")

    return session_info.session


def _get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session, hash_funcs)

    return session._custom_session_state


if __name__ == "__main__":
    main()
