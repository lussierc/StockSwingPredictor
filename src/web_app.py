"""Web App user interface for the project using Streamlit."""

# imports:
import streamlit as st
import pandas as pd
from PIL import Image
from streamlit.hashing import _CodeHasher

import prediction, scraper, data_cleaner, json_handler

try:
    # Before Streamlit 0.65
    from streamlit.ReportThread import get_report_ctx
    from streamlit.server.Server import Server
except ModuleNotFoundError:
    # After Streamlit 0.65
    from streamlit.report_thread import get_report_ctx
    from streamlit.server.server import Server


def main():
    state = _get_state()
    pages = {
        "Home": page_home,
        "Dashboard": page_dashboard,
        "Settings": page_settings,
    }

    st.sidebar.title(":floppy_disk: Page states")
    page = st.sidebar.radio("Select your page", tuple(pages.keys()))

    # Display the selected page with the session state
    pages[page](state)

    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()

def page_home(state):
    """Sets up the home page of the web app."""

    st.title(":house: Welcome to Stock Swing Predictor (SSP)")

    image = Image.open("ssp.png")  # load logo
    st.image(image, use_column_width=True)

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
    st.markdown(
        "Within the Dashboard, you can then view information for all the stocks at once, or look at individual stocks and more specific information (pertaining to individual articles)."
    )

def page_dashboard(state):
    st.title(":chart_with_upwards_trend: Dashboard page")
    display_state_values(state)

    for stock_data in state.finalized_data:
        st.markdown("## Select Stocks to View Results:")
        if st.checkbox(stock_data["stock"]):
            st.write(stock_data)

            ############################################
            df = pd.DataFrame()
            df = df.append(pd.DataFrame([stock_data["prediction_results"]["swing_predictions"]]))
            df = df.append(pd.DataFrame([stock_data["prediction_results"]["model_scores"]]))
            df = df.append(pd.DataFrame([stock_data["prediction_results"]["next_day_predictions"]]))
            df.index = ['Swing Predicton', 'Model Score', 'Price Prediction']
            df = df.transpose()
            st.write(df)
            ############################################

            st.write(stock_data['prev_predictions'])

            df2 = pd.DataFrame.from_dict(stock_data['prev_predictions'])
            my_chart = st.line_chart(df2)
            st.write(my_chart)

def page_settings(state):
    st.title(":wrench: Settings")
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
    state.period = st.radio("Choose data length.", options, options.index(state.radio) if state.radio else 0)



    if st.button("Run the Tool", state.run):
        state.run = True
        st.markdown("### *PLEASE WAIT! Scraping data, training models, and generating prediction results NOW!*")
        state.scraped_data = scraper.perform_scraping(state.stocks_list, state.period)
        state.finalized_data = prediction.run_predictor(state.scraped_data, state.period)

    st.write(state.finalized_data)

    if state.run == True:
        st.markdown(
            "## *Go to the dashboard to view your newly scraped data data.*"
        )
        st.markdown("### Export Options")
        if st.checkbox("Would you like to export results?", state.export_checkbox):
            state.export_checkbox = True
            st.markdown("#### Enter New or Existing Export File Name (filename.json):")
            state.file_name = st.text_input("Enter the export filename.", state.input or "")
            for data in state.finalized_data:
                json_handler.append_json(data['prediction_results'], state.file_name)

def display_state_values(state):
    st.write("Ticker Symbols:", state.stocks)
    st.write("Tickers List:", state.stocks_list)
    st.write("Time Period:", state.period)
    st.write("Export Checkbox state:", state.export_checkbox)
    st.write("Export/Append file name:", state.file_name)

    if st.button("Clear state"):
        state.clear()


class _SessionState:

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

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False

        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
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
