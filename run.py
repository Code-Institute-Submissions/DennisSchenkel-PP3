# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import os #Import os for terminal vipe
import pandas as pd # import pandas for excel handling
import time # Import time for sleep feature


# ------------------------------------ Google API & Sheets ------------------------------------

# The following code was taken from the Code Institute Love Sandwitches project.
import gspread # Import to work with google sheets
from google.oauth2.service_account import Credentials # Import for authorization with the google API

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("evp_survey_samples")

def get_g_survey_data():
    """
    Get content from survey data worksheet
    """
    survey_data = SHEET.worksheet("Survey_data")
    all_g_survey_data = survey_data.get_all_values()
    return all_g_survey_data

def get_g_survey_results():
    """
    Get content from survey results worksheet
    """
    survey_results = SHEET.worksheet("Survey_results")
    all_g_survey_results = survey_results.get_all_values()
    return all_g_survey_results


# ------------------------------------ App Functions ------------------------------------

# Get Excel file by import
def get_excel_file():
    """
    This functions asks for the location of the file to import. 
    The "samples.xlsx" can be used for test purposes.
    With the import a test for the import of a Excel file is done.
    If a Excel file is imported, the file is tested for correct structure.
    """
    vipe_terminal() # Clear terminal
    while True:
        try:
            # Check for error, if a correct file was entered       
            # Ask for the location and name of Excel file.
            location = input('Where is the file located?:\n(E.g. "samples.xlsx")\n')  
            # Name and location of file is formatted as string
            get_excel = "{}".format(location)
            # Formatted name and location is pasted into read_excel() function
            excel_read = pd.read_excel(get_excel)
            
                                                                                            # Validation for correct Excel structure is missing
                                                                                            # If correct, TRUE, else FALSE
            
            # Return content of the excel file
            print("file read")
            return excel_read
        except:
            # Print FileNotFoundError statement
            vipe_terminal() # Clear terminal
            print("FileNotFoundError: Sorry, but no Excel file to use war found.\n")
            
            # Ask if the user wants to try again entering a file name and location
            while True:  # Test if user enters only y or n and no other key.
                try_again = input("Do you want to try a different file? (y/n): ")
                if try_again.lower() == 'y':
                    print("\n")
                    break  # Go back to beginning of the first while loop
                elif try_again.lower() == 'n':
                    print("Going back to the start")
                    start() # Restart programm by calling start()
                    break
                else:
                    # vipe_terminal() # Clear terminal
                    print("\nInvalid input. Please enter 'y' to try again or 'n' to exit.")
        
        
# ------------------------------------ General Functions ------------------------------------

def start():
    """
    Start of the program.
    """
    vipe_terminal() # Clear terminal
    print("Welcome to the EVP Survey\n")
    print("You have two options to choose from:\n")
    print("(1) Import file to analyze\n")
    print("(2) Use the integrated Google sheet to analyze\n")
    options = input("What would you like to do?: ")
    if options == "1":
        list = get_excel_file()
        return list
    elif options == "2":
        print("\nOption 2 was not integrated at this point.")
    else:
        vipe_terminal() # Clear terminal
        print("Wrong input. Please select one of the shown options.\n")
        print("The program will restart in 3 seconds.")
        time.sleep(3)
        start()

def vipe_terminal():
    """
    Delete all text in the terminal
    """
    if os.name == "posix":  # macOS and Linux
        os.system("clear")
    elif os.name == "nt":  # Windows
        os.system("cls")
        
        
# ------------------------------------ Start Program ------------------------------------
        
vipe_terminal() # Clear terminal

# Call start function and asign result to data variable
data = start() 

# Print returned content of excel file
print(data)



# Print content of the google worksheets
gresult = get_g_survey_results()
print(gresult)




