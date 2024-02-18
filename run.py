# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import os #Import os for terminal vipe
import sys # Import sys for restart of app
import subprocess # Import subprocess for restart of app
import pandas as pd # import pandas for excel handling
import time # Import time for sleep feature
from colorama import Fore, Back, Style # import color sheme




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
    if os.name == "posix":  # Identify if OS is macOS or Linux
        os.system("clear")
    elif os.name == "nt":  # Identify of OS is Windows
        os.system("cls") 

# Restart the program by executing run.py
def restart():
    vipe_terminal() # Clear terminal
    print(Fore.BLUE + "You want to exit" + Style.RESET_ALL)
    print("The program will restart in 2 seconds.")
    time.sleep(2) # Wait for 2 seconds
    
    # End the current process and restart it
    subprocess.run(['python3', sys.argv[0]]) # sys.argv[0] defines the path and script to start with python 3. In this case itselfe.
    sys.exit() # After restarting the script, exit the current script.
    
    
        



# ------------------------------------ App Functions ------------------------------------

# Start of the program - Do survey or login and analyze data
def start():
    """
    This functions starts the program and contains all logics.
    """
    
    vipe_terminal() # Clear terminal

    
    # Calling the first navigation function to ask if user wants to analyze existing data or do the survey
    survey_or_analyze = nav_survey_or_analyze()

    # Select what option is choosen in the first navigation step
    if survey_or_analyze == "do_survey":
        survey()
    elif survey_or_analyze == "do_login":
        login_true = login()

    # If login was valid, call function to choose data source for analyzation
    if survey_or_analyze == "do_login" and login_true == True:
        print("You are now logged in")
        data = choose_data_source()
        
        # User is now logged in and can start with the analyzing.
        # Function to start the first analyzing step with selecting the company to analyze.
        company = analyze_select_company(data)
        
        print(company)
   
    else:
        print("Housten, we have a problem!\nSome kind of fatal error happend!\nThe program will restart in 3 seconds!")
        time.sleep(3) # Wait for 3 seconds
        restart()





# ------------------------------------ Navigation Functions ------------------------------------

def nav_survey_or_analyze():
    """
    This function displays the first navigation where the user can choose between doing the survey or logging in and analyzing the data.
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
            print("Survey is loading ...")
            return "do_survey"
        elif option == "2":
            # Call login function
            print("Login is loading ...")
            time.sleep(2) # Wait for 2 seconds
            return "do_login"
        else:
            vipe_terminal() # Clear terminal
            print("Wrong input. Please select one of the shown options.\n")
            time.sleep(2) # Wait for 2 seconds




# ------------------------------------ Survey Functions ------------------------------------



def survey():
    """
    Do survey.
    """
    for q in questions:
        print("This is the question:")
        answer = input(q)
        print(answer)


def survey_select_company():
    """
    Select company the user wants to do the servey for
    """



# ------------------------------------ Login Functions ------------------------------------

# User login with username and password
def login():
    """
    Login for users to analyze survey results.
    """
    vipe_terminal() # Clear terminal
    username = login_user_validation()    # If username is found this function returns the correct username
    password_valid = login_password_validation(username)    # Correct password sets variable to True   
    return True # Returns True when login worked correctly
        
# Validadion of username input 
def login_user_validation():
    """
    Validate if username is to find in user database (gspreed)
    """
    list_of_users = get_google_users()
    print(Fore.BLUE + "This is the user validation." + Style.RESET_ALL)
    print("If you want to exit, please enter 'EXIT'\n")
    while True:
        username = input("What is your username?\n")  # Use "Test" as test user (with uppercase T)    
        if username == "EXIT":
            restart()
            break
        else:   
            for element in list_of_users:
                if username == element[0]:    
                    vipe_terminal() # Clear terminal
                    print(Fore.GREEN + f"Your username {username} is correct!" + Style.RESET_ALL)
                    time.sleep(2) # Wait for 2 seconds
                    return username
        vipe_terminal() # Clear terminal
        print(Fore.RED + "Username was not found.\nPlease try again." + Style.RESET_ALL)
        print("If you want to exit, pleas enter 'EXIT'\n")    
    
# Validation of password input    
def login_password_validation(username):
    """
    Validate if the password insered by the users is valid
    """    
    list_of_passwords = get_google_users()
    vipe_terminal() # Clear terminal
    print(Fore.BLUE + "This is the password validation." + Style.RESET_ALL)
    print("If you want to exit, please enter 'EXIT'\n")
    while True:
        vipe_terminal() # Clear terminal
        print(Fore.BLUE + "This is the password validation." + Style.RESET_ALL)
        print("If you want to exit, please enter 'EXIT'\n")
        password = input("Please enter your password?\n")  # Use "Test" as test user (with uppercase T)    
        if password == "EXIT":
            restart()
            break
        else:   
            for element in list_of_passwords:
                if username == element[0]:    
                    if password == element[1]:
                        vipe_terminal() # Clear terminal
                        print(Fore.GREEN + "Password is correct!\n" + Style.RESET_ALL + "You will now get logged in ...")
                        time.sleep(2) # Wait for 2 seconds
                        return True
                    else:
                        vipe_terminal() # Clear terminal
                        print(Fore.RED + "Password is not correct.\nPlease try again." + Style.RESET_ALL)
                        time.sleep(2) # Wait for 2 seconds
                else:
                    continue
    
    
    

        


# ------------------------------------ Data Analyzing Functions ------------------------------------


def analyze_select_company(data):
    """
    Select company to analyze
    """
    while True:
        vipe_terminal()
        print("Please select the company you want to analyze.")    
        print("If you like to exit, pleas enter EXIT\n")

        # Create empty list for all companies that are contained in the results data
        company_list = []
        index_list = []
        
        # Itterate through the list of data and check for every line, if the company is already in the company_list.
        # If not, add it to that list.
        # Each company should only be in the list one time.
        for entry in data:
            if entry[2] not in company_list:
                company_list.append(entry[2])
                
        # After every company was added to the list, print every element in the list.
        # Before every element of the list, print its index with +1 to not start at 0.
        for company in company_list:
            company_index = company_list.index(company) + 1
            index_list.append(company_index)
            print(f"({company_index}) " + company + "\n")
        
        # Take input which company the user selects.
        selection = input()   
        
        try:
            selection_index = int(selection) - 1
            if selection_index >= 0 and selection_index <= len(company_list):
                selected_company = company_list[selection_index]
                vipe_terminal()
                print(f"You selected: ({selection}) {selected_company}")
                time.sleep(2) # Wait for 2 seconds
                
            else:
                raise ValueError
                

        except ValueError:
            # If users want to exit, they just enter "Exit" and the program will restart. 
            if selection == "EXIT":
                restart()
                break
            
            else:
                vipe_terminal()
                print("exeption Error")
                print("Sorry, your selection is no valid option.\nPlease try again in 2 seconds.")
                time.sleep(2) # Wait for 2 seconds


# ------------------------------------ Data Source: Functions ------------------------------------

# Choose which source to get data from for analyzing
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
            gspread = get_google_file_data()
            return gspread  
        elif option == "3":
            vipe_terminal() # Clear terminal
            print("The program will restart in 2 seconds.")
            time.sleep(2) # Wait for 2 seconds
            return False
        else:
            vipe_terminal() # Clear terminal
            print("Wrong input. Please select one of the shown options.\n")
            print("Please try again in 2 seconds.")
            time.sleep(2) # Wait for 2 seconds


# Get Excel file by import
def get_excel_file_data():
    """
    This functions asks for the location of the file to import. 
    The "samples.xlsx" can be used for test purposes.
    With the import a test for the import of a Excel file is done.
    If a Excel file is imported, the file is tested for correct structure.
    """
    while True:
        vipe_terminal() # Clear terminal
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
                    restart()
                    break
                else:
                    # vipe_terminal() # Clear terminal
                    print("\nInvalid input. Please enter 'y' to try again or 'n' to exit.")



        
# ------------------------------------ Start Program ------------------------------------
        

start()