import os  # Import os for terminal wipe
import sys  # Import sys for restart of app
import subprocess  # Import subprocess for restart of app
import pandas as pd  # import pandas for excel handling
import time  # Import time for sleep feature
from datetime import date  # Import to get date
from colorama import Fore, Back, Style  # import color sheme


# ----------------------- Google API & Sheets -----------------------
# The following code was taken from and inspired by
# the Code Institute Love Sandwitches project.

import gspread  # Import to work with google sheets

# Import for authorization with the google API
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("evp_survey_samples")
SHEET_DATA = SHEET.worksheet("Survey_data")
SHEET_USER = SHEET.worksheet("Users")


# ----------------------- General Data -----------------------


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

# Valid spellings to use when trying to exit the app
exit_words = [
    "EXIT", "Exit", "eXit", "exIt", "exiT",
    "EXit", "EXIt", "EXiT", "eXIT",
    "ExIt", "ExiT", "ExIT",
    "eXiT", "eXIT",
    "ExiT", "exit"
]

# Valid spellings to use when trying to create a new company
new_words = [
    "NEW", "New", "nEw", "neW",
    "NEw", "NeW", "nEW", "new"
]


# Choose company to analyze.
def select_company(mode, data):
    """
    Summary:
        This function selects the company to do the survey or to analyze.
        The list of companies to choose from comes from the results lists.
        The User can also create a new company when doing the survey.

    Args:
        mode (str): Selection of the mode. Ether "survey" or "analyze".

    Return:
        selected_company (str): Selected company for survey or analyzation.
        new_company (str): Company created by the user when doing survey.
    """

    while True:
        wipe_terminal()  # Clear terminal
        if mode == "survey":
            print(Fore.BLUE + "\nPlease select the company to do the survey."
                  + Style.RESET_ALL
                  )
        else:
            print(Fore.BLUE + "\nPlease select the company"
                  " you want to analyze."
                  + Style.RESET_ALL
                  )
        print("\n-------------------------------------------------- \n")

        company_list = get_companies(mode, data)

        # Take input which company the user selects.
        selection = input("What would you like to do?: ")

        # If the user chooses to do the survey,
        # check if creation of a new company was selected.
        if mode == "survey" and selection in new_words:
            # Get new company name and return it.
            new_company = survey_create_company(company_list)
            return new_company

        # Find company associated to input and return selected company
        try:
            selection_index = (
                int(selection) - 1
            )  # -1 for adjusting to the index count of lists
            if selection_index >= 0 and selection_index < len(company_list):
                selected_company = company_list[selection_index]
                wipe_terminal()  # Clear terminal
                print(f"\nYou selected: ({selection}) {selected_company}")
                time.sleep(2)  # Wait for 2 seconds
                return selected_company
            else:
                raise ValueError
        except ValueError:
            # If users wants to exit, they enter 0 and the program will restart
            if selection == "0":
                restart()
                break
            else:
                wipe_terminal()  # Clear terminal

                print(Fore.RED + "\nSorry, your selection is"
                      " no valid option.\n"
                      + Style.RESET_ALL
                      )
                print("Please try again in 2 seconds.")
                time.sleep(2)  # Wait for 2 seconds


# ----------------------- Get Google Data -----------------------


# Get questions from gspread sheet.
def get_questions_from_google():
    """
    Summary:
        Get content from survey data worksheet and format it as list of lists.

    Return:
        questions (list of str): All questions from the survey as string
        all_g_survey_data (list of lists): All data from gspread results sheet.
    """
    # Select worksheet "Survey_data"
    survey_data = SHEET_DATA

    # All data in a list of lists
    all_g_survey_data = survey_data.get_all_values()

    # Select only the index with the questions in it
    questions = all_g_survey_data[0]
    return questions, all_g_survey_data


# Get users from gspread sheet.
def get_google_users():
    """
    Summary:
        Get information about registered users from gspread sheet "Users"

    Return:
        all_g_survey_users (list of lists): All data from gspread users sheet.

    """
    survey_results = SHEET_USER  # Select worksheet "Users"
    all_g_survey_users = survey_results.get_all_values()
    all_g_survey_users.pop(
        0
    )  # Remove the first row filled with questions from the list
    return all_g_survey_users


# ----------------------- Data Source Functions -----------------------


# Choose which source to get data from for analyzing
def data_choose_source():
    """
    Summary:
        Ask for the data source to get data for analyzation from.
        Include option to go back to previous step.
        In this case restart the program.

    Returns:
        excel_file (list of lists): All survey results data from Excel file.
        gspread (list of lists): All survey result data from gspread.
        False (boolean): If user wants to exit the program.
    """
    while True:
        wipe_terminal()
        print(Fore.BLUE + "\nWhere should your data come from?"
              + Style.RESET_ALL
              )
        print("\n-------------------------------------------------- \n")
        print(Fore.GREEN + "(1) " + Style.RESET_ALL +
              "Import Excel file to analyze\n"
              )
        print(Fore.GREEN + "(2) " + Style.RESET_ALL +
              "Use Google sheet to analyze\n"
              )
        print(Fore.RED + "(0) " + Style.RESET_ALL +
              "Go back to the start of the program\n"
              )
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
            restart()
            break
        else:
            wipe_terminal()  # Clear terminal
            print(Fore.RED + "\nWrong input. Please select "
                  "one of the shown options.\n" + Style.RESET_ALL
                  )
            print("Please try again in 2 seconds.")
            time.sleep(2)  # Wait for 2 seconds


# Get Excel file by import
def data_get_excel_file():
    """
    Summary:
        This function asks for the location of the file to import.
        The "samples.xlsx" can be used for test purposes.
        With the import, a test for the import of a Excel file is done.
        If an Excel file is imported, the file is tested for correct structure.

    Returns:
        excel_content_as_list (List of lists): All survey result data,
        without the first row (date, name, company, questions).
    """
    while True:
        wipe_terminal()  # Clear terminal
        try:
            # Check for error, if a correct file was entered
            # Ask for the location and name of Excel file.
            location = input(
                '\nWhere is the file located?:\n(Test file: "samples.xlsx")\n'
            )
            # Name and location of file is formatted as string
            get_excel = "{}".format(location)
            # Formatted name and location is pasted into read_excel() function
            excel_content = pd.read_excel(get_excel)

            # Validation for correct Excel structure is not implemented
            # Validation would check file structure is correct.
            # If correct, TRUE, else FALSE

            # Return content of the excel file
            excel_content_as_list = (
                excel_content.to_numpy()
            )  # Format results as list of lists

            return excel_content_as_list
        except FileNotFoundError:
            # Print FileNotFoundError statement
            wipe_terminal()  # Clear terminal
            print("\nFileNotFoundError: Sorry, but no Excel file was found.\n")

            # Ask if the user wants to try again entering a file name
            while True:  # Test if user enters only y or n and no other key.
                print("Do you want to try again?\n")
                print(Fore.GREEN + "(1)" + Style.RESET_ALL
                      + " to enter different file name\n")
                print(Fore.RED + "(0)" + Style.RESET_ALL
                      + " to EXIT the application\n")
                try_again = input("What would you like to do?")
                if try_again == "1":
                    print("\n")
                    break  # Go back to beginning of the first while loop
                elif try_again == "0":
                    restart()
                    break
                else:
                    wipe_terminal()  # Clear terminal
                    print("Invalid input. Enter '1' "
                          "to try again or '0' to exit.\n"
                          )


# Get Google spreadsheet by API request.
def data_get_google_file():
    """
    Summary:
        Get content from survey data worksheet and format it as list of lists

    Returns:
        all_g_survey_data (List of lists): All survey result data,
        without the first row (date, name, company, questions).
    """
    survey_data = SHEET.worksheet("Survey_data")  # Select sheet "Survey_data"
    all_g_survey_data = survey_data.get_all_values()
    all_g_survey_data.pop(0)  # Remove the first row (questions) from the list

    return all_g_survey_data


# ----------------------- Data Analyzing Functions -----------------------


# Get company list from selectes source gspread or Excel.
def get_companies(mode, data):
    """
    Summary:
        Get a list of all companies that are existing in the selected source.

    Args:
        mode (str): Selection of the mode. Ether "survey" or "analyze".
        data (List of lists): All data from selected source.

    Returns:
        List of str: List with all companies that are in the gspread database.
    """

    # Create empty list for all companies,
    # that are contained in the results data.
    company_list = []
    # Create empty list for all the indexes,
    # the user can select in this function.
    index_list = []

    # Itterate through the list of data and check for every line,
    # if the company is already in the company_list.
    # If not, add it to that list.
    # Each company should only be in the list one time.
    for entry in data:
        if entry[2] not in company_list:
            company_list.append(entry[2])

    # After every company was added to the list, print every lists element.
    # Before every element of the list, print its index with +1.
    # +1 to not start at 0.
    for company in company_list:
        company_index = company_list.index(company) + 1
        index_list.append(company_index)
        print(Fore.GREEN + f"({company_index}) "
              + Style.RESET_ALL + company
              )

    # If in survey mode, show option to create new company.
    if mode == "survey":
        print(Fore.BLUE + "(NEW)" + Style.RESET_ALL + " Create new company\n")

    print(Fore.RED + "\n(0)" + Style.RESET_ALL + " If you like to exit\n")

    return company_list


# Choose which question to analyze
def analyze_choose_question():
    """
    Summary:
        This function gives the user the option to choose a question,
        for analyzing the results.

    Return:
        selected_question (str): Text of the selected question
        selection (str): Selection made by the user
        selection_index (str): Index of the selected question
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
            print(Fore.BLUE + "\nFrom which question would you "
                  "like to see the results?" + Style.RESET_ALL
                  )
            print("\n-------------------------------------------------- \n")

            # Create empty list for all the indexes
            # the user can select in this function.
            # Creation of this list inside the loop
            # to reset it with every loop.
            index_list = []

            for question in questions:
                question_index = questions.index(question)
                index_list.append(question_index)
                print(
                    Fore.GREEN + f"({question_index + 1})"
                    + Style.RESET_ALL + f"{question}"
                    )  # Print all questions and the associated index + 1

            print(Fore.RED + "\n(0)" + Style.RESET_ALL +
                  " If you like to exit"
                  )
            print("\n-------------------------------------------------- \n")

            # Take input which question the user selects.
            selection = input("Choose a question: ")

            # If users want to exit, they just enter "0"
            # and the program will restart.
            if selection == "0":
                restart()
                break

            if int(selection) > 0 and int(selection) <= len(index_list):

                selection_index = (
                    int(selection) - 1
                )  # -1 for adjusting to the index count of lists
                selected_question = questions[selection_index]

                wipe_terminal()  # Clear terminal
                print(f"\nYou selected: ({selection})\n{selected_question}")
                time.sleep(2)  # Wait for 2 seconds
                return selected_question, selection, selection_index
            else:
                raise ValueError
        except ValueError:
            wipe_terminal()  # Clear terminal
            print(Fore.RED + "\nSorry, your selection is no valid option.\n"
                  + Style.RESET_ALL
                  )
            print("Please try again in 2 seconds.")
            time.sleep(2)  # Wait for 2 seconds


# Display results for one specific question
def analyze_single_question_results(company, data):
    """
    Summary:
        Display the results for a single specific question
        by using the analyze_get_overall_results function.

    Args:
        company (string): Name of the selected company to analyze.
        data (str, int): A list with all survey data,
        that is then filtered for the selected company.
    """
    while True:

        selected_question = analyze_choose_question()
        # Get result for selected company from gspread.
        analyzation_results = analyze_get_overall_results(company, data)
        # Get index of the selected question.
        question_index = int(selected_question[2])
        # Get results of selected question.
        question_result = analyzation_results[1]
        sum = question_result[question_index]

        wipe_terminal()  # Clear terminal
        print(
            f"\nThe results for question "
            + Fore.BLUE
            + selected_question[1]
            + Style.RESET_ALL
            + " for "
            + Fore.BLUE
            + company
            + Style.RESET_ALL
            + " are as follows:\n"
            )
        print("-------------------------------------------------- \n")

        print(selected_question[0] + "\n")

        print(f"Results: {'{:.2f}'.format(sum)} out of 10\n")

        print("-------------------------------------------------- \n")
        input("Press any key and enter to continue!")

        wipe_terminal()  # Clear terminal

        option = nav_analyze_different_question()

        if option:
            break


# Calculate and display the overall company results
def analyze_overall_question_results(company, data):
    """
    Summary:
        Get all data for the selected company,
        calculate results and print them in an overview.

    Args:
        company (string): Name of the company to analyze
    """
    while True:

        analyzation_results = analyze_get_overall_results(company, data)

        # Index for the topics list to go through when printing.
        topic_index = 0

        # Variable for calculation the overall sum
        # of ratings the companie received.
        overall_sum = 0

        wipe_terminal()  # Clear terminal

        print(
            Fore.BLUE
            + "\n" + company
            + Style.RESET_ALL
            + " received "
            + Fore.BLUE
            + str(analyzation_results[0])
            + Style.RESET_ALL
            + " survey submissions."
        )
        print("Results per question are as follows:\n")
        print("-------------------------------------------------- \n")

        # Display the results for each question/topic
        # and calculate overall result sum.
        for sum in analyzation_results[1]:

            # Add rating of this specific question
            # to the overall_sum for the company
            overall_sum += sum
            sum = "{:.2f}".format(
                sum
            )  # Convert float to string and limit to two decimal points.
            print(sum + " of 10 for "
                  + question_topics[topic_index].lower()
                  )
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

        print("\n-------------------------------------------------- \n")
        print(Fore.GREEN + "(1)" + Style.RESET_ALL +
              " Analyze a different company\n"
              )
        print(Fore.RED + "(0)" + Style.RESET_ALL +
              " Exit the program\n"
              )
        option = input("What would you like to do?: ")

        if option == "1":
            return True

        elif option == "0":
            restart()
            break
        else:
            wipe_terminal()  # Clear terminal
            print(Fore.RED + "\nWrong input. Please select"
                  " one of the shown options.\n" + Style.RESET_ALL
                  )
            time.sleep(2)  # Wait for 2 seconds


# Get and calculate the overall company results.
def analyze_get_overall_results(company, data):
    """
    Summary;
        Calculate the average results for every company
        and every question by adding up the individual submits
        and dividing the sum by the sum of submits.

    Args:
        results (list of lists): Contains all the individual answers
        submitted by users taking the survey
        company (string): Name of the company to analyze

    Returns:
        count_submits (int): The amount of submits to these companies survey.
        result_sum (list of floats): Average results
        for every question for this company.
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

            # Starting with 3 because 0-2 are Date,
            # Name, Company and not question answers
            question_index = 3

            # Starting with the first index in the list
            # and go through it with the while loop.
            sum_index = 0

            # For every result to every question,
            # add the answer to the result_sum list.
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


# ----------------------- General Functions -----------------------


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
        This function is for restarting the run.py
        and is used as the EXIT solution
    """
    wipe_terminal()  # Clear terminal
    print(Fore.BLUE + "\nThe program will restart"
          " in 2 seconds." + Style.RESET_ALL
          )
    time.sleep(2)  # Wait for 2 seconds

    # End the current process and restart it
    subprocess.run(["python3", sys.argv[0]])
    # sys.argv[0] defines the path and script
    # to start with python 3. In this case itself.

    sys.exit()  # After restarting the script, exit the current script.


# Display an error message
def unexpected_error():
    """
    Summary:
        If an error occurs which reason is unknown, "
        "this error message is shown.
    """
    print(
        "Houston, we have a problem!\n"
        "Some kind of fatal error happened!"
        "\nThe program will restart in 3 seconds!"
    )
    time.sleep(3)  # Wait for 3 seconds
    restart()


# ----------------------- Login Functions -----------------------


# User login with username and password
def login():
    """
    Summary:
        Login for users to analyze survey results.

    Return:
        True: When login is valid return true.
    """

    # Counter for wrong login attempts
    wrong_attempts_count = 0

    while True:
        wipe_terminal()  # Clear terminal

        print(Fore.BLUE + "\nThis is the user login.\n" + Style.RESET_ALL)
        print("-------------------------------------------------- \n")

        print("If you want to exit, please enter 'EXIT'\n")

        username = input("What is your" + Fore.GREEN + " username"
                         + Style.RESET_ALL + "? (Test)\n"
                         )
        # Validate if the user wants to exit the program using "EXIT"
        if username in exit_words:
            restart()
            break

        password = input("\nPlease enter your" + Fore.GREEN + " password"
                         + Style.RESET_ALL + "? (Test)\n"
                         )
        # Validate if the user wants to exit the program using "EXIT"
        if password in exit_words:
            restart()
            break

        # If username is found in database, this function returns True
        user_valid = login_user_validation(username)

        # If password is correct, functions returns True
        pw_valid = login_password_validation(username, password)

        # If username and password are correct, return True for login
        if user_valid and pw_valid:
            return True  # Login was successful

        # If login was incorrect, increase count and restart when count is 3
        else:
            wipe_terminal()  # Clear terminal
            wrong_attempts_count += 1  # Increase count of failed login attempt
            print(Fore.RED + "\nUsername and/or password are wrong!"
                  + Style.RESET_ALL
                  )
            if wrong_attempts_count < 3:
                print("You have " + Fore.RED + f"{3 - wrong_attempts_count}"
                      + Style.RESET_ALL + " attempts left."
                      )
                time.sleep(3)  # Wait for 3 seconds
            elif wrong_attempts_count == 3:
                print("\nYour 3 login attempts failed.")
                print("The program will restart.\n")
                print(Fore.RED + "Your username will be blocked "
                      "for 5 minutes!" + Style.RESET_ALL
                      )
                print("No, not really ;)")
                time.sleep(5)  # Wait for 5 seconds
                restart()
                break


# Validation for username input
def login_user_validation(username):
    """
    Summary:
        Validate if username is to find in user database (gspreed).

    Args:
        username (str): Username entered by the user.

    Returns:
        boolean: True if username is correct.
    """
    list_of_users = get_google_users()

    for element in list_of_users:
        if username == element[0]:
            return True  # Username is correct

    return False  # Username is wrong


# Validation of password input
def login_password_validation(username, password):
    """
    Summary:
        Validate if the password inserted by the users
        is to be found associated to the username in the database.

    Args:
        username (str): Username entered by the user
        password (str): Password entered by the zser

    Returns:
        boolean: True if password is correct
    """

    list_of_passwords = get_google_users()

    for element in list_of_passwords:
        if username == element[0]:
            if password == element[1]:
                return True  # Password is correct
            else:
                return False  # Password is wrong
        else:
            continue


# ----------------------- Navigation Functions -----------------------


# First screen with navigation
def nav_survey_or_analyze():
    """
    Summary:
        This function displays the first navigation where
        the user can choose between doing the survey
        or logging in and analyzing the data.

    Return:
        "do_survey" (str): Returns the information,
        that the user wants to do the survey.
        "do_login" (str): Returns the information,
        that the user wants login.
    """
    while True:
        wipe_terminal()  # Clear terminal
        print(Fore.BLUE + "\nWelcome to the EVP Survey\n" + Style.RESET_ALL)
        print("-------------------------------------------------- \n")
        print("With this survey, we want to find out, "
              "what makes your employer special.\n")
        print("You have two options to choose from:\n")
        print(Fore.GREEN + "(1)" + Style.RESET_ALL +
              " Do the survey\n"
              )
        print(Fore.GREEN + "(2)" + Style.RESET_ALL +
              " Login and analyze survey results\n"
              )
        option = input("What would you like to do?: ")
        if option == "1":
            # Call survey function
            wipe_terminal()  # Clear terminal
            print("Survey is loading ...")
            return "do_survey"
        elif option == "2":
            # Call login function
            wipe_terminal()  # Clear terminal
            print("\nLogin is loading ...")
            time.sleep(2)  # Wait for 2 seconds
            return "do_login"
        else:
            wipe_terminal()  # Clear terminal
            print(Fore.RED + "\nWrong input. Please select"
                  " one of the shown options.\n" + Style.RESET_ALL
                  )
            time.sleep(2)  # Wait for 2 seconds


# Selection if results of one question or overall results
def nav_one_or_all_question_results():
    """
    Summary:
        Question if to analyze one specific question
        or the overall results of a company.

    Return:
        "One Question" (str): Returns the information
        that the user wants to analyze one single question.
        "Overall Results" (str): Returns the information
        that the user wants to analyze the overall results.
    """
    while True:
        wipe_terminal()
        print(Fore.BLUE + "\nWelcome to the survey results!\n"
              + Style.RESET_ALL
              )

        print(
            "Select if you like to analyze "
            "one specific question or the overall results.\n"
        )
        print("-------------------------------------------------- \n")
        print(Fore.GREEN + "(1)" + Style.RESET_ALL +
              " Analyze one single survey question\n"
              )
        print(Fore.GREEN + "(2)" + Style.RESET_ALL +
              " Analyze overall survey results\n"
              )
        print(Fore.RED + "(0)" + Style.RESET_ALL +
              " If you like to exit\n"
              )
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
            print(Fore.RED + "\nWrong input. Please select "
                  "one of the shown options.\n" + Style.RESET_ALL
                  )
            time.sleep(2)  # Wait for 2 seconds


# Ask if to analyze a different question or exit
def nav_analyze_different_question():
    """
    Summary:
        Ask if to analyze a different question
        after the one just analyzed or exit the program

    Return:
        break: If the user wants to analyze another question
        for the selected company.
        True (boolean): If the user wants to analyze a different company.
    """
    while True:

        wipe_terminal()
        print(Fore.GREEN + "\n(1)" + Style.RESET_ALL
              + " Analyze another question\n"
              )
        print(Fore.GREEN + "(2)" + Style.RESET_ALL
              + " Analyze a different company\n"
              )
        print(Fore.RED + "(0)" + Style.RESET_ALL
              + " Exit the program\n"
              )

        option = input("What would you like to do?: ")

        if option == "1":
            wipe_terminal()  # Clear terminal
            print("\nYou want to analyze a different question."
                  "\nList is loading...\n"
                  )
            time.sleep(2)  # Wait for 2 seconds
            break

        elif option == "2":
            return True

        elif option == "0":
            restart()
            break
        else:
            wipe_terminal()  # Clear terminal
            print(Fore.RED + "\nWrong input. Please select "
                  "one of the shown options.\n" + Style.RESET_ALL
                  )
            time.sleep(2)  # Wait for 2 seconds


# ----------------------- Survey Functions -----------------------


# Class for survey results.
class Survey:
    """
    Summary:
        Initialize the Survey class.
        Used for survey results and export to gspread.

    Args:
        today (str): Current date as string
        name (str): Name of the user
        company (str): Name of the company
        answers (list of ints): Question results in a list
        of ints between 0 and 10
    """

    def __init__(self, today, name, company, *answers):
        self.today = today
        self.name = name
        self.company = company
        self.answers = answers


# Function for going through the survey process.
def survey():
    """
    Summary:
        Logic for doing the survey and exporting results to gspead.
    """

    wipe_terminal()  # Clear terminal

    # Get the company to do the survey for.
    data = data_get_google_file()

    # Defines mode as survey mode.
    mode = "survey"

    # Get the current days date.
    today_raw = date.today()
    # Change date to string format.
    today = today_raw.isoformat()

    # Get the company name from user.
    company = select_company(mode, data)

    # Get the users name.
    name = survey_get_name()

    # Get survey answers from user.
    answers = survey_get_answers(name, company)

    wipe_terminal()  # Clear terminal

    # Put data into class object.
    survey_results = Survey(today, name, company, *answers)

    # Format data for export to gspread sheet.
    survey_data_to_db = [
        survey_results.today,
        survey_results.name,
        survey_results.company,
    ] + list(survey_results.answers)

    # Export survey data to gspread sheet.
    SHEET_DATA.append_row(survey_data_to_db)

    print(Fore.BLUE + f"\nThank you, {name}!" + Style.RESET_ALL)
    print(f"You've completed the survey for {company}")
    time.sleep(2)  # Wait for 2 seconds


# Get the users name.
def survey_get_name():
    """
    Summary:
        Get the user name by input and validate it for specific specifications.
        A maximum of 20 letters, first letter uppercase and the rest lowercase.

    Raises:
        ValueError: When input is not max 20 letters,
        first uppercase, rest lowercase.

    Returns:
        string: Name of the user.
    """
    while True:
        wipe_terminal()  # Clear terminal
        print(Fore.BLUE + "\nWhat is your first name?\n" + Style.RESET_ALL)
        print("-------------------------------------------------- \n")
        print("(Max 20 letters and the first letter in uppercases)\n")
        print("If you want to exit, please enter 'EXIT'\n")
        name = input("Please type in your first name: ")
        # Validate if the user wants to exit the program using "EXIT"
        if name in exit_words:
            restart()
            break

        try:
            # Validate if name is a maximum of 20 letters,
            # first letter uppercase and rest lowercase.
            if (
                name.isalpha()
                and name[0].isupper()
                and name[1:].islower()
                and len(name) <= 20
            ):
                return name
            else:
                raise ValueError

        except ValueError:
            wipe_terminal()  # Clear terminal
            print(Fore.RED + "\nNo valid first name!\n" + Style.RESET_ALL)
            print("Please enter a first name with up to 20 letters")
            print("and make sure that the first letter is in uppercases.\n")
            print("You can try again in 5 seconds.")
            time.sleep(5)  # Wait for 5 seconds


# Create a new company, that is not in the database.
def survey_create_company(company_list):
    """
    Summary:
        User can create a new company that is not already
        existing in the gspread survey results list.

    Args:
        company_list (list of str): All companies that are
        in the gspread survey results list.

    Returns:
        new_company (str): New company created by user.
    """
    while True:
        wipe_terminal()  # Clear terminal
        print(Fore.BLUE + "\nYou want to create a "
              "new company for the survey?\n"
              + Style.RESET_ALL
              )
        print("If you want to exit, please enter 'EXIT'\n")
        new_company = input("Enter the company name: ")

        # Validate if the user wants to exit the program using "EXIT"
        if new_company in exit_words:
            restart()
            break

        # Ask if the entered new company name is correct.
        while True:
            wipe_terminal()  # Clear terminal
            print("\nIs " + Fore.BLUE + f"{new_company}" + Style.RESET_ALL +
                  " as company name correct?\n"
                  )
            print(Fore.GREEN + "(1)" + Style.RESET_ALL +
                  " Use the entered name\n"
                  )
            print(Fore.RED + "(2)" + Style.RESET_ALL +
                  " Enter different name\n"
                  )
            correct_name = input("What would you like to do?: ")

            if correct_name.lower() == "2":
                print("\n")
                break  # Go back to beginning of the first while loop
            elif correct_name.lower() == "1":
                # Check if the entered company is already existing in database
                if new_company in company_list:
                    wipe_terminal()  # Clear terminal
                    print(Fore.RED + f"\n{new_company} is "
                          "already in the database.\n"
                          + Style.RESET_ALL
                          )
                    print("Please enter a different name or EXIT.")
                    time.sleep(3)  # Wait for 3 seconds
                    break
                else:
                    return new_company
            else:
                wipe_terminal()  # Clear terminal
                print(
                    "\nInvalid input. Please enter (1) "
                    "to continue or (2) for a different name."
                    )
                time.sleep(2)  # Wait for 2 seconds


# Get survey answeres from user.
def survey_get_answers(name, company):
    """
    Summary:
        The user has to answer 8 questions with an int value
        between 0 and 10. The results are then used for saving
        in the gspread file.

    Args:
        name (str): First name of the person doing the survey.

    Raises:
        ValueError: Error for when no valid input was given.

    Returns:
        answers (list of ints): A list with an int value between 0 and 10
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
    # Initializing a list to be filled with the users answers.
    answers = []

    for question in questions:

        # Count the questions for showing the current one displayed.
        question_count += 1

        while True:
            wipe_terminal()  # Clear terminal
            print(Fore.BLUE + f"\n{name}, you are doing the survey "
                  f"for the company {company}.\n" + Style.RESET_ALL
                  )
            print("-------------------------------------------------- \n")
            print("Please answer the following question.")
            print("Choose a value between 0 and 10.\n")
            print("If you want to exit, please enter 'EXIT'\n")
            print("-------------------------------------------------- \n")
            print(Fore.BLUE + f"Question {question_count}:" + Style.RESET_ALL)
            print(question)
            user_input = input()
            # Validate if the user wants to exit the program using "EXIT"
            if user_input in exit_words:
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
                print(Fore.RED + "\nYour answer is not valid.\n"
                      + Style.RESET_ALL
                      )
                print("Please choose a value between 0 and 10.")
                time.sleep(2)  # Wait for 2 seconds

    return answers


# ----------------------- Program Flow -----------------------


# Start of the program - Do survey or login and analyze data
def main():
    """
    Summary:
        This function starts the program and contains all logics.
    """
    wipe_terminal()  # Clear terminal

    # Calling the first navigation function to
    # ask if user wants to analyze existing data or do the survey
    survey_or_analyze = nav_survey_or_analyze()

    # Select what option is chosen in the first navigation step
    if survey_or_analyze == "do_survey":
        survey()  # Start survey, the end of the program is included.
    elif survey_or_analyze == "do_login":
        login_true = login()  # Start login process

    # If login was valid, call function to choose data source for analyzation
    if survey_or_analyze == "do_login" and login_true:
        wipe_terminal()  # Clear terminal
        print(Fore.GREEN + "\nYou are now logged in!" + Style.RESET_ALL)
        time.sleep(2)  # Wait for 2 seconds

        # Choose data source to analyze. Excel file or gspread file.
        data = data_choose_source()

        # Defines mode as analyzation mode
        mode = "analyze"

        while True:
            # User is now logged in and can start with the analyzing.
            # Function to start the first analyzing step
            # with selecting the company to analyze.
            company = select_company(mode, data)

            # Function to define if the user wants to analyze one
            # specific question or the overall results of the company.
            analyzation = nav_one_or_all_question_results()

            if analyzation == "One question":
                # Start analyzation of one single question results.
                analyze_single_question_results(company, data)

            elif analyzation == "Overall results":
                # Start analyzation of the overall company results.
                analyze_overall_question_results(company, data)

            else:
                unexpected_error()

            print(company + analyzation)
    wipe_terminal()  # Clear terminal
    print("\nThis is the end of all things!\n")
    print("The program will restart in 3 seconds.")
    time.sleep(3)  # Wait for 3 seconds

    restart()


# ----------------------- Program Start -----------------------


# Start the program
main()
