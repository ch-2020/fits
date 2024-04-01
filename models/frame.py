from datetime import date
import uuid 

from .entry import *
from .entrytype import *

class Frame:
    def __init__(self, year: str = "", month: str = "") -> None:
        if year == "":
            self.year: str = date.today().year
        else:
            self.year = year
            
        if month == "":
            self.month: str = date.today().month
        else:
            self.month = month

        self.expense_entries = []
        self.recurr_expense_entries = []
        self.incomes_entries = []
        self.recurr_incomes_entries = []
    
    def add_expense(self, expense_type: EntryCategory, expense: Entry, id: str = "") -> str:
        """
        Add expense to the collection
        - expense_type: EntryCategory NONRECURR, RECURR
        - expense: Entry object
        - return: id of the entry
        """
        if id == "":
            id = str(uuid.uuid4())

        if expense_type == EntryCategory.NONRECURR:
            self.expense_entries.append((id, expense))
        elif expense_type == EntryCategory.RECURR:
            self.recurr_expense_entries.append((id, expense))
        else: 
            print(f"Error when adding expense of type: {expense_type}")
        return id

    def add_income(self, income_type: EntryCategory, income: Entry, id: str = "") -> str:
        """
        Add expense to the collection
        - income_type: EntryCategory NONRECURR, RECURR
        - income: Entry object
        - return: id of the entry
        """
        if id == "":
            id = str(uuid.uuid4())
            
        if income_type == EntryCategory.NONRECURR:
            self.incomes_entries.append((id, income))
        elif income_type == EntryCategory.RECURR:
            self.recurr_incomes_entries.append((id, income))
        else: 
            print(f"Error when adding expense of type: {income_type}")
        return id

    def remove_entry(self, id_remove: str) -> None:
        collections = [self.recurr_expense_entries, self.expense_entries, self.recurr_incomes_entries, self.incomes_entries]
        for col in collections:
            for id, obj in enumerate(col):
                if obj[0] == id_remove:
                    col.pop(id)
                    print(f"Removed {id_remove}.")
                    return 0
        print(f"Error: {id_remove} is not found!")

    def export_to_json(self) -> dict:
        current_obj = {
            "year": self.year,
            "month": self.month,
            "recurr_expense_entries": [(id, x.export_to_json()) for id, x in self.recurr_expense_entries],
            "expense_entries": [(id, x.export_to_json()) for id, x in self.expense_entries],
            "recurr_incomes_entries": [(id, x.export_to_json()) for id, x in self.recurr_incomes_entries],
            "incomes_entries": [(id, x.export_to_json()) for id, x in self.incomes_entries]
        }
        return current_obj

    def __str__(self) -> str:
        info = ("------------------------------------------------------\n" + 
                "The frame has the following details:\n" + 
                f"   year: {self.year}\n" +
                f"  month: {self.month}\n" +
                "------------------------------------------------------\n")

        info += "\n* Recurring incomes:\n"
        for ts, ri in self.recurr_incomes_entries:
            info += f"[{ri.date_time}   {ts}] {ri.entry_name} : {ri.entry_value} : {ri.entry_comment}\n"
        
        info += "\n* Variable incomes:\n"
        for ts, ie in self.incomes_entries:
            info += f"[{ie.date_time}   {ts}] {ie.entry_name} : {ie.entry_value} : {ie.entry_comment}\n"

        info += "\n* Recurring expenses:\n"
        for ts, re in self.recurr_expense_entries:
            info += f"[{re.date_time}   {ts}] {re.entry_name} : {re.entry_value} : {re.entry_comment}\n"
        
        info += "\n* Variable expenses:\n"
        for ts, ee in self.expense_entries:
            info += f"[{ee.date_time}   {ts}] {ee.entry_name} : {ee.entry_value} : {ee.entry_comment}\n"

        return info


if __name__ == "__main__":
    f = Frame()
    # Adding entries
    f.add_expense(EntryCategory.NONRECURR, Entry("book", 30.99, EntryType.UNF_EDUCATION))
    f.add_expense(EntryCategory.NONRECURR, Entry("trip", 549.45, EntryType.UNF_TRAVEL))
    f.add_expense(EntryCategory.RECURR, Entry("rent", 800, EntryType.FX_EXPENSE))
    f.add_income(EntryCategory.RECURR, Entry("salary", 3000, EntryType.INC_SALARY))
    f.add_income(EntryCategory.NONRECURR, Entry("bonus", 35, EntryType.INC_PATENT))
    print(str(f))

    # Remove an entry
    income = f.incomes_entries[0]
    print(str(income))
    f.remove_entry(income[0])
    print(str(f))

    # Remove a non-existant entry
    f.remove_entry("asdffgfgfgg")

