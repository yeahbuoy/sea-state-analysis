import os
import glob
import pandas as pd
from deCorrupter import *
generate_dataframe("./scraped")

files = [
    'CoolSpreadSheet.csv',
    'scraped-data.csv'
]

combined_spreadsheet = pd.concat([pd.read_csv(f) for f in files], sort=True)
combined_spreadsheet.to_csv('CombinedSpreadSheet.csv', index=False)