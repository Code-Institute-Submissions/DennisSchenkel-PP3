# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import os #Import os for terminal vipe
import pandas as pd # import pandas for excel handling
import time # Import time for sleep feature




questions = ["Name", "Question 1", "Question 2", "Question 3", "Question 4", "Question 5", "Question 6", "Question 7", "Question 8"]








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

def get_google_file_data():
    """
    Get content from survey data worksheet and format it as list of lists
    """
    survey_data = SHEET.worksheet("Survey_data") # Select worksheet "Survey_data"
    all_g_survey_data = survey_data.get_all_values()
    all_g_survey_data.pop(0) # Remove the first row filled with questions from the list
    return all_g_survey_data

def get_google_users():
    """
    Get information about registered users from google sheet and worksheet "Users"
    """
    survey_results = SHEET.worksheet("Users") # Select worksheet "Users"
    all_g_survey_results = survey_results.get_all_values()
    all_g_survey_results.pop(0) # Remove the first row filled with questions from the list
    return all_g_survey_results




        
        
# ------------------------------------ General Functions ------------------------------------

# Clear the terminal from all text
def vipe_terminal():
    """
    Delete all text in the terminal
    """
    if os.name == "posix":  # macOS and Linux
        os.system("clear")
    elif os.name == "nt":  # Windows
        os.system("cls")
        

def program():
    while True:
        keepgoing = choose_data_source()
        print(keepgoing)                             ## Delete later ----------------------------
        
        if keepgoing != True:   # If keepgoing is no longer true, the program will end. this is 
            break



# ------------------------------------ App Functions ------------------------------------

# Start of the program - Do survey or login and analyze data
def start():
    """
    Start of the program.
    """
    while True:
        vipe_terminal() # Clear terminal
        print("Welcome to the EVP Survey\n")
        print("You have two options to choose from:\n")
        print("(1) Do the survey\n")
        print("(2) Login and analyze survey results\n")
        option = input("What would you like to do?: ")
        if option == "1":
            # Call survey function
            print("Here comes the survey")
        elif option == "2":
            # Call login function
            print("Here comes the Login")
            choose_data_source()
        else:
            vipe_terminal() # Clear terminal
            print("Wrong input. Please select one of the shown options.\n")
            print("The program will restart in 3 seconds.")
            break
            # time.sleep(3) # Wait for 3 seconds
            # os.system('python "run.py"') # Restart programm by calling start()





# ------------------------------------ Survey Functions ------------------------------------



def survey():
    """
    Do survey.
    """
    for q in questions:
        print("This is the question:")
        answer = input(q)
        print(answer)


def select_company():
    """
    Select company for servey
    """



# ------------------------------------ Data Analyzing Functions ------------------------------------


def login():
    """
    Login for users to analyze survey results.
    """

    



def choose_data_source():
    """
    Ask for the data source to get data for analyzation from.
    Include option to go back to previous step. In this case restart the program.
    """
    while True:
        vipe_terminal()
        print("(1) Import Excel file to analyze\n")
        print("(2) Use Google sheet to analyze\n")
        print("(3) Go back to the start of the program\n")
        option = input("What would you like to do?: ")
        if option == "1":
            # Call function to get data from excel sheet
            excel_file = get_excel_file_data()
            return excel_file
        elif option == "2":
            # Call function to get data from google sheet
            gsheet = get_google_file_data()
            return gsheet  
        elif option == "3":
            vipe_terminal() # Clear terminal
            print("The program will restart in 3 seconds.")
            time.sleep(3) # Wait for 3 seconds
            # vipe_terminal()
            return False
        else:
            vipe_terminal() # Clear terminal
            print("Wrong input. Please select one of the shown options.\n")
            print("Please try again in 3 seconds.")
            time.sleep(3) # Wait for 3 seconds



# ------------------------------------ Data Source Excel: Functions ------------------------------------


# Get Excel file by import
def get_excel_file_data():
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
            excel_content = pd.read_excel(get_excel)
            
                                                                                            # Validation for correct Excel structure is missing
                                                                                            # If correct, TRUE, else FALSE
            
            # Return content of the excel file
            excel_content_as_list = excel_content.to_numpy() # Format results as list of lists
            return excel_content_as_list
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
                    os.system('python "run.py"') # Restart programm by calling start()
                else:
                    # vipe_terminal() # Clear terminal
                    print("\nInvalid input. Please enter 'y' to try again or 'n' to exit.")



        
# ------------------------------------ Start Program ------------------------------------
        
vipe_terminal() # Clear terminal

# Call start function and asign result to data variable
# data = start()
survey()

# Print returned content of excel file


# print(data)

# print(data[0][6])