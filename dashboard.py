from datetime import datetime

import pandas as pd
import streamlit as st
from dateutil.relativedelta import relativedelta

from expenses import get_expenses
from login import gatekeeper


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

    cols = st.columns(len(df.category.unique()))
    for i, category in enumerate(df.category.unique()):
        col = cols[i]
        category_cost_current_month = get_cost_per_category(df_current_month, category=category)
        category_cost_previous_month = get_cost_per_category(df_previous_month, category=category)
        col.metric(
            f"{category} cost for {today.strftime('%B')}",
            category_cost_current_month,
            (category_cost_current_month - category_cost_previous_month),
        )


if __name__ == "__main__":
    gatekeeper(dashboard)
