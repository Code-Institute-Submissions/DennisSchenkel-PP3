# EVP Survey

## Introduction

Code Institute - Portfolio Project 3 - Python Command-Line Application

[The deployed application can be found here](https://ci-pp3-survey-dennis-schenkel-25f95a95d1e3.herokuapp.com/)

This application is giving small companies a tool to do surveys among their employees to get valid information about what makes the company a special employer and what is the EVP (Employer Value Proposition). Therefore, users can do the survey and answer 8 questions that later can be used in an analyzation of the overall company results.
Users with an account are able to access the analyzation of the survey company results.


## Table of Contents

* [Introduction](#introduction)

* [User Experience](#user-experience-ux)
  * [User Stories](#user-stories)

* [Design](#design)
  * [Color Scheme](#color-scheme)
  * [Flowchart](#flowchart)

* [Features](#features)
  * [Frontend Features](#frontend-features)
  * [Logic Features](#logic-features)
  * [Technical Features](#technical-features)
  * [Accessibility](#accessibility)

* [Technologies Used](#technologies-used)
  * [Languages Used](#languages-used)
  * [Frameworks, Libraries Used](#frameworks--libraries-used)
  + [Programs Used](#programs-used)

* [Deployment](#deployment)

* [Testing](#testing)
  * [Validator Testing](#validator-testing)
  * [Manual Testing](#manual-testing)
  * [Known And Unfixed Bugs](#known--unfixed-bugs)
  * [Learnings](#learnings)
  * [Possible Improvements](#possible-improvements)

* [Credits](#credits)
  * [Acknowledgments](#acknowledgments)






## User Experience

This application is giving small companies a tool to do surveys among their employees to get valid information about what makes the company a special employer. Therefore, users can do the survey and answer 8 questions that later can be used in an analyzation of the overall company results.
Users with an account are able to access the analyzation of the survey company results.


### User Stories

**Employees doing the survey**

- As an employee, I would like to select the company that I work for, so that I can do the survey.
- As an employer. I want to be able to add another company to the list of companies, so I can do the survey for a company not already listed.


**Employer analyzing survey results**

- As a manager, I want to be able to log into a secured area, so that I get access to the survey results.
- As a manager, I want be able to select a source of data, so that I am able to use my own excel file as data source.
- As a manager, I would like to select the company that I work for, to work with only the relevant data.
- As a manager, I would like to select the results of a specific question, to get only the results of this question.
- As a manager, I would like to select an overview of the overall results of the company survey, to get all relevant information on one scree.


**All users**

- As a user, I would like to be able to exit the application at any stage, so I am not trapped in a lengthy process that I can not stop.


## Design

### Color Scheme

This application uses only a few colors for highlighting important information and user options.

**Blue**

- Page headlines - All page headlines are in blue color.

- Highlighting important information - Important information like results are in blue color.


**Green**

- Highlighting navigation options - Options that can be selected by the user are in green color.


**Red**

- Highlighting important critical information - Critical information like invalid login attempt are in red color.

- Invalid input message - Information about invalid input is stated in red color.

- Highlighting of exit options - Exit options are in red color.



### Flowchart

The option to exit the program is indicated in the flowchart with "(Exit Opt.)" in every step, it is available.

![Flowchart](documentation/images/flowchart.png)



## Features

### Frontend Features


### Logic Features



### Technical Features

**User Login**

- User login: Users can log in by using a valid username and password.

- User data: The gspread file imported contains a sheet with information of multiple users, including username and password.

- 3 Invalid login attempts: When a user unsuccessfully tries to log in for three times, the program is ending and a message displayed that the account is blocked for 5 minutes. (This is not really happening due to avoiding misunderstanding when testing the app. This feature could easily be added by posting a time stamp in the user's gspread sheet and with every login attempt test if a time stamp of no longer then 5 minutes ago is associated with the user.)


**Data Source Selection**

When selecting to analyze survey results, the user can choose between two different data sources to get data from. Google Spreadsheet as cloud service or a local Excel file.
The local Excel file must be located within the application folder. In the current state only the owner of the repository can add different files. In a later version a upload feature could be added.

**Data Export**

When a survey has been conducted, the results are exported to a gspread sheet and extended with the current date.


### Accessibility

Since the application is solely console based, accessibility can not really be influenced by the creator. Still, it is important to make the console content as readable as possible by using colors and clear structures. In this application, I tried to make the content as understandable and readable as possible.


## Technologies Used

### Languages Used

- Python



### Modules & libraries used

**Google-Auth**
- Google-Auth helps with the authentication to use the Google API.


**gspread**
- gspread is needed for accessing and updating data in a Google spread sheet.


**xlrd**
- xlrd is a library that helps with reading data from Excel files (.xls).


**Panda**
- Panda helps with importing and analyzing data.


**openpyxl**
- openpyxl is a library that helps with reading data from Excel files (.xlsx/.xlsm).


**colorama**
- colorama helps with coloring the text and its background.


**Misc.**
- pyArrow
- os - for terminal wipe
- sys - Import sys for restart of app
- subprocess - Import subprocess for restart of app
- time - Import time for sleep feature
- datetime - Import to get date


### Programs Used

During the development of this application, the following programs have been used.

- VS Code
- Lucid
- Heroku
- Git
- GitHub
- Excel
- Google Spreadsheet



## Deployment

## Testing
### Validator Testing

The code validation with the Code Institute Python Linter shows no errors
![CI Python Linter](documentation/images/ci-python-linter.png)


### Manual Testing

| **Test** | **Description** | **Expected Outcome** | **Result** |
| --- | --- | --- | --- |
| **Welcome Screen** |  |  |  |
| --- | --- | --- | --- |
| Selecting "Do the survey" | Entering 1 and pressing enter | App accepting input and loading list of companies from gspread | Pass |
| Selecting "Login and analyze survey results" | Entering 2 and pressing enter | Accepting input, showing loading screen and login screen | Pass |
| Enter not shown option (int) | Entering an integer that is not shown and pressing enter | Show error message for wrong input and reload screen | Pass |
| Enter not shown option (str) | Entering an string that is not shown and pressing enter | Show error message for wrong input and reload screen | Pass |
| Enter not shown option (empty space) | Not entering anything and pressing enter | Show error message for wrong input and reload screen | Pass |
| --- | --- | --- | --- |
| **Conducting Survey** |  |  |  |
| --- | --- | --- | --- |
| **Select Company** |  |  |  |
| Select a shown company | Entering an int shown and press enter | Show screen to confirm selection and loading screen for input of first name | Pass |
| Select "Create new compyne" | Entering "NEW" and press enter | Show screen to enter new company name or exit the app | Pass |
| Enter "NEW" in not only upper cases | Entering "NEW" in various writings | Show screen to enter new company name or exit the app | Pass |
| Exit application | Entering "0" and press enter | Show confirmation screen that app is restarting in 2 seconds an then restarts | Pass |
| Enter not shown option (int) | Entering an integer that is not shown and pressing enter | Show error message for wrong input and reload screen | Pass |
| Enter not shown option (str) | Entering an string that is not shown and pressing enter | Show error message for wrong input and reload screen | Pass |
| Enter not shown option (empty space) | Not entering anything and pressing enter | Show error message for wrong input and reload screen | Pass |
| **Create New Company** |  |  |  |
| Enter new company name | Enter a new company name and press enter | Show screen to confirm entered new company name | Pass |
| Exit application | Enter "EXIT" and press enter | Show confirmation screen that app is restarting in 2 seconds an then restarts | Pass |
| Enter "EXIT" in not only upper cases | Entering "EXIT" in various writings | Show confirmation screen that app is restarting in 2 seconds an then restarts | Pass |
| Enter new company name | A company name is entered | Show screen to confirm entered company name | Pass |
| Confirm new company name | Confirm new company name by pressing 1 and enter | Show next screen for entering the users first name | Pass |
| Decline new company name | Decline new company name by pressing 2 and enter | Reload screen to enter new comoany name | Pass |
| Enter existing company name | An existing company name is entered and confirmed | Show error message and exit hint and reload screen to enter new company name | Pass |
| **Enter Users First Name** |  |  |  |
| Enter name | Enter name with first letter uppercase and not more then 20 letters | Load first survey question with correct name in header | Pass |
| Enter wrong name (int) | Enter name with an integer in it | Show error screen with name conventions and reload after 5 seconds | Pass |
| Enter name with first letter not uppercase  | Enter name where the first letter or is not uppercase | Show error screen with name conventions and reload after 5 seconds | Pass |
| Enter name with wrong letter sizes  | Enter name where the first letter or is not uppercase and/or others are uppercase | Show error screen with name conventions and reload after 5 seconds | Pass |
| Enter name with empty space  | Enter name with an empty space in it | Show error screen with name conventions and reload after 5 seconds | Pass |
| Enter name with empty space  | Enter name with an empty space in it | Show error screen with name conventions and reload after 5 seconds | Pass |
| Enter name with with 20+ letters  | Enter name with to many letters (20+) | Show error screen with name conventions and reload after 5 seconds | Pass |
| **Answer Survey Questions** |  |  |  |






| --- | --- | --- | --- |
| **Analyzing Results** |  |  |  |
| --- | --- | --- | --- |
| Step 1 circle active | Mark circle step indicator as active | The first of the white circles in the header gets a dark-colored border. | Pass |
| Step 1 text active  | Change text of step indicator in header | Text in header changes to "Step 1: Select talent to reach". | Pass |
| Step 1 circle done  | Mark circle step indicator as done | When going to step 2 the bordered circle of step 1 gets filled out and the number gets white. | Pass |
| Step 1 circle back  | Change of circle step indicator in header | When going back to the start page from step 1, the bordered circle of step 1 gets back to white again and all circles are completely white. | Pass |
| Step 1 text back  | Change text of step indicator in header | Text in header changes back to "Start". | Pass |
| Step 2 circle active | Mark circle step indicator as active | The second of the white circles in the header gets a dark-colored border. | Pass |
| Step 2 text active | Change text of step indicator in header | Text in header changes to "Step 2: Choose platforms to use". | Pass |
| Step 2 circle done  | Mark circle step indicator as done | When going to step 3 the bordered circle of step 2 gets filled out and the number gets white. | Pass |
| Step 2 circle back  | Change of circle step indicator in header | When going back to step 1 from step 2, the bordered circle of step 2 gets back to white again and the circle of step 1 is no longer filled out but only with the border again. Former white number of the now active gets black again. | Pass |
| Step 2 text back  | Change text of step indicator in header | Text in header changes back to "Step 1: Select talent to reach". | Pass |
| Step 3 circle active | Mark circle step indicator as active | The third of the white circles in the header gets a dark-colored border. | Pass |
| Step 3 text active | Change text of step indicator in header | Text in header changes to "Step 3: Define budget to allocate". | Pass |
| Step 3 circle done  | Mark circle step indicator as done | When going to step 4 the bordered circle of step 3 gets filled out and the number gets white. | Pass |
| Step 3 circle back  | Change of circle step indicator in header | When going back to step 2 from step 3, the bordered circle of step 3 gets back to white again and the circle of step 2 is no longer filled out but only with the border again. Former white number of the now active gets black again. | Pass |
| Step 3 text back  | Change text of step indicator in header | Text in header changes back to "Step 2: Choose platforms to use". | Pass |
| Step 4 circle active | Mark circle step indicator as active | The fourth of the white circles in the header gets a dark-colored border. | Pass |
| Step 4 text active | Change text of step indicator in header | Text in header changes to "Step 4: Results & recommendations". | Pass |
| Step 4 circle back  | Change of circle step indicator in header | When going back to step 3 from step 4, the bordered circle of step 4 gets back to white again and the circle of step 3 is no longer filled out but only with the border again. Former white number of the now active gets black again. | Pass |
| Step 4 text back  | Change text of step indicator in header | Text in header changes back to "Step 3: Define budget to allocate". | Pass |
| **Footer** |  |  |  |
| Responsiveness - Footer imprint element | Check for responsiveness of footer element | Footer element with imprint link should always be located at the bottom right of the page and stay in this position when window size is changed. | Pass |
| Footer Imprint Link | Click on the logo in footer | Loading of the imprint.html in the same tab. | Pass |




### Known And Unfixed Bugs
### Learnings



### Possible Improvements

- Deactivating user account for five minutes after three failed login attempts.
- User can upload own Excel file with survey results to analyze.
- Uploaded Excel file will be checked for correct structure and data validity.
- Improving the visual design with some ASCII art and other ways for better structuring.
- More sophisticated analyzing algorithm.


## Credits
### Acknowledgments











## Excel file structure

- Only one sheet
- Questions and kind of field input in first row
    -   Date, Name, Company Name, Questions
- Answers in following rows

G-Spread
https://docs.google.com/spreadsheets/d/16vTHxofSbLFpQXTzHNgIS84chSTrg7NF4gkwami_Di0/edit?usp=sharing


## Questions to integrate

How motivated are you to come to work every day?

How much do you feel valued and recognized for your work?

How would you rate the opportunities for professional development and career opportunities in the company?

Do you feel you are treated fairly and equally?

How would you rate the company's salary and benefits?

How transparent are decision-making processes in the company?

How would you rate the leadership skills in the company?

How well are new employees integrated into the company?







## Acknowledgement


Although I not copied entire code, I'd like to acknoledge the following resources as inspiration

- Restart() - using subprocess and sys
    - Great information about how to use subprocesses and sys instead ob os if to find here: https://www.dataquest.io/blog/python-subprocess/ 

- wipe_terminal() - using os 
    - A lengthy discussion on the various methodes of clearing the termal is to find here: https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python

