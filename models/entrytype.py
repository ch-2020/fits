from enum import Enum, auto

class EntryType(Enum):
    FX_FOOD = auto()
    FX_DAILY = auto()
    FX_EXPENSE = auto()
    UNF_TRAVEL = auto()
    UNF_ENTERT = auto()
    UNF_EDUCATION = auto()
    UNF_OTHERS = auto()
    INC_SALARY = auto()
    INC_PATENT = auto()
    INC_INVESTMENT = auto()
    INC_INTEREST = auto()
    INC_BONUS = auto()
    INC_GIFT = auto()

class EntryCategory(Enum):
    NONRECURR = auto()
    RECURR = auto()
    