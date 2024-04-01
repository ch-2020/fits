import os, sys
import unittest
import pprint as pp

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

from models.frame import *
from models.report import *

class TestCases(unittest.TestCase):
    def test_frame(self):
        f = Frame()
        f.add_expense(EntryCategory.NONRECURR, Entry("book", 30.99, EntryType.UNF_EDUCATION))
        f.add_expense(EntryCategory.RECURR, Entry("rent", 800, EntryType.FX_EXPENSE))
        f.add_income(EntryCategory.RECURR, Entry("salary", 3000, EntryType.INC_SALARY))
        f.add_income(EntryCategory.NONRECURR, Entry("bonus", 35, EntryType.INC_PATENT))

        self.assertEqual(len(f.incomes_entries), 1)
        self.assertEqual(len(f.recurr_incomes_entries), 1)
        self.assertEqual(len(f.expense_entries), 1)
        self.assertEqual(len(f.recurr_expense_entries), 1)

    def test_report(self):
        f = Frame()
        f.add_expense(EntryCategory.NONRECURR, Entry("book", 30.99, EntryType.UNF_EDUCATION))
        f.add_expense(EntryCategory.RECURR, Entry("rent", 800, EntryType.FX_EXPENSE))
        f.add_income(EntryCategory.RECURR, Entry("salary", 3000, EntryType.INC_SALARY))
        f.add_income(EntryCategory.NONRECURR, Entry("bonus", 35, EntryType.INC_PATENT))

        report = Report(f)
        overview = report.generate_report()
        result = {'year': 2024, 'month': 3, 'date_updated': '2024-03-14', 'overview': {'total_income': '3035.00', 'total_expense': '830.99', 'total_savings': '2204.01'}, 'expense_by_category': {'EntryType.FX_EXPENSE': 800.0, 'EntryType.UNF_EDUCATION': 30.99}, 'analysis': {'percentage_overview': {'expense': '27.38', 'savings': '72.62'}, 'percentage_expense_by_category': {'EntryType.FX_EXPENSE': '96.27', 'EntryType.UNF_EDUCATION': '3.73'}}, 'data': {'incomes_list': [{'date': '2024-03-14', 'name': 'salary', 'value': '3000.00'}, {'date': '2024-03-14', 'name': 'bonus', 'value': '35.00'}], 'expense_list': [{'date': '2024-03-14', 'name': 'rent', 'value': '800.00'}, {'date': '2024-03-14', 'name': 'book', 'value': '30.99'}]}}
        self.assertEqual(overview, result)

if __name__ == '__main__':
    unittest.main()



    
