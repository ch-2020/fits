"""
Import relevant packages
"""
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from projection_data import ProjectionData
    from monthtype import Month
else: 
    from .projection_data import ProjectionData
    from .monthtype import Month

class Projection:
    """
    Projection class to forecast further finances
    """
    def __init__(self, projection_name: str) -> None:
        self.projection_name = projection_name
        self.projections = []

    def add_new_projection_data(self, projectiondata: ProjectionData):
        """
        Add new data into the list
        """
        self.projections.append(projectiondata)

    def extract_income_for_viz(self):
        """
        Extract the total incomes from each entry and export it as list
        """
        incmonths = []
        incdata = []
        for proj in self.projections:
            incmonths.append(proj.month.name)
            incdata.append(proj.total_income)
        return incmonths, incdata
    
    def extract_expense_for_viz(self):
        """
        Extract the total expenses from each entry and export it as list
        """
        expmonths = []
        expdata = []
        for proj in self.projections:
            expmonths.append(proj.month.name)
            expdata.append(proj.total_expense)
        return expmonths, expdata

    def get_projection_in_dict(self) -> dict:
        """
        Get projection in dict format
        """
        projlist = [x.export_to_json() for x in self.projections]
        output = {
            "projection_name": self.projection_name,
            "projections": projlist
        }
        return output

    def _sort_data(self) -> None:
        """
        Sort or merge data according to month for visualization
        """
    
if __name__ == "__main__":
    p = Projection("Financial forecast 2024")

    d1 = ProjectionData("2024", Month.JAN)
    d1.add_item("income", "salary", 500)
    d1.add_item("income", "interest", 10)
    d1.add_item("expense", "living", 200.50)

    print(d1.month.name)
    print(f"Income: {d1.total_income}, Expense: {d1.total_expense}")
    for d in d1.income:
        print(d)

    d2 = ProjectionData("2024", Month.APR)
    d2.add_item("income", "salary", 500)
    d2.add_item("income", "interest", 40)
    d2.add_item("expense", "living", 350.50)
    d2.add_item("expense", "travel", 200)

    p.add_new_projection_data(d1)
    p.add_new_projection_data(d2)

    inc_months, inc_data = p.extract_income_for_viz()
    print(inc_months)
    print(inc_data)
    exp_months, exp_data = p.extract_expense_for_viz()
    print(exp_months)
    print(exp_data)
