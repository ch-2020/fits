"""Module"""
from datetime import date
import os
import sys
import json

from os.path import abspath
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

from models.entry import *
from models.entrytype import *
from models.frame import *
from models.report import *
from data_api.jsonfile_api import *
from data_api.textfile_api import *

def check_or_create_jsonfile(dirpath: str, name: str) -> tuple[str, bool]:
    """
    Function to check whether the json file exists
    if not existed, create a new json file
    dirpath: str
    name: str
    return: success (bool)
    """
    file_exist = False
    absolute = dirpath + "/" + name
    if os.path.isfile(absolute):
        file_exist = True
    else:
        open(absolute, "w", encoding="utf-8").close()
        print(f"A new json file is created: {absolute}")
    return (absolute, file_exist)

def get_user_inputs() -> tuple[str, str]:
    """
    Function to get user input
    inputs: -
    return: year (str), month (str)
    """
    currentyear: str = ""
    currentmonth: str = ""
    print("-------------------------------")

    inputyear = input("Select the year you wish to update YYYY (Enter if current year is requested): ")
    if inputyear == "":
        currentyear = date.today().year
    else:
        currentyear = inputyear

    inputmonth = input("Select the month you wish to update M (Enter if current month is requested): ")
    if inputmonth == "":
        currentmonth = date.today().month
    else:
        currentmonth = inputmonth

    confirmed = input(f"You have selected {currentyear}-{currentmonth}. Is this correct? (Y/N)?")
    print("-------------------------------")

    if confirmed in ["Y", "y", ""]:
        return (currentyear, currentmonth)
    else:
        return get_user_inputs()

def read_json_file(file_path_absolute) -> json:
    """
    Function to get json data from an absolute filepath
    filepath: str
    return: data (json)
    """
    extracted_data = {}
    try:
        api = JsonFileApi(filepath)
        extracted_data = api.extract_data()
        return extracted_data
    except Exception as err:
        print(f"Error when reading {file_path_absolute}: {err}!")
        return extracted_data

def read_recurr_entries(abs_file_path: str):
    """
    Function to read recurring entries from text file
    file_path: str
    return: recurr_entries 
    """
    api = TextFileApi(abs_file_path)
    recurr_incomes = api.get_recc_incomes()
    recurr_expense = api.get_recc_expense()
    return recurr_incomes, recurr_expense

def get_existed_frame(data_input: json) -> Frame:
    """
    Function to create a frame from a json data string
    data_input: json
    return: Frame
    """
    extracted_fr = Frame(data_input["frame"]["year"], data_input["frame"]["month"])
    for uni_id, ex_d in data_input["frame"]["expense_entries"]:
        extracted_fr.add_expense(EntryCategory.NONRECURR, Entry(ex_d["entry_name"], float(ex_d["entry_value"]), ex_d["entry_type"], ex_d["entry_comment"], ex_d["date_time"]), uni_id)

    for uni_id, ex_d in data_input["frame"]["recurr_expense_entries"]:
        extracted_fr.add_expense(EntryCategory.RECURR, Entry(ex_d["entry_name"], float(ex_d["entry_value"]), ex_d["entry_type"], ex_d["entry_comment"], ex_d["date_time"]), uni_id)

    for uni_id, in_d in data_input["frame"]["incomes_entries"]:
        extracted_fr.add_income(EntryCategory.NONRECURR, Entry(in_d["entry_name"], float(in_d["entry_value"]), in_d["entry_type"], in_d["entry_comment"], in_d["date_time"]), uni_id)

    for uni_id, in_d in data_input["frame"]["recurr_incomes_entries"]:
        extracted_fr.add_income(EntryCategory.RECURR, Entry(in_d["entry_name"], float(in_d["entry_value"]), in_d["entry_type"], in_d["entry_comment"], in_d["date_time"]), uni_id)
    return extracted_fr

def generate_report(input_frame: Frame) -> json:
    """
    Function to generate a report based on the current frame
    input_frame: Frame
    return: report (json)
    """
    report = Report(input_frame)
    overview = report.generate_report()
    return overview

def save_result(file_path: str, report_res: json):
    """
    Function to save result to json file
    file_path: str
    report_res: json
    return: success (bool)
    """
    try:
        with open(file_path, "w") as file:
            json.dump(report_res, file)
        return True
    except Exception as err:
        print(f"Error when saving file: {err}")
        return False

def generate_user_prompt():
    """
    Function to get inputs from user
    """
    name = ""
    while name == "":
        name = input("Key in your entry name: ")

    value = None
    while True:
        try:
            value = float(input("Key in your entry value: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid float value.")

    entrytype = ""
    while True:
        print("Key in your entry type: ")
        for en in EntryType:
            print(f"        {en}: {en.value}")
        entrytypeinput = int(input())
        for typ in EntryType:
            if typ.value == entrytypeinput:
                entrytype = typ
                break
        if entrytype != "":
            break
        else:
            print("Entry type not valid!")

    comment = input("Key in your comment:")
    print(f"Entry {name} ({value}): {entrytype} (comment: {comment})")
    return name, value, entrytype, comment

def print_report(report_over: dict, rep_frame: Frame) -> None:
    """
    Prompt to visualize report result
    """
    yr = report_over["year"]
    mo = report_over["month"]
    inc = report_over["overview"]["total_income"]
    exp = report_over["overview"]["total_expense"]
    sav = report_over["overview"]["total_savings"]

    try:
        exp_per = report_over["analysis"]["percentage_overview"]["expense"]
    except Exception:
        exp_per = "NIL"

    try:
        sav_per = report_over["analysis"]["percentage_overview"]["savings"]
    except Exception:
        sav_per = "NIL"

    print(f"Report for {yr} month {mo}")
    print(f"Total income    : {inc}")
    print(f"Total expense   : {exp} ({exp_per})")
    print(f"Total savings   : {sav} ({sav_per})")
    print(str(rep_frame))

if __name__ == "__main__":
    os.system("clear")

    # ----------------------------------
    #   Prompt for year and month
    # ----------------------------------
    year, month = get_user_inputs()
    filename = f"report_{year}_{month}.json"
    filepath, file_existed = check_or_create_jsonfile(abspath("userdata/monthlyreports"), filename)

    extracted_frame = {}
    if file_existed:
        # extract data and update the frame
        data = read_json_file(filepath)
        if data != {}:
            extracted_frame = get_existed_frame(data)

    else:
        # create a new frame for the first time
        extracted_frame = Frame(year, month)
        print(f"New frame created: {extracted_frame}")

        # add in recurr entries
        recurr_file = abspath("userdata/recurrdata/recurr_entries.txt")
        recurr_inc, recurr_exp = read_recurr_entries(recurr_file)

        # Create Frame object and update recurring data
        for typ, nam, val in recurr_inc:
            extracted_frame.add_income(EntryCategory.RECURR, Entry(nam, float(val), EntryType[typ]))

        for typ, nam, val in recurr_exp:
            extracted_frame.add_expense(EntryCategory.RECURR, Entry(nam, float(val), EntryType[typ]))

    report_overview = generate_report(extracted_frame)
    print_report(report_overview, extracted_frame)

    input()
    os.system("clear")

    # ----------------------------------
    #    Provide user the options to add entries
    # ----------------------------------
    report_overview = {}
    while(True):
        print("-------------------------------")
        print("What do you want to do next?")
        print("     X: Exit")
        print("     E: Add expense")
        print("     I: Add income")
        userin = input("-------------------------------")

        if userin in ["x", "X"]:
            break
        elif userin in ["e", "E"]:
            n, v, et, c = generate_user_prompt()
            extracted_frame.add_expense(EntryCategory.NONRECURR, Entry(n, v, et, c))
            print("adding your expense...")
            report_overview = generate_report(extracted_frame)

        elif userin in ["i", "I"]:
            n, v, et, c = generate_user_prompt()
            extracted_frame.add_income(EntryCategory.NONRECURR, Entry(n, v, et, c))
            print("adding your income...")
            report_overview = generate_report(extracted_frame)
        else:
            print("Invalid input, please try again!")
        os.system("clear")

    os.system("clear")

    # ----------------------------------
    #    # Save the file and print report
    # ----------------------------------
    print("-------------------------------")
    print("Saving the data into the file...")
    print("-------------------------------")

    report_overview = generate_report(extracted_frame)
    SUCCESS = save_result(filepath, report_overview)
    print("File saving was successful\n" if SUCCESS else "File saving not successful\n")

    print_report(report_overview, extracted_frame)
