import xlrd

book = xlrd.open_workbook('samples.xlsx')

header = []
report_card = []

# Count Stmnts for Required Data
valid_count = 0
app_req_count = 0
intr_req_count = 0

# Count Stmts for Missing Data
missing_app_count = 0
missing_intr_count = 0
missing_oe_intr_count = 0

sheet = book.sheets()[0]
for row_num, row in enumerate(sheet.get_rows()):
    if row_num <= 4:
        #  print(row)  # Print out the header
        header.append([row[0], row[2]])

print(header)