# Main program that does everything

import pandas as pd

# Import raw data from excel files
# How to read from excel https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html
# Need to use engine option as described here: https://stackoverflow.com/questions/48066517/python-pandas-pd-read-excel-giving-importerror-install-xlrd-0-9-0-for-excel
data_raw_publications = pd.read_excel("input/MAG - 2021 AI Index Report (Main).xlsx", sheet_name="By CountryRegion", engine='openpyxl')
data_raw_investment_amount = pd.read_excel("input/NetBase Quid - 2021 AI Index Report.xlsx", sheet_name="Investment Amount", engine='openpyxl')
data_raw_number_companies = pd.read_excel("input/NetBase Quid - 2021 AI Index Report.xlsx", sheet_name="Number of Companies", engine='openpyxl')

# Clean publications data
data_publications = data_raw_publications
data_publications = data_publications[data_publications["Publish Year"] == 2020] # Drop non-2020 data
data_publications = data_publications[data_publications["Field of Study"] == "Artificial intelligence"] # Drop non-AI data
# TODO: Change to collapse. I just don't know how to do that yet # Collapse number of papers or citations, by field of study
data_publications = data_publications[["Country Name","Doc Type","Number of Papers"]] # Drop unnecessary variables
data_publications_long = data_publications #rename wide to be clear
#Reshape publications data from long to wide
data_publications_wide = data_publications_long.pivot(index="Country Name",columns="Doc Type",values="Number of Papers") # Learned how to do this here: https://www.datasciencemadesimple.com/reshape-long-wide-pandas-python-pivot-function/
data_publications = data_publications_wide.reset_index() # the pivot changed country name to the df index. This changes Country name from the df's index back to a variable

# Clean investment amount data
data_investment_amount = data_raw_investment_amount
data_investment_amount = data_investment_amount[["Target Location ", 2020]] # Drop unnecessary variables
data_investment_amount = data_investment_amount.rename(columns={2020: "Investment Amount"})
data_investment_amount = data_investment_amount.rename(columns={"Target Location ": "Country Name"})

# Clean number of companies data
data_number_companies = data_raw_number_companies
data_number_companies = data_number_companies[["Target Location",2020]] # Drop unnecessary variables
data_number_companies = data_number_companies.rename(columns={2020: "Number of Companies"})
data_number_companies = data_number_companies.rename(columns={"Target Location": "Country Name"})

# Merge data
data_main = data_number_companies.merge(data_investment_amount, on="Country Name", how="outer") # Outer merge keeps data that is in either
data_main = data_main.merge(data_publications_wide, on="Country Name", how="outer") # Outer merge keeps data that is in either

#TODO: use apply function to create new columns

pass # Use this placeholder line with a break to stop the program from completing