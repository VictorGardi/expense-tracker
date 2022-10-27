import os

import numpy as np
import pandas as pd
from splitwise import Splitwise

s = Splitwise(
    consumer_key=os.environ["CONSUMER_KEY"],
    consumer_secret=os.environ["CONSUMER_SECRET"],
    api_key=os.environ["API_KEY"],
)


def get_expenses(start_date, end_date) -> pd.DataFrame:
    expenses = s.getExpenses(
        limit=1000, group_id="34890548", dated_after="2022-05-18T12:19:51.685496"
    )
    expense_descriptions = [i.getDescription() for i in expenses if i.getDeletedAt() is None]
    expense_costs = [float(i.getCost()) for i in expenses if i.getDeletedAt() is None]
    expense_dates = [i.getDate() for i in expenses if i.getDeletedAt() is None]

    df = pd.DataFrame()
    df["description"] = expense_descriptions
    df["cost"] = expense_costs
    df["date"] = expense_dates
    food_words = ["hemköp", "willys", "mat", "coop", "ica"]
    df["description_lowercase"] = df.description.str.lower()
    df["category"] = np.where(
        sum(df.description_lowercase.str.contains(food_word) for food_word in food_words),
        "food",
        "other",
    )
    df["category"] = np.where(
        df.description_lowercase.str.contains("restaurang"), "eat_out", df.category
    )
    df["date"] = pd.to_datetime(df.date, format="%Y-%m-%dT%H:%M:%SZ")
    df["year-month"] = df.date.dt.strftime("%Y-%m")
    return df
