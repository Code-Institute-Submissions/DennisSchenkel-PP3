# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import os
import pandas as pd


# ------------------------------------ App Functions ------------------------------------

# Get Excel file by import
def get_excel_file():
    """
    This functions asks for the location of the file to import. 
    The "samples.xlsx" can be used for test purposes.
    With the import a test for the import of a Excel file is done.
    If a Excel file is imported, the file is tested for correct structure.
    """
   
    while True:
        try:
            # Check for error, if a correct file was entered       
            # Ask for the location and name of Excel file.
            location = input('Where is the file located?:\n(E.g. "samples.xlsx")\n')  
            # Name and location of file is formatted as string
            get_excel = "{}".format(location)
            # Formatted name and location is pasted into read_excel() function
            excel_content = pd.read_excel(get_excel)
            
                                                                                            # Validation for correct Excel structure is missing
                                                                                            # If correct, TRUE, else FALSE
            
            # Return content of the excel file
            return excel_content
        except:
            # Print FileNotFoundError statement
            vipe_terminal()
            print("\nFileNotFoundError: Sorry, but no Excel file to use war found.\n")
            
            # Ask if the user wants to try again entering a file name and location
            while True:  # Test if user enters only y or n and no other key.
                try_again = input("Do you want to try a different file? (y/n): ")
                if try_again.lower() == 'y':
                    break  # Go back to beginning of the first while loop
                elif try_again.lower() == 'n':
                    print("Going back to the start")
                    start() # Restart programm by calling start()
                    break
                else:
                    vipe_terminal()
                    print("Invalid input. Please enter 'y' to try again or 'n' to exit.")
        

        

# ------------------------------------ General Functions ------------------------------------

def start():
    """
    Start of the program.
    """
    vipe_terminal()
    print("Welcome to the EVP Survey\n")
    print("What would you like to do?\n")
    print("(1) Import file to analyze\n")
    print("(2) Use the integrated Google sheet to analyze\n")


def vipe_terminal():
    """
    Delete all text in the terminal
    """
    if os.name == "posix":  # macOS and Linux
        os.system("clear")
    elif os.name == "nt":  # Windows
        os.system("cls")
        
        
# ------------------------------------ Start Program ------------------------------------
        
vipe_terminal()
start()

# Call function to get import of excel file
list = get_excel_file() 

# Print returned content of excel file
print(list)