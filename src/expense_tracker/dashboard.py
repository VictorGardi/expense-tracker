import calendar
from datetime import datetime

import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta

from expense_tracker.expenses import get_expenses
from expense_tracker.login import gatekeeper
from expense_tracker.metric import Metric


def horizontal_bar():
    st.markdown(
        """<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
        unsafe_allow_html=True,
    )


def plot_bars(df: pd.DataFrame) -> None:
    grouped_df = df.groupby("year-month").aggregate(
        {"cost": "sum", "year": "first", "month": "first"}
    )
    grouped_df.sort_values("month", inplace=True)
    fig = plt.figure(figsize=(10, 4))
    sns.barplot(grouped_df, x="month", y="cost", hue="year")
    st.pyplot(fig)


def dashboard():
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title("Expense tracker")
    st.sidebar.markdown("Dashboard")
    df = get_expenses()

    col1, col2 = st.columns(2)
    # Create year selectbox
    chosen_year = col1.selectbox(
        "Choose year of interest", sorted(list(df.year.unique()), reverse=True), index=0
    )

    # Create month selectbox
    months = calendar.month_name[1:]
    chosen_month = col2.selectbox(
        "Choose month of interest",
        months,
        index=int(datetime.today().strftime("%m")) - 1,
    )
    chosen_month_index: int = months.index(chosen_month)
    # Use 15th as day in month since it exists for all months..
    month_as_str = str(chosen_year) + "-" + str(chosen_month_index + 1) + "-15"
    month_as_datetime = datetime.strptime(month_as_str, "%Y-%m-%d")
    previous_month = (month_as_datetime + relativedelta(months=-1)).strftime("%Y-%m")
    metrics_current_month = Metric(
        df[df["year-month"] == month_as_datetime.strftime("%Y-%m")]
    )
    metrics_previous_month = Metric(df[df["year-month"] == previous_month])

    st.markdown(f"**Costs for {months[chosen_month_index]}**")
    categories = sorted(metrics_current_month.data.category.unique())
    n_cols = 2 if len(categories) < 3 else 3
    cols = st.columns(n_cols)
    # define categories that do not contain any data for the current or previous
    # month
    invalid_categories = []
    for i, col in enumerate(cols):
        for category in np.array_split(categories, n_cols)[i]:
            if category == "income":
                continue
            category_cost_current_month = metrics_current_month.get_category_cost(
                category
            )
            category_cost_previous_month = metrics_previous_month.get_category_cost(
                category
            )
            if category_cost_current_month == 0:
                invalid_categories.append(category)
                continue
            col.metric(
                f"{category}",
                int(category_cost_current_month),
                int(category_cost_current_month - category_cost_previous_month),
                delta_color="inverse",
            )
    horizontal_bar()
    cols = st.columns(3)
    with cols[0]:
        st.metric(
            "Total income",
            int(metrics_current_month.income),
            int(metrics_current_month.income - metrics_previous_month.income),
        )

    with cols[1]:
        st.metric(
            "Total expense",
            metrics_current_month.cost,
            int(metrics_current_month.cost - metrics_previous_month.cost),
            delta_color="inverse",
        )
    with cols[2]:
        st.metric(
            "Net expense",
            metrics_current_month.net_expense,
            metrics_current_month.net_expense - metrics_previous_month.net_expense,
            delta_color="inverse",
        )

    horizontal_bar()
    chosen_category = st.selectbox(
        "Choose a specific category", list(set(categories) - set(invalid_categories))
    )
    category_df = df[df.category == chosen_category]
    st.markdown(f"**Detailed expenses for {chosen_category}**")
    cols = st.columns(2)
    with cols[0]:
        st.metric(
            f"Expenses for category {chosen_category} during {chosen_month}",
            int(metrics_current_month.get_category_cost(chosen_category)),
        )
    with cols[1]:
        st.metric(
            f"Avg expense per month spent on {chosen_category}",
            int(
                category_df.groupby("year-month")
                .aggregate({"cost": "sum", "year": "first", "month": "first"})
                .cost.mean()
            ),
        )
    with st.expander("display detailed data"):
        st.dataframe(metrics_current_month.get_category_data(chosen_category))
    st.markdown(f"**Bar plot showing historic expenses for {chosen_category}**")
    plot_bars(category_df)


if __name__ == "__main__":
    gatekeeper(dashboard)
