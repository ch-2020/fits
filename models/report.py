from datetime import date
import pprint as pp

from .frame import *

class Report:
    """Class to generate report from frame"""
    def __init__(self, frame: Frame) -> None:
        self.input_frame = frame

        self.year = self.input_frame.year
        self.month = self.input_frame.month
        self.date_updated = str(date.today())

        self.total_income: float = 0
        self.data_incomes_list = []

        self.total_expense: float = 0
        self.data_expense_list = []
        self.total_expense_by_category = {}
        self.percentage_expense_by_category = {}
        
        self.total_savings: float = 0
        self.percentage_expense_savings = {}

    def generate_report(self) -> dict:
        """
        Generate report based on the existing data
        """
        # incomes
        self.total_income = 0
        self.data_incomes_list = []
        income_list = self.input_frame.recurr_incomes_entries + self.input_frame.incomes_entries
        for _, entry in income_list:
            data = {
                "date": str(entry.date_time),
                "name": entry.entry_name,
                "value": entry.entry_value
            }
            self.total_income += float(entry.entry_value)
            self.data_incomes_list.append(data)

        # expenses
        self.total_expense = 0
        self.data_expense_list = []
        expense_list = self.input_frame.recurr_expense_entries + self.input_frame.expense_entries
        for _, exp in expense_list:
            data = {
                "date": str(exp.date_time),
                "name": exp.entry_name,
                "value": exp.entry_value
            }
            self.total_expense += float(exp.entry_value)
            self.data_expense_list.append(data)

            if str(exp.entry_type) not in self.total_expense_by_category.keys():
                self.total_expense_by_category[str(exp.entry_type)] = 0
                self.percentage_expense_by_category[str(exp.entry_type)] = 0
            self.total_expense_by_category[str(exp.entry_type)] += float(exp.entry_value)

        for k in self.total_expense_by_category.keys():
            self.percentage_expense_by_category[k] = format(self.total_expense_by_category[k] / self.total_expense * 100, ".2f")

        # Analysis
        self.total_savings = 0
        self.total_savings = format(self.total_income - self.total_expense, ".2f")

        if self.total_income != 0:
            per_expense = format(self.total_expense / self.total_income * 100, ".2f")
            per_saving = format(float(self.total_savings) / float(self.total_income) * 100, ".2f")
            self.percentage_expense_savings = {
                "expense": per_expense,
                "savings": per_saving
            }

        return self.get_report_in_dict()

    def get_report_in_dict(self) -> dict:
        """
        Return report in dict format
        """
        report = {
            "year": self.year,
            "month": self.month,
            "date_updated": self.date_updated,
            "overview": {
                "total_income": format(self.total_income, ".2f"),
                "total_expense": format(self.total_expense, ".2f"),
                "total_savings": format(float(self.total_savings), ".2f")
            },
            "expense_by_category": self.total_expense_by_category,
            "analysis": {
                "percentage_overview": self.percentage_expense_savings,
                "percentage_expense_by_category": self.percentage_expense_by_category
            },
            "data": {
                "incomes_list": self.data_incomes_list,
                "expense_list": self.data_expense_list
            },
            "frame": self.input_frame.export_to_json()
        }
        return report

    def __str__(self) -> str:
        info = ("------------------------------------------------------\n" + 
                "Generated report:\n" + 
                f"   year: {self.year}\n" +
                f"  month: {self.month}\n" +
                f"updated: {self.date_updated}\n" +
                "------------------------------------------------------\n")
        info += f"*** total_income: {self.total_income}\n"
        info += f"*** total_expense: {self.total_expense}\n"
        info += f"*** total_savings: {self.total_savings}\n"
        info += f"*** percentage_overview: {self.percentage_expense_savings}\n\n"
        info += f"expense_by_category: {self.total_expense_by_category}\n"
        info += f"percentage_expense_by_category: {self.percentage_expense_by_category}\n"

        return info
