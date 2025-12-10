import pandas as pd

xl = pd.ExcelFile('Level_3.xlsx')
print(xl.sheet_names)
