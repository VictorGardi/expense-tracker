import calendar
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
from dateutil.relativedelta import relativedelta

from expense_tracker.expenses import get_expenses
from expense_tracker.login import gatekeeper


def get_cost_per_category(df: pd.DataFrame, category: str) -> float:
    return df[df.category == category].cost.sum()


def dashboard():
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title("Expense tracker")
    st.sidebar.markdown("Dashboard")
    col1, col2 = st.columns(2)
    # Create year selectbox
    chosen_year = col1.selectbox(
        "Choose year of interest", ["2022", "2023", "2024"], index=2
    )

    # Create month selectbox
    months = calendar.month_name[1:]
    current_month = int(datetime.today().strftime("%m")) - 1
    chosen_month: str = col2.selectbox(
        "Choose month of interest", months, index=current_month
    )
    chosen_month_index: int = months.index(chosen_month)
    # Use 15th as day in month since it exists for all months..
    month_as_str = chosen_year + "-" + str(chosen_month_index + 1) + "-15"
    month_as_datetime = datetime.strptime(month_as_str, "%Y-%m-%d")
    previous_month = (month_as_datetime + relativedelta(months=-1)).strftime("%Y-%m")
    # TODO: add date input and choose only data from current and previous month..
    df = get_expenses()

    df_current_month = df[df["year-month"] == month_as_datetime.strftime("%Y-%m")]
    df_previous_month = df[df["year-month"] == previous_month]
    income_current_month = df_current_month[
        df_current_month.category == "income"
    ].cost.sum()
    income_previous_month = df_previous_month[
        df_previous_month.category == "income"
    ].cost.sum()
    cost_current_month = int(df_current_month.cost.sum() - income_current_month)
    cost_previous_month = int(df_previous_month.cost.sum() - income_previous_month)
    net_expense_current_month = int(cost_current_month - income_current_month)
    net_expense_previous_month = int(cost_previous_month - income_previous_month)

    st.markdown(f"**Costs for {months[chosen_month_index]}**")
    categories = sorted(df_current_month.category.unique())
    n_cols = 2 if len(categories) < 3 else 3
    cols = st.columns(n_cols)
    # define categories that do not contain any data for the current or previous
    # month
    invalid_categories = []
    for i, col in enumerate(cols):
        for category in np.array_split(categories, n_cols)[i]:
            if category == "income":
                continue
            category_cost_current_month = get_cost_per_category(
                df_current_month, category=category
            )
            category_cost_previous_month = get_cost_per_category(
                df_previous_month, category=category
            )
            if category_cost_current_month == 0:
                invalid_categories.append(category)
            if category_cost_current_month == 0 and category_cost_previous_month == 0:
                invalid_categories.append(category)
                continue
            col.metric(
                f"{category}",
                int(category_cost_current_month),
                int(category_cost_current_month - category_cost_previous_month),
                delta_color="inverse",
            )
    st.markdown(
        """<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
        unsafe_allow_html=True,
    )
    cols = st.columns(3)
    with cols[0]:
        st.metric(
            "Total income",
            int(income_current_month),
            int(income_current_month - income_previous_month),
        )

    with cols[1]:
        st.metric(
            "Total expense",
            cost_current_month,
            int(cost_current_month - cost_previous_month),
            delta_color="inverse",
        )
    with cols[2]:
        st.metric(
            "Net expense",
            net_expense_current_month,
            net_expense_current_month - net_expense_previous_month,
            delta_color="inverse",
        )

    st.markdown("**Detailed expenses in specific category**")
    chosen_category = st.selectbox(
        "Choose a specific category", list(set(categories) - set(invalid_categories))
    )
    st.dataframe(df_current_month[df.category == chosen_category])


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


if __name__ == "__main__":
    gatekeeper(dashboard)
