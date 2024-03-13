# EVP Survey

## Introduction

Code Institute - Portfolio Project 3 - Python Command-Line Application

![The deployed application can be found here] (Link to app here)

This application is giving small companies a tool to do surveys among their employees to get valid information about what makes the company a special employer and what is the EVP (Employer Value Proposition). Therefore users can do the survey and answer 8 questions that later can be used in a analyzation of the overall company results.
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
  * [Lighthouse Testing](#lighthouse-testing)
  * [Manual Testing](#manual-testing)
  * [Known And Unfixed Bugs](#known--unfixed-bugs)
  * [Learnings](#learnings)
  * [Possible Improvements](#possible-improvements)

* [Credits](#credits)
  * [Acknowledgments](#acknowledgments)






## User Experience

This application is giving small companies a tool to do surveys among their employees to get valid information about what makes the company a special employer. Therefore users can do the survey and answer 8 questions that later can be used in a analyzation of the overall company results.
Users with an account are able to access the analyzation of the survey company results.


### User Stories

**Employees doing the survey**

- As a employee, I would like to select the company that I work for, so that I can do the survey.
- As a employer. I want to be able to add another company to the list of companies, so I can do the survey for a company not already listet.


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

This application uses only a few colores for highlighting important information and user options.

**Blue**

Page headlines.

Highlighting important information.


**Green**

Highlighting navigation options


**Red**

Highlighting of exit options.

Highlighting important critical information.

Invalid input message.


### Flowchart

![Flowchart](documentation/images/flowchart.png)



## Features

### Frontend Features


### Logic Features



### Technical Features

**User Login**



**Data Source Selection**

Choose between two different data sources to get data from. Google Spreadsheet as cloud service or a local Excel file.


**Data Export**



### Accessibility

## Technologies Used

### Languages Used

- Python



### Modules & libraries used

**Google-Auth**
Google-Auth helps with the authentication to use the google API.

**gspread**
gspread is needed for accessing and updating data in a google spread sheet.

**xlrd**
xlrd is a library that helps with reading data from Excel files (.xls).

**Panda**
Panda helps with importing and analyzing data.

**openpyxl**
openpyxl is a library that helps with reading data from Excel files (.xlsx/.xlsm).

**colorama**
colorama helps with coloring the text and its background.

**Misc.**
- pyArrow
- os - for terminal wipe
- sys - Import sys for restart of app
- subprocess - Import subprocess for restart of app
- time - Import time for sleep feature
- datetime - Import to get date


### Programs Used

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
### Lighthouse Testing
### Manual Testing
### Known And Unfixed Bugs
### Learnings
### Possible Improvements

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

