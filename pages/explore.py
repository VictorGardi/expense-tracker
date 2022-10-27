import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from expenses import get_expenses
from gatekeeper import gatekeeper


def explore_expenses():
    st.sidebar.markdown("Explore expenses")
    expenses_df = get_expenses(1, 2)
    st.dataframe(expenses_df)
    fig = plt.figure(figsize=(10, 4))
    sns.lineplot(
        data=expenses_df,
        x="date",
        y="cost",
        hue="category",
        style="category",
        markers=True,
        dashes=False,
    )
    st.pyplot(fig)


if __name__ == "__main__":
    gatekeeper(explore_expenses)
