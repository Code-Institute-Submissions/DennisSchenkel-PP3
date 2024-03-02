![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **March 14, 2023**

## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!





## Modules & libraries used

### Google-Auth

Google-Auth helps with the authentication to use the google API

### gspread

gspread is needed for accessing and updating data in a google spread sheet.


### xlrd

xlrd is a library that helps with reading data from Excel files (.xls).


### Panda

Panda helps with importing and analyzing data


### openpyxl

openpyxl is a library that helps with reading data from Excel files (.xlsx/.xlsm).

### colorama

colorama helps with coloring the text and its background

### Misc.

- pyArrow
- os - for terminal wipe
- sys - Import sys for restart of app
- subprocess - Import subprocess for restart of app
- time - Import time for sleep feature
- datetime - Import to get date



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





## Items to develop

### Login

- Ask for Login
- Ask if just do survey



### Result calculation

- Select compamy to analyse
    - Loop through result list and add each company and number of done surveys in another list



### Do survey

- Select existing company from list
- If not in list, write own company name

- Go back to previous question



## Acknowledgement


Although I not copied entire code, I'd like to acknoledge the following resources as inspiration

- Restart() - using subprocess and sys
    - Great information about how to use subprocesses and sys instead ob os if to find here: https://www.dataquest.io/blog/python-subprocess/ 

- wipe_terminal() - using os 
    - A lengthy discussion on the various methodes of clearing the termal is to find here: https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python

