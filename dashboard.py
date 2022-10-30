import calendar
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
    col1, col2 = st.columns(2)
    # Create year selectbox
    chosen_year = col1.selectbox("Choose year of interest", ["2022", "2023", "2024"], index=0)

    # Create month selectbox
    months = calendar.month_name[1:]
    current_month = int(datetime.today().strftime("%m")) - 1
    chosen_month: str = col2.selectbox("Choose month of interest", months, index=current_month)
    chosen_month_index: int = months.index(chosen_month)
    # Use 15th as day in month since it exists for all months..
    month_as_str = chosen_year + "-" + str(chosen_month_index + 1) + "-15"
    month_as_datetime = datetime.strptime(month_as_str, "%Y-%m-%d")
    previous_month = (month_as_datetime + relativedelta(months=-1)).strftime("%Y-%m")
    # TODO: add date input and choose only data from current and previous month..
    df = get_expenses(1, 2)
    df_current_month = df[df["year-month"] == month_as_datetime.strftime("%Y-%m")]
    df_previous_month = df[df["year-month"] == previous_month]

    st.markdown(f"**Costs for {months[chosen_month_index]}**")
    cols = st.columns(len(df.category.unique()))
    for i, category in enumerate(sorted(df.category.unique())):
        col = cols[i]
        category_cost_current_month = get_cost_per_category(df_current_month, category=category)
        category_cost_previous_month = get_cost_per_category(df_previous_month, category=category)
        if category_cost_current_month == 0 and category_cost_previous_month == 0:
            continue
        col.metric(
            f"{category} costs",
            category_cost_current_month,
            (category_cost_current_month - category_cost_previous_month),
        )


if __name__ == "__main__":
    gatekeeper(dashboard)
