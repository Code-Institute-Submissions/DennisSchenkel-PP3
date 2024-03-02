# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import os  # Import os for terminal wipe
import sys  # Import sys for restart of app
import subprocess  # Import subprocess for restart of app
import pandas as pd  # import pandas for excel handling
import time  # Import time for sleep feature
from datetime import date  # Import to get date
from colorama import Fore, Back, Style  # import color sheme


# --------------------------------- Google API & Sheets ---------------------------------

# The following code was taken from the Code Institute Love Sandwitches project.
import gspread  # Import to work with google sheets
from google.oauth2.service_account import (
    Credentials,
)  # Import for authorization with the google API

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("evp_survey_samples")


# --------------------------------- General Data ---------------------------------

# A list of the topics of the questions in the survey
question_topics = [
    "Motivation",
    "Recognition and valuing",
    "Career opportunities",
    "Fairness and equality",
    "Salary and benefits",
    "Decision-making processes",
    "Leadership",
    "Employee integration",
]


# Choose company to analyse
def select_company(mode):
    """
    Summary:
        This functions is for selecting the company to analyze. The list of companies to choose from comes from the companies in the results lists.
    """
    while True:
        wipe_terminal()  # Clear terminal
        print("Please select the company you want to analyze.")
        print("------------------------------------------------------------ \n")

        company_list = get_google_companies(mode)
        
        # Take input which company the user selects.
        selection = input()

        # If the user chooses to do the survey, check if creation of a new company was selected.
        if mode == "survey" and selection == "NEW":
            # Get new company name and return it.
            new_company = survey_create_company()
            return new_company

        # Find company associated to input and return selected company
        try:
            selection_index = (
                int(selection) - 1
            )  # -1 for adjusting to the index count of lists
            if selection_index >= 0 and selection_index < len(company_list):
                selected_company = company_list[selection_index]
                wipe_terminal()  # Clear terminal
                print(f"You selected: ({selection}) {selected_company}")
                time.sleep(2)  # Wait for 2 seconds
                return selected_company
            else:
                raise ValueError
        except ValueError:
            # If users want to exit, they just enter "0" and the program will restart.
            if selection == "0":
                restart()
                break
            else:
                wipe_terminal()  # Clear terminal
                print("exeption Error")
                print(
                    "Sorry, your selection is no valid option.\nPlease try again in 2 seconds."
                )
                time.sleep(2)  # Wait for 2 seconds



# --------------------------------- Get Google Data ---------------------------------


def get_questions_from_google():
    """
    Summary:
        Get content from survey data worksheet and format it as list of lists
    """
    survey_data = SHEET.worksheet("Survey_data")  # Select worksheet "Survey_data"
    all_g_survey_data = survey_data.get_all_values()  # All data in a list of lists
    questions = all_g_survey_data[0]  # Select only the index with the questions in it
    return questions, all_g_survey_data


def get_google_users():
    """
    Summary:
        Get information about registered users from google sheet and worksheet "Users"
    """
    survey_results = SHEET.worksheet("Users")  # Select worksheet "Users"
    all_g_survey_results = survey_results.get_all_values()
    all_g_survey_results.pop(
        0
    )  # Remove the first row filled with questions from the list
    return all_g_survey_results




# --------------------------------- Data Source Functions ---------------------------------


# Choose which source to get data from for analyzing
def data_choose_source():
    """
    Summary:
        Ask for the data source to get data for analyzation from.
        Include option to go back to previous step. In this case restart the program.
    """
    while True:
        wipe_terminal()
        print("(1) Import Excel file to analyze\n")
        print("(2) Use Google sheet to analyze\n")
        print("(0) Go back to the start of the program\n")
        option = input("What would you like to do?: ")
        if option == "1":
            # Call function to get data from excel sheet
            excel_file = data_get_excel_file()
            return excel_file
        elif option == "2":
            # Call function to get data from google sheet
            gspread = data_get_google_file()
            return gspread
        elif option == "0":
            wipe_terminal()  # Clear terminal
            print("The program will restart in 2 seconds.")
            time.sleep(2)  # Wait for 2 seconds
            return False
        else:
            wipe_terminal()  # Clear terminal
            print("Wrong input. Please select one of the shown options.\n")
            print("Please try again in 2 seconds.")
            time.sleep(2)  # Wait for 2 seconds


# Get Excel file by import
def data_get_excel_file():
    """
    Summary:
        This functions asks for the location of the file to import.
        The "samples.xlsx" can be used for test purposes.
        With the import a test for the import of a Excel file is done.
        If a Excel file is imported, the file is tested for correct structure.
    """
    while True:
        wipe_terminal()  # Clear terminal
        try:
            # Check for error, if a correct file was entered
            # Ask for the location and name of Excel file.
            location = input('Where is the file located?:\n(Test file: "samples.xlsx")\n')
            # Name and location of file is formatted as string
            get_excel = "{}".format(location)
            # Formatted name and location is pasted into read_excel() function
            excel_content = pd.read_excel(get_excel)

            # Validation for correct Excel structure is not implemented
            # Validation would check file tructure is correct.
            # If correct, TRUE, else FALSE

            # Return content of the excel file
            excel_content_as_list = (
                excel_content.to_numpy()
            )  # Format results as list of lists

            return excel_content_as_list
        except FileNotFoundError:
            # Print FileNotFoundError statement
            wipe_terminal()  # Clear terminal
            print("FileNotFoundError: Sorry, but no Excel file was found.\n")

            # Ask if the user wants to try again entering a file name and location
            while True:  # Test if user enters only y or n and no other key.
                try_again = input("Do you want to try a different file? (y/n): ")
                if try_again.lower() == "y":
                    print("\n")
                    break  # Go back to beginning of the first while loop
                elif try_again.lower() == "n":
                    restart()
                    break
                else:
                    wipe_terminal()  # Clear terminal
                    print(
                        "\nInvalid input. Please enter 'y' to try again or 'n' to exit."
                    )


# Get Google spreadsheet by API request.
def data_get_google_file():
    """
    Summary:
        Get content from survey data worksheet and format it as list of lists
    """
    survey_data = SHEET.worksheet("Survey_data")  # Select worksheet "Survey_data"
    all_g_survey_data = survey_data.get_all_values()
    all_g_survey_data.pop(0)  # Remove the first row filled with questions from the list

    return all_g_survey_data


# --------------------------------- Data Analyzing Functions ---------------------------------




def get_google_companies(mode):
    
    # Get all survey data from gspread.
    data = data_get_google_file()
    
    # Create empty list for all companies that are contained in the results data.
    company_list = []
    # Create empty list for all the indexes the user can select in this function.
    index_list = []

    # Itterate through the list of data and check for every line, 
    # if the company is already in the company_list.
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

    # If in survey mode, show option to create new company.
    if mode == "survey":
        print("(NEW) Create new company\n")

    print("\n(0) If you like to exit\n")
    
    return company_list





# Choose which question to analyze
def analyze_choose_question():
    """
    Summary:
        This function gives the user the option to choose a question for analyzing the results.
    """
    only_questions = get_questions_from_google()
    questions = only_questions[0]
    del questions[
        0:3
    ]  # Remove first two entries from list of questions (Date, Company Name)

    while True:

        # Find question associated with input and return selected question
        try:

            wipe_terminal()  # Clear terminal
            print("From which question would you like to see the results?")
            print("------------------------------------------------------------ \n")

            # Create empty list for all the indexes the user can select in this function.
            # Creation of this list inside the loop to reset it with every loop.
            index_list = []

            for question in questions:
                question_index = questions.index(question)
                index_list.append(question_index)
                print(
                    f"({question_index + 1}) {question}"
                )  # Print all questions and the associated index + 1

            print("\n(0) If you like to exit")
            print("\n------------------------------------------------------------ \n")

            # Take input which question the user selects.
            selection = input("\nChoose a question: ")

            # If users want to exit, they just enter "0" and the program will restart.
            if selection == "0":
                restart()
                break

            if int(selection) > 0 and int(selection) <= len(index_list):

                selection_index = (
                    int(selection) - 1
                )  # -1 for adjusting to the index count of lists
                selected_question = questions[selection_index]

                wipe_terminal()  # Clear terminal
                print(f"You selected: ({selection}) {selected_question}")
                time.sleep(2)  # Wait for 2 seconds
                return selected_question, selection, selection_index
            else:
                raise ValueError
        except ValueError:
            wipe_terminal()  # Clear terminal
            print(
                "Sorry, your selection is no valid option.\nPlease try again in 2 seconds."
            )
            time.sleep(2)  # Wait for 2 seconds


# Display results for one specific question
def analyze_single_question_results(company, data):
    """
    Summary:
        Display the results for a single specific question by using the analyze_get_overall_results function.

    Args:
        company (string): Name of the selected company to analyze.
        data (str, int): A list with all survey data that is then filtered for the selected company.
    """
    while True:

        selected_question = analyze_choose_question()
        analyzation_results = analyze_get_overall_results(company, data)
        question_index = int(selected_question[2])
        question_result = analyzation_results[1]
        sum = question_result[question_index]

        wipe_terminal()  # Clear terminal
        print(
            f"The results for question {selected_question[1]} for {company} are as follows:\n"
        )
        print("------------------------------------------------------------ \n")

        print(selected_question[0] + "\n")

        print(f"Results: {'{:.2f}'.format(sum)} out of 10\n")

        print("------------------------------------------------------------ \n")
        input("Press any key to continue!")

        wipe_terminal()  # Clear terminal

        option = nav_analyze_different_question()

        if option:
            break


# Calculate and display the overall company results
def analyze_overall_question_results(company, data):
    """
    Summary:
        Get all data for the selected company, calculate results and print them in an overview.

    Args:
        company (string): Name of the company to analyze
    """
    #    result_data = get_questions_from_google() # Get all data from g-spread
    #    results = result_data[1] # 1 to select the second RETURN from the function

    while True:
        analyzation_results = analyze_get_overall_results(company, data)

        topic_index = 0  # Index for the topics list to go through when printing.
        overall_sum = 0  # Variable for calculation the overall sum of ratings the companie received.

        wipe_terminal()  # Clear terminal

        print(
            Fore.BLUE
            + company
            + Style.RESET_ALL
            + " reveived "
            + Fore.BLUE
            + str(analyzation_results[0])
            + Style.RESET_ALL
            + " survey submissions."
        )
        print("Results per question are as follows:\n")
        print("------------------------------------------------------------ \n")

        # Display the results for each question/topic and calculate overall result sum.
        for sum in analyzation_results[1]:
            overall_sum += sum  # Add rating of this specific question to the overall_sum for the company
            sum = "{:.2f}".format(
                sum
            )  # Convert float to string and limit to two decimal points.
            print(sum + " of 10 for " + question_topics[topic_index].lower() + "\n")
            topic_index += 1  # Go to next topic

        print(
            f"\nThe overall result for "
            + Fore.BLUE
            + company
            + Style.RESET_ALL
            + " is "
            + Fore.BLUE
            + "{:.2f}".format(overall_sum)
            + Style.RESET_ALL
            + " out of "
            + Fore.BLUE
            + "80"
            + Style.RESET_ALL
            + "."
        )

        print("\n------------------------------------------------------------ \n")
        print("(1) Analyse a different company\n")
        print("(0) Exit the program\n")
        option = input("What would you like to do?: ")

        if option == "1":
            return True

        elif option == "0":
            restart()
            break
        else:
            wipe_terminal()  # Clear terminal
            print("Wrong input. Please select one of the shown options.\n")
            time.sleep(2)  # Wait for 2 seconds


# Get and calculate the overall company results.
def analyze_get_overall_results(company, data):
    """
    Summary;
        Calculate the average results for every company and every question by adding up the individual submits and deviding the sum by the sum of submits.

    Args:
        results (list of lists): Contains all the individual answeres submitted by users taking the survey
        company (string): Name of the company to analyze

    Returns:
        count_submits (int): The amount of submits to this companies survey.
        result_sum (list of floats): Average results for every question for this company.
    """
    count_submits = 0  # Used for later deviding the summed up question results

    result_sum = [0, 0, 0, 0, 0, 0, 0, 0]

    result_data = data
    # get_questions_from_google() # Get all data from g-spread
    results = result_data  # 1 to select the second RETURN from the function

    # For every row (list) in the list(s) of results
    for result in results:

        # Only use the row, if the company mentioned is the selected company.
        if result[2] == company:

            count_submits += (
                1  # For every submit for this company, increase the count by 1
            )
            result_count = len(
                result
            )  # Length of each row of results in the results g-spread
            question_index = 3  # Starting with 3 because 0-2 are Date, Name, Company and not question answers
            sum_index = 0  # Starting with the first index in the list and go though it with the while loop.

            # For every result to every question, add the answer to the result_sum list.
            while question_index < result_count:

                result_sum[sum_index] = result_sum[sum_index] + float(
                    result[question_index]
                )  # Make sure to convert so float for accurate calculation.

                sum_index += 1  # Go to next index in result_sum list
                question_index += 1  # Go to answer for the next question

    # Calculate the average result for every question from this company.
    if count_submits > 0:
        result_sum = [value / count_submits for value in result_sum]

    return count_submits, result_sum


# --------------------------------- General Functions ---------------------------------


# Clear the terminal from all text
def wipe_terminal():
    """
    Summary:
        Delete all text in the terminal
    """
    if os.name == "posix":  # Identify if OS is macOS or Linux
        os.system("clear")
    elif os.name == "nt":  # Identify of OS is Windows
        os.system("cls")


# Restart the program by executing run.py
def restart():
    """
    Summary:
        This function is for restarting the run.py and is used as the EXIT solution
    """
    wipe_terminal()  # Clear terminal
    print(Fore.BLUE + "You want to exit" + Style.RESET_ALL)
    print("The program will restart in 2 seconds.")
    time.sleep(2)  # Wait for 2 seconds

    # End the current process and restart it
    subprocess.run(
        ["python3", sys.argv[0]]
    )  # sys.argv[0] defines the path and script to start with python 3. In this case itselfe.
    sys.exit()  # After restarting the script, exit the current script.


# Display an error message
def unexpected_error():
    """
    Summary:
        If an error occures which reason is unknown, this error message is shown.
    """
    print(
        "Housten, we have a problem!\nSome kind of fatal error happend!\nThe program will restart in 3 seconds!"
    )
    time.sleep(3)  # Wait for 3 seconds
    restart()


# --------------------------------- Login Functions ---------------------------------


# User login with username and password
def login():
    """
    Summary:
        Login for users to analyze survey results.
    """
    wipe_terminal()  # Clear terminal
    username = (
        login_user_validation()
    )  # If username is found this function returns the correct username
    login_password_validation(username)  # Correct password sets variable to True
    return True  # Returns True when login worked correctly


# Validadion of username input
def login_user_validation():
    """
    Summary:
        Validate if username is to find in user database (gspreed).
    """
    list_of_users = get_google_users()
    print(Fore.BLUE + "This is the user validation." + Style.RESET_ALL)
    print("If you want to exit, please enter 'EXIT'\n")
    while True:
        username = input(
            "What is your username? (Test)\n"
        )  # Use "Test" as test user (with uppercase T)
        # Validate if the user wants to exit the program using "EXIT"
        if username == "EXIT":
            restart()
            break
        else:
            for element in list_of_users:
                if username == element[0]:
                    wipe_terminal()  # Clear terminal
                    print(
                        Fore.GREEN
                        + f"Your username {username} is correct!"
                        + Style.RESET_ALL
                    )
                    time.sleep(2)  # Wait for 2 seconds
                    return username
        wipe_terminal()  # Clear terminal
        print(Fore.RED + "Username was not found.\nPlease try again." + Style.RESET_ALL)
        print("If you want to exit, pleas enter 'EXIT'\n")


# Validation of password input
def login_password_validation(username):
    """
    Summary:
        Validate if the password insered by the users is valid.
    """
    list_of_passwords = get_google_users()
    wipe_terminal()  # Clear terminal
    print(Fore.BLUE + "This is the password validation." + Style.RESET_ALL)
    print("------------------------------------------------------------ \n")
    print("If you want to exit, please enter 'EXIT'\n")
    while True:
        wipe_terminal()  # Clear terminal
        print(Fore.BLUE + "This is the password validation." + Style.RESET_ALL)
        print("------------------------------------------------------------ \n")
        print("If you want to exit, please enter 'EXIT'\n")
        password = input(
            "Please enter your password? (Test)\n"
        )  # Use "Test" as test user (with uppercase T)
        # Validate if the user wants to exit the program using "EXIT"
        if password == "EXIT":
            restart()
            break
        else:
            for element in list_of_passwords:
                if username == element[0]:
                    if password == element[1]:
                        wipe_terminal()  # Clear terminal
                        print(
                            Fore.GREEN
                            + "Password is correct!\n"
                            + Style.RESET_ALL
                            + "You will now get logged in ..."
                        )
                        time.sleep(2)  # Wait for 2 seconds
                        return True
                    else:
                        wipe_terminal()  # Clear terminal
                        print(
                            Fore.RED
                            + "Password is not correct.\nPlease try again."
                            + Style.RESET_ALL
                        )
                        time.sleep(2)  # Wait for 2 seconds
                else:
                    continue


# --------------------------------- Navigation Functions ---------------------------------


# First screen with navigation
def nav_survey_or_analyze():
    """
    Summary:
        This function displays the first navigation where the user can choose between doing the survey or logging in and analyzing the data.
    """
    while True:
        wipe_terminal()  # Clear terminal
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
            time.sleep(2)  # Wait for 2 seconds
            return "do_login"
        else:
            wipe_terminal()  # Clear terminal
            print("Wrong input. Please select one of the shown options.\n")
            time.sleep(2)  # Wait for 2 seconds


# Selection if results of one question or overall results
def nav_one_or_all_question_results():
    """
    Summary:
        Question if to analyse one specific question or the overall results of a company.
    """
    while True:
        wipe_terminal()
        print(
            "Please select if you like to analyze on specific question or the overall results."
        )
        print("------------------------------------------------------------ \n")
        print("(1) Analyse one single survey question\n")
        print("(2) Analyse overall survey results\n")
        print("(0) If you like to exit, please enter EXIT\n")
        option = input("What would you like to do?: ")
        if option == "1":
            print(option)
            return "One question"
        elif option == "2":
            print(option)
            return "Overall results"
        elif option == "0":
            restart()
            break
        else:
            wipe_terminal()  # Clear terminal
            print("Wrong input. Please select one of the shown options.\n")
            time.sleep(2)  # Wait for 2 seconds


# Ask if to analyze a different question or exit
def nav_analyze_different_question():
    """
    Summary:
        Ask if to analyze a different question after the one just analyzed or exit the program
    """
    while True:

        wipe_terminal()
        print("(1) Analyse another question\n")
        print("(2) Analyse a different company\n")
        print("(0) Exit the program\n")

        option = input("What would you like to do?: ")

        if option == "1":
            wipe_terminal()  # Clear terminal
            print("You want to analyze a different question. \nList is loading...\n")
            time.sleep(2)  # Wait for 2 seconds
            break

        elif option == "2":
            return True

        elif option == "0":
            restart()
            break
        else:
            wipe_terminal()  # Clear terminal
            print("Wrong input. Please select one of the shown options.\n")
            time.sleep(2)  # Wait for 2 seconds


# --------------------------------- Survey Functions ---------------------------------











class Survey:
    def __init__(self, today, name, company, q1, q2, q3, q4, q5, q6, q7, q8):
        self.today = today
        self.name = name
        self.company = company
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
        self.q5 = q5
        self.q6 = q6
        self.q7 = q7
        self.q8 = q8





def survey():
    """
    Summary:
        Do survey.
    """
    
    wipe_terminal()  # Clear terminal
    
    # Get the company to do the survey for.
    
    # Defines mode as survey mode.
    mode = "survey"

    today = date.today()

    print(today)
    
    name = survey_get_name()
    
    company = select_company(mode)
    
    print(company)

    answer = survey_get_answers(name)

    survey_answers = Survey(today, name, company, *answer)

    print(survey_answers)

    input()





def survey_get_name():
    """
    Summary:
        Get the user name by input and validate it for specific specifications.
        A maximum of 20 letters, first leter uppercase and the rest lowercase.

    Raises:
        ValueError: When input is not max 20 letters, first uppercase, rest lowercase.

    Returns:
        string: Name of the user.
    """
    while True:
        
        wipe_terminal()  # Clear terminal
        print("What is your first name?")
        print("(Max 20 letters and the first letter in uppercases)")
        print("If you want to exit, please enter 'EXIT'\n")
        name = input("Please type in your first: ")
        # Validate if the user wants to exit the program using "EXIT"
        if name == "EXIT":
            restart()
            break

        try:
            # Validate if name is a maximum of 20 letters,
            # first letter uppercase and rest lowercase.
            if (name.isalpha() and 
                name[0].isupper() and 
                name[1:].islower() and 
                len(name) <= 20):                
                return name
            else:
                raise ValueError
        
        except ValueError:
            wipe_terminal()  # Clear terminal
            print("No valid first name!\n")
            print("Please enter a first name with up to 20 letters")
            print("and make sure that the first letter is in uppercases.\n")
            print("You can try again in 5 seconds.")
            time.sleep(5)  # Wait for 5 seconds
        
        




def survey_create_company():
    
    while True:
        wipe_terminal()  # Clear terminal
        print("You want to create a new company for the survey?")
        print("What is the company name?\n")
        print("If you want to exit, please enter 'EXIT'\n")
        new_company = input()
        
        # Validate if the user wants to exit the program using "EXIT"
        if new_company == "EXIT":
            restart()
            break
        
        while True:
            print(f"Is {new_company} correct?")
            print("(y) Use the entered name")
            print("(n) Enter different name\n")
            correct_name = input()
            
            if  correct_name.lower() == "n":
                print("\n")
                break  # Go back to beginning of the first while loop
            elif  correct_name.lower() == "y":
                return new_company
            else:
                wipe_terminal()  # Clear terminal
                print("\nInvalid input. Please enter 'y' to continue or (n) for a different name.")
                time.sleep(2)  # Wait for 2 seconds



def survey_get_answers(name):
    """
    Summary:
        The user has to answer 8 questions with an int valie
        between 0 and 10. The results are then used for saving
        in the gspread file.
    
    Args:
        name (str): First name of the person doing the survey.

    Raises:
        ValueError: Error for when no valid input was given.

    Returns:
        answers (list of ints): A list with a int value between 0 and 10
        for each answered question.
    """
    # Get all data from gspread.
    get_questions = get_questions_from_google()
    # Select only all the questions from the first row.
    selected_questions = get_questions[0]
    # Remove date, name and company from questions list.
    questions = selected_questions[3:]

    # Initializing a counter for questions.
    question_count = 0
    # Initialising a list to be filled with the users answers.
    answers = []

    
    for question in questions:

        # Count the questions for showing the current one displayed.
        question_count += 1

        while True:
            wipe_terminal()  # Clear terminal
            print(f"{name}, please answer the following question.")
            print("Choose a value between 0 and 10.\n")
            print("If you want to exit, please enter 'EXIT'\n")
            print(f"Question {question_count}:")
            print(question)
            user_input = input()
            # Validate if the user wants to exit the program using "EXIT"
            if user_input == "EXIT":
                restart()
                break
            
            # Validate is user input is integer.
            try:
                int_user_input = int(user_input)
                # If input is int, check if between 0 and 10.
                # If so, add to answers list.
                if int_user_input >= 0 and int_user_input <= 10:
                    answers.append(int_user_input)
                    break
                else:
                    raise ValueError
            # If input is not correct, raise ValueError.
            except ValueError:
                wipe_terminal()  # Clear terminal
                print("Your answer is not valid.")
                print("Please choose a value between 0 and 10.")
                time.sleep(2)  # Wait for 2 seconds
                    
    return answers










# --------------------------------- Program Flow ---------------------------------


# Start of the program - Do survey or login and analyze data
def main():
    """
    Summary:
        This functions starts the program and contains all logics.
    """
    wipe_terminal()  # Clear terminal

    # Calling the first navigation function to ask if user wants to analyze existing data or do the survey
    survey_or_analyze = nav_survey_or_analyze()

    # Select what option is choosen in the first navigation step
    if survey_or_analyze == "do_survey":
        survey()
    elif survey_or_analyze == "do_login":
        login_true = login()

    # If login was valid, call function to choose data source for analyzation
    if survey_or_analyze == "do_login" and login_true:
        print("You are now logged in")
        time.sleep(2)  # Wait for 2 seconds

        # Choose data source to analyse. Excel file or gspread file.
        data = data_choose_source()
        
        # Defines mode as analyzation mode
        mode = "analyze"

        while True:

            # User is now logged in and can start with the analyzing.
            # Function to start the first analyzing step with selecting the company to analyze.
            company = select_company(mode)

            # Function to define if the user wants to analyze one specific question or the overall results of the company.
            analyzation = nav_one_or_all_question_results()

            if analyzation == "One question":
                analyze_single_question_results(company, data)

            elif analyzation == "Overall results":
                analyze_overall_question_results(company, data)

            else:
                unexpected_error()

            print(company + analyzation)

    else:
        unexpected_error()


# --------------------------------- Program Start ---------------------------------



# survey()
main()  # Start the program
