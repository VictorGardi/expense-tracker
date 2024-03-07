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


def get_cost_per_category(df: pd.DataFrame, category: str) -> float:
    return df[df.category == category].cost.sum()


def plot_bars(df: pd.DataFrame) -> None:
    grouped_df = df.groupby("year-month").aggregate(
        {"cost": "sum", "year": "first", "month": "first"}
    )
    grouped_df.sort_values("month", inplace=True)
    fig = plt.figure(figsize=(10, 4))
    sns.barplot(grouped_df, x="month", y="cost", hue="year")
    st.pyplot(fig)


def get_cost(cost: pd.Series, income: float) -> int:
    return int(cost.sum() - income)


def get_income(df: pd.DataFrame) -> float:
    return df[df.category == "income"].cost.sum()


def generate_metrics(df: pd.DataFrame, current_month: str, previous_month: str) -> dict:
    metrics = {"current_month": {}, "previous_month": {}}
    metrics["current_month"]["data"] = df[df["year-month"] == current_month]
    metrics["previous_month"]["data"] = df[df["year-month"] == previous_month]
    for month in metrics.keys():
        temp_df = metrics[month]["data"]
        metrics[month]["income"] = get_income(temp_df)
        metrics[month]["cost"] = get_cost(temp_df.cost, metrics[month]["income"])
        metrics[month]["net_expense"] = int(
            metrics[month]["cost"] - metrics[month]["income"]
        )
    return metrics


def dashboard():
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title("Expense tracker")
    st.sidebar.markdown("Dashboard")
    df = get_expenses()
    plot_bars(df[df.category != "income"])

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
    metrics = generate_metrics(df, month_as_datetime.strftime("%Y-%m"), previous_month)

    st.markdown(f"**Costs for {months[chosen_month_index]}**")
    categories = sorted(metrics["current_month"]["data"].category.unique())
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
                metrics["current_month"]["data"], category=category
            )
            category_cost_previous_month = get_cost_per_category(
                metrics["previous_month"]["data"], category=category
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
            int(metrics["current_month"]["income"]),
            int(
                metrics["current_month"]["income"] - metrics["previous_month"]["income"]
            ),
        )

    with cols[1]:
        st.metric(
            "Total expense",
            metrics["current_month"]["cost"],
            int(metrics["current_month"]["cost"] - metrics["previous_month"]["cost"]),
            delta_color="inverse",
        )
    with cols[2]:
        st.metric(
            "Net expense",
            metrics["current_month"]["net_expense"],
            metrics["current_month"]["net_expense"]
            - metrics["previous_month"]["net_expense"],
            delta_color="inverse",
        )

    chosen_category = st.selectbox(
        "Choose a specific category", list(set(categories) - set(invalid_categories))
    )
    category_df = df[df.category == chosen_category]
    st.markdown(f"**Detailed expenses for {chosen_category}**")
    cols = st.columns(2)
    with cols[0]:
        st.metric(
            f"Expenses for category {chosen_category} during {chosen_month}",
            int(
                metrics["current_month"]["data"]
                .query(f'category == "{chosen_category}"')
                .cost.sum()
            ),
        )
    with cols[1]:
        st.metric(
            f"Mean expense per month for category: {chosen_category}",
            int(
                category_df.groupby("year-month")
                .aggregate({"cost": "sum", "year": "first", "month": "first"})
                .cost.mean()
            ),
        )
    st.dataframe(
        metrics["current_month"]["data"][
            metrics["current_month"]["data"].category == chosen_category
        ]
    )
    st.markdown(f"**Bar plot showing historic expenses for {chosen_category}**")
    plot_bars(category_df)


if __name__ == "__main__":
    gatekeeper(dashboard)
