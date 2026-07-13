from data_handling import load_data, save_data, delete_row
import streamlit as st
import pandas as pd
from datetime import datetime, date
from dataclasses import dataclass, asdict


@dataclass
class AppState:
    '''
    A dataclass to hold the state of the application, including input values and flags and clearing out the 
    input values in the session state to their default values.

    '''
    show_confirm: bool = False
    clear_inputs: bool = False
    tx_date: date = date.today()
    tx_category: str = "Rent"
    tx_amount: float = 0.0
    tx_type: str = "Expense"
    tx_notes: str = ""


def init_session_state():
    '''
    Initialize the session state with default values for the application.
    This function checks if the session state already contains necessary keys.
    if condition here is to avoid overwriting existing user input values in the session state when the app reruns.

    '''
    defaults = asdict(AppState())
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_next_id(df):
    '''
    Get the next available ID for a new transaction based on the existing DataFrame.
    If the DataFrame is Empty it returns 1, otherwise it returns the maximum existing ID + 1.

    '''
    existing = df["id"].tolist() if not df.empty else []
    return max(existing, default=0) + 1


# ─── SIDEBAR: MANAGE TRANSACTIONS ───────

def render_sidebar():
    """
    Widget for Adding, Deleting and Clearing Transactions from the Expense Tracker.
    This widget is placed in the sidebar of the Streamlit app and allows users to input transaction details,
    delete specific transactions by ID, and clear all inputs. It interacts with the data handling functions
    to load, save, and delete data from the CSV file.
    """
    init_session_state()  # Initialize session state with default values

    # Reset input values BEFORE rendering widgets if clear was requested
    if st.session_state.clear_inputs:
        for key, value in asdict(AppState()).items():
            st.session_state[key] = value
        st.session_state.clear_inputs = False  # Reset the flag after clearing inputs

    categories = ["Rent", "Groceries", "Utilities", "Transport", "Entertainment", "Savings", "Income"]
    tx_types = ["Expense", "Income", "Savings"]

    with st.sidebar:
        # ------- Render Inputs ------ #
        st.header("Transactions")
        selected_date = st.date_input("Date", value=st.session_state.tx_date, key="tx_date")
        category = st.selectbox(
            "Category",
            categories,
            index=categories.index(st.session_state.tx_category),
            key="tx_category"
        )
        amount = st.number_input("Amount (€)", min_value=0.0, step=0.01, value=st.session_state.tx_amount, key="tx_amount")
        tx_type = st.radio("Type", tx_types, index=tx_types.index(st.session_state.tx_type), key="tx_type")
        notes = st.text_input("Notes", value=st.session_state.tx_notes, key="tx_notes")

        # ----- Render Action Buttons ----- #
        add, delete, clear = st.columns(3)

        # --- Add Transaction --- #
        if add.button("Add", icon="➕", width="stretch"):
            # Add a new row to the DataFrame
            df = load_data()
            new_row = {
                "id": get_next_id(df),
                "date": pd.to_datetime(selected_date),
                "category": category,
                "amount": amount,
                "type": tx_type,
                "notes": notes
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            st.toast("Added Successfully!")

        # --- Delete Transaction --- #
        if delete.button("Delete", icon="🗑", width="stretch"):
            # Set the flag to show confirmation
            st.session_state.show_confirm = True

        # Only show if flag is True:
        if st.session_state.show_confirm:
            df = load_data()
            if not df.empty:
                row_id = delete.selectbox("Select Transaction ID", options=df["id"].tolist())
                c1, c2 = delete.columns(2)
                if c1.button("Confirm", type="primary"):
                    df = delete_row(df, row_id)
                    save_data(df)
                    st.session_state.show_confirm = False
                    delete.toast(f"Deleted ID {row_id} successfully!")
                    st.rerun()  # Rerun to refresh the UI and reset the confirmation state
                if c2.button("Cancel"):
                    st.session_state.show_confirm = False
                    st.rerun()
            else:
                delete.warning("No transactions to delete.")
                st.session_state.show_confirm = False

        # --- Clear Inputs --- #
        if clear.button("Clear All", icon="🧹", width="stretch"):
            # Set flag and rerun so values are reset before widgets render
            st.session_state.clear_inputs = True
            st.rerun()
