import os, sys
from os.path import abspath
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

from data_api.textfile_api import *

absolute = abspath("data/recurr_entries.txt")

api = TextFileApi(absolute)
print(f"Expense: {api.get_recc_expense()}")
print(f"Income: {api.get_recc_incomes()}")