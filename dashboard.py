from datetime import datetime

import pandas as pd
import streamlit as st
from dateutil.relativedelta import relativedelta

from expenses import get_expenses
from gatekeeper import gatekeeper


def get_cost_per_category(df: pd.DataFrame, category: str) -> float:
    return df[df.category == category].cost.sum()


def dashboard():
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title("Expense tracker")
    st.sidebar.markdown("Dashboard")
    df = get_expenses(1, 2)
    today = datetime.today()
    current_month = today.strftime("%Y-%m")
    previous_month = (today + relativedelta(months=-1)).strftime("%Y-%m")
    df_current_month = df[df["year-month"] == current_month]
    df_previous_month = df[df["year-month"] == previous_month]
    food_cost_current_month = get_cost_per_category(df_current_month, category="food")
    other_cost_current_month = get_cost_per_category(df_current_month, category="other")
    food_cost_previous_month = get_cost_per_category(df_previous_month, category="food")
    other_cost_previous_month = get_cost_per_category(df_previous_month, category="other")
    col1, col2 = st.columns(2)
    col1.metric(
        f"Food cost for {today.strftime('%B')}",
        food_cost_current_month,
        (food_cost_current_month - food_cost_previous_month),
    )
    col2.metric(
        f"Other costs for {today.strftime('%B')}",
        other_cost_current_month,
        (other_cost_current_month - other_cost_previous_month),
    )


if __name__ == "__main__":
    gatekeeper(dashboard)
