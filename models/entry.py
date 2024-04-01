from enum import Enum
from datetime import date

from .entrytype import EntryType

class Entry:
    """
    Represent a single entry
    - name: name of the entry
    - value: the expense or income of the entry
    - type: type of entry based on EntryType enum
    - comment: (optional) comment given to the entry
    """
    def __init__(self, name: str, value: float, type: EntryType, comment: str = "", input_date: str = "") -> None:
        try:
            self.date_time = str(date.today())
            if input_date != "": 
                self.date_time = input_date
            self.entry_name = name
            self.entry_value = format(value, '.2f')
            self.entry_currency = "€"
            self.entry_type = type
            self.entry_comment = comment
        except Exception as e:
            print("Error when creating entry: " + str(e))
    
    def export_to_json(self) -> dict:
        result = {
            "date_time": self.date_time,
            "entry_name": self.entry_name,
            "entry_value": self.entry_value,
            "entry_currency": self.entry_currency,
            "entry_type": str(self.entry_type),
            "entry_comment": self.entry_comment
        }
        return result

    def __str__(self):
        if self.entry_comment == "":
            return f"[{self.entry_type}] The entry {self.entry_name} ({self.entry_value} {self.entry_currency}) was created on the {self.date_time}."
        else:
            return f"[{self.entry_type}] The entry {self.entry_name} ({self.entry_value} {self.entry_currency}) was created on the {self.date_time}.\n  -- Comment: {self.entry_comment}"

    def __repr__(self):
        return f"Entry(\'{self.date_time}\', \'{self.entry_name}\', {self.entry_value}, \'{self.entry_type}\', \'{self.entry_comment}\'"

if __name__ == "__main__":
    a = Entry("restaurant", 3.555, EntryType.FX_FOOD, "Outing with friends")
    print(str(a))
    print(repr(a))
