import sys
from pathlib import Path
from dataclasses import dataclass

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from monthtype import Month
else:
    from .monthtype import Month

@dataclass
class ProjectionData:
    """
    Object class to describe projection data
    """
    year: str
    month: Month
    income: list[set()]
    expense: list[set()]
    total_income: float
    total_expense: float

    def __init__(self, year: str, month: Month) -> None:
        self.year = year
        self.month = month.name
        self.total_income = 0
        self.total_expense = 0
        self.income = []
        self.expense = []

    def add_item(self, itemtype: str, itemname: str, itemvalue: float):
        """
        itemtype: "income", "expense"
        """
        if itemtype not in ["income", "expense"]:
            print("itemtype not correct (options: income, expense)")
            print("Item not saved!")
        else:
            if itemtype == "income":
                self.income.append((itemname, itemvalue))
                self.total_income += itemvalue
            elif itemtype == "expense":
                self.expense.append((itemname, itemvalue))
                self.total_expense += itemvalue

    def export_to_json(self) -> dict:
        """
        export data to json
        """
        current_obj = {
            "year": self.year,
            "month": self.month,
            "total_income": self.total_income,
            "total_expense": self.total_expense,
            "income": [(id, x) for id, x in self.income],
            "expense": [(id, x) for id, x in self.expense]
        }
        return current_obj