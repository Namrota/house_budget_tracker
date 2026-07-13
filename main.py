import streamlit as st
import pandas as pd
from datetime import datetime
from data_handling import load_data
from widgets import render_sidebar

# ─── CONFIG ─────────────────────────
st.set_page_config(page_title="Household Tracker", layout="wide")

# ─── SIDEBAR ────────────────────────
render_sidebar()

# ─── MAIN DASHBOARD ─────────────────
st.title("🏠 Household Expense & Savings Tracker")

df = load_data()

if not df.empty:
    # KPIs
    total_income = df[df["type"] == "Income"]["amount"].sum()
    total_expenses = df[df["type"] == "Expense"]["amount"].sum()
    total_savings = df[df["type"] == "Savings"]["amount"].sum()
    balance = total_income - total_expenses - total_savings
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Income", f"€{total_income:,.2f}")
    col2.metric("Expenses", f"€{total_expenses:,.2f}")
    col3.metric("Savings", f"€{total_savings:,.2f}")
    col4.metric("Balance", f"€{balance:,.2f}")
    
    # Monthly trend
    st.subheader("Monthly Trend")
    df["month"] = df["date"].dt.to_period("M")
    monthly = df.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0)
    st.bar_chart(monthly)
    
    # Category breakdown
    st.subheader("By Category")
    cat_data = df[df["type"] == "Expense"].groupby("category")["amount"].sum()
    st.bar_chart(cat_data)
    
    # Savings goal
    st.subheader("Savings Goal")
    goal = st.number_input("Monthly Savings Goal (€)", value=500.0)
    progress = min(total_savings / goal, 1.0) if goal > 0 else 0
    st.progress(progress, text=f"{progress*100:.1f}% of goal")
    
    # Raw data
    st.subheader("Recent Transactions")
    st.dataframe(df.sort_values("date", ascending=False).head(20))
    
    # Download
    st.download_button("Download CSV", df.to_csv(index=False), "expenses.csv")
else:
    st.info("No transactions yet. Add one in the sidebar!")
