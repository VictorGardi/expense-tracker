import json
import os
from typing import Dict, List

import numpy as np
import pandas as pd
from splitwise import Splitwise

from expense_tracker.db import get_categories


SPLITWISE = Splitwise(
    consumer_key=os.environ["CONSUMER_KEY"],
    consumer_secret=os.environ["CONSUMER_SECRET"],
    api_key=os.environ["API_KEY"],
)


def add_category(df: pd.DataFrame, words: List, category_name: str) -> pd.DataFrame:
    df["category"] = np.where(
        sum(df.description_lowercase.str.contains(word) for word in words),
        category_name,
        df.category,
    )
    return df


def read_json(path_to_file: str) -> Dict:
    with open(path_to_file) as f:
        data = json.load(f)
    return data


def prepare_data(data) -> pd.DataFrame:
    expense_descriptions = [
        i.getDescription() for i in data if i.getDeletedAt() is None
    ]
    expense_costs = [float(i.getCost()) for i in data if i.getDeletedAt() is None]
    expense_dates = [i.getDate() for i in data if i.getDeletedAt() is None]

    df = pd.DataFrame()
    df["description"] = expense_descriptions
    df["cost"] = expense_costs
    df["date"] = expense_dates
    df["description_lowercase"] = df.description.str.lower()
    df["category"] = "other"
    df.drop(df[df.description == "Payment"].index, inplace=True)
    df["date"] = pd.to_datetime(df.date, format="%Y-%m-%dT%H:%M:%SZ")
    df["year-month"] = df.date.dt.strftime("%Y-%m")
    df["year"] = df.date.dt.strftime("%Y")
    df["month"] = df.date.dt.strftime("%m")
    return df


def get_expenses() -> pd.DataFrame:
    expenses = SPLITWISE.getExpenses(
        limit=1000, group_id="34890548", dated_after="2022-05-18T12:19:51.685496"
    )
    df = prepare_data(expenses)
    for category, tags in get_categories().items():
        df = add_category(df, tags, category)
    return df
