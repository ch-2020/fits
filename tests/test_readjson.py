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
from data_api.jsonfile_api import *

# Read data from existing report
absolute = abspath("data/report_2024_03.json")
api = JsonFileApi(absolute)
data = api.extract_data()

# Recreate frame
f = Frame(data["frame"]["year"], data["frame"]["month"])

for id, x in data["frame"]["expense_entries"]:
    f.add_expense(EntryCategory.NONRECURR, Entry(x["entry_name"], float(x["entry_value"]), x["entry_type"], x["entry_comment"], x["date_time"]))

for id, x in data["frame"]["recurr_expense_entries"]:
    f.add_expense(EntryCategory.RECURR, Entry(x["entry_name"], float(x["entry_value"]), x["entry_type"], x["entry_comment"], x["date_time"]))

for id, x in data["frame"]["incomes_entries"]:
    f.add_income(EntryCategory.NONRECURR, Entry(x["entry_name"], float(x["entry_value"]), x["entry_type"], x["entry_comment"], x["date_time"]))

for id, x in data["frame"]["recurr_incomes_entries"]:
    f.add_income(EntryCategory.RECURR, Entry(x["entry_name"], float(x["entry_value"]), x["entry_type"], x["entry_comment"], x["date_time"]))

f.add_income(EntryCategory.NONRECURR, Entry("tax return", 200, EntryType.UNF_OTHERS))
print(str(f))

# Create a new report
report = Report(f)
overview = report.generate_report()
pp.pprint(overview)

with open("data/report_2024_03.json", "w") as f:
    json.dump(overview, f)
