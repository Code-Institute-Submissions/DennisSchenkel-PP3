# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import pandas as pd

print('test')


def get_excel_file():
    """
    This functions asks for the location of the file to import. 
    The "samples.xlsx" can be used for test purposes.
                                                        After input the list is printed.
                                                                            The Try statement for validation of file input is missing
    """
    location = input('Where is the file located?:\n(Write "samples.xlsx" for the samples file)\n')

    # Name and location of file is formatted as string
    get_excel = "{}".format(location)
    
    # Formatted name and location is pasted into read_excel() function
    excel_content = pd.read_excel(get_excel) 
    
    # Return content of the excel file
    return(excel_content)

# Trigger function to get import of excel file
list = get_excel_file()

# Print returned content of excel file
print(list)