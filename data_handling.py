import os
import pandas as pd

# ─── DATA PERSISTENCE ───────────────
DATA_FILE = "expenses.csv"

'''
Load data into CSV file if it exists, otherwise create an empty DataFrame with the required columns:

'''
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        # Robustly parse date column in case CSV has mixed formats
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        return df
    return pd.DataFrame(columns=["id", "date", "category", "amount", "type", "notes"])

'''
Save the DataFrame into CSV file:
'''
def save_data(df):
    df.to_csv(DATA_FILE, index=False)


def delete_row(df, row_id):
    """
    Returns a new DataFrame with the matching row removed.
    Does NOT modify the original df (pandas best practice).
    """
    return df[df["id"] != row_id]
