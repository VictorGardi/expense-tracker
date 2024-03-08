import pandas as pd


class Metric:
    def __init__(self, data: pd.DataFrame, **kwargs) -> None:
        self.data = data
        self.income_category = kwargs.get("income_category", "income")
        self.n_decimals = kwargs.get("n_decimals", 0)

    @property
    def cost(self) -> float:
        return round(
            self.data.query(f"category != '{self.income_category}'").cost.sum(),
            self.n_decimals,
        )

    @property
    def income(self) -> float:
        return round(
            self.data.query(f"category == '{self.income_category}'").cost.sum()
        )

    @property
    def net_expense(self) -> float:
        return round(self.cost - self.income, self.n_decimals)

    def get_category_cost(self, category: str) -> float:
        return self.get_category_data(category).cost.sum()

    def get_category_data(self, category: str) -> pd.DataFrame:
        return self.data.query(f'category == "{category}"')
