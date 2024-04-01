import os, sys
from os.path import abspath
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

import pprint as pp
import json

from models.entry import *
from models.entrytype import *
from models.frame import *
from models.report import *
from data_api.textfile_api import *

# Read data from recurring file
absolute = abspath("data/recurr_entries.txt")
api = TextFileApi(absolute)
recurr_incomes = api.get_recc_incomes()
recurr_expense = api.get_recc_expense()

# Create Frame object and update recurring data
current_frame = Frame()
for typ, nam, val in recurr_incomes:
    current_frame.add_income(EntryCategory.RECURR, Entry(nam, float(val), EntryType[typ]))

for typ, nam, val in recurr_expense:
    current_frame.add_expense(EntryCategory.RECURR, Entry(nam, float(val), EntryType[typ]))

# Add additional entries to the frame
e1 = current_frame.add_expense(EntryCategory.NONRECURR, Entry("book", 24, EntryType.UNF_EDUCATION))
e2 = current_frame.add_expense(EntryCategory.NONRECURR, Entry("food", 350, EntryType.FX_FOOD))
e3 = current_frame.add_expense(EntryCategory.NONRECURR, Entry("transport", 50, EntryType.FX_EXPENSE))
e4 = current_frame.add_expense(EntryCategory.NONRECURR, Entry("daily items", 150, EntryType.FX_DAILY))
print(str(current_frame))

# Create a report at the end
report = Report(current_frame)
overview = report.generate_report()
print(str(report))

with open("data/report_2024_03.json", "w") as f:
    json.dump(overview, f)
