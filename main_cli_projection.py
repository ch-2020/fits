"""Modules"""
import os

from models.projection import Projection

def prompt_projection_input():
    """
    Prompt to input projection
    """
    os.system("clear")

    month_input = 0
    print("You wish to add a new entry for month X (number)?...")

    while True:
        try:
            month_input = int(input("Please enter a valid month...: "))
            if month_input < 0 or month_input > 12:
                print("Invalid input. Please enter a valid month value.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid int value.")

    os.system("clear")

    type_input = ""
    while(type_input not in ["i", "I", "e", "E"]):
        print("Please enter a valid option?...")
        print("-------------------------------")
        print("     i: income")
        print("     e: expense")
        type_input = input("-------------------------------\n")

    os.system("clear")

    item_input = input("Item: ")
    value_input = ""
    while True:
        try:
            value_input = float(input("Please enter a valid value...: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid float value.")

    print(f"{month_input} - {type_input} - {item_input}: {value_input}")
    input()

def generate_plot():
    """
    Function to generate plot
    """
    print("You wish to generate the projection...")


if __name__ == "__main__":
    p = Projection("Financial forecast 2024")

    # ----------------------------------
    #    Provide user the options
    # ----------------------------------
    while(True):
        print("-------------------------------")
        print("What do you want to do next?")
        print("     X: Exit")
        print("     A: Add projection")
        print("     V: Visualize projection")
        userin = input("-------------------------------\n")

        if userin in ["x", "X"]:
            break
        elif userin in ["a", "A"]:
            prompt_projection_input()
        elif userin in ["v", "V"]:
            generate_plot()
        else:
            print("Invalid input, please try again!")
        os.system("clear")

    os.system("clear")

    # ----------------------------------
    #    Save the file and print report
    # ----------------------------------
    print("Saving the results...")
