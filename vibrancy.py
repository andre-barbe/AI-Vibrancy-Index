# Main program that does everything

import pandas as pd
import numpy as np

# ===============Import raw data from Excel sheets of Vibrancy website files===============
# How to read from excel https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html
# Need to use engine option as described here: https://stackoverflow.com/questions/48066517/python-pandas-pd-read-excel-giving-importerror-install-xlrd-0-9-0-for-excel
version_year = 2021 #flag to import either the 2021 or 2022 version of the data
if version_year == 2021:
    data_raw_research = pd.read_excel("data/raw/MAG - 2021 AI Index Report (Main).xlsx", sheet_name="By CountryRegion", engine='openpyxl')
    data_raw_investment_amount = pd.read_excel("data/raw/NetBase Quid - 2021 AI Index Report.xlsx", sheet_name="Investment Amount", engine='openpyxl')
    data_raw_number_companies = pd.read_excel("data/raw/NetBase Quid - 2021 AI Index Report.xlsx", sheet_name="Number of Companies", engine='openpyxl')
    data_raw_ranking_2020 = pd.read_excel("data/raw/2020 Global Vibrancy Ranking - Absolute.xlsx", sheet_name="Data", engine='openpyxl')
if version_year == 2022:
    #TODO: improt citation data
    #TODO: import publication data
    data_raw_investment_amount = pd.read_excel("data/raw/2022 Report Data/NetBase Data for Vibrancy Tool.xlsx", sheet_name="Private Investment Across Count", engine='openpyxl')
    data_raw_number_companies = pd.read_excel("data/raw/2022 Report Data/NetBase Data for Vibrancy Tool.xlsx", sheet_name="Newly Funded AI Companies Acros", engine='openpyxl')
    data_raw_ranking_2020 = pd.read_excel("data/raw/2020 Global Vibrancy Ranking - Absolute.xlsx", sheet_name="Data", engine='openpyxl')

#TODO: revise rest of code to use the 2022 data
# =============== Filter research data ===============
data_research = data_raw_research
data_research = data_research[data_research["Publish Year"] == 2020]  # Drop non-2020 data
data_research = data_research[data_research["Field of Study"] == "Artificial intelligence"]  # Drop non-AI data
# TODO: Change to collapse. I just don't know how to do that yet # Collapse number of papers or citations, by field of study
data_research = data_research[["Country Name", "Doc Type", "Number of Papers","Number of Citations"]]  # Drop unnecessary variables

# =============== Reshape research data ===============
data_research_long = data_research  # rename wide to be clear
# Reshape research data from long to wide
data_research_wide = data_research_long.pivot(index="Country Name", columns="Doc Type",
                                                      values=["Number of Papers","Number of Citations"])  # Learned how to do this here: https://www.datasciencemadesimple.com/reshape-long-wide-pandas-python-pivot-function/
data_research = data_research_wide.reset_index()  # the pivot changed country name to the df index. This changes Country name from the df's index back to a variable
data_research["Country Name"] = data_research["Country Name"].str.title()  # Capitalize all the same to make merging later easier

# =============== Clean investment amount data ===============
data_investment_amount = data_raw_investment_amount  # save raw investment data safely and only manipulate working data
data_investment_amount = data_investment_amount[["Target Location ", 2020]]  # Drop unnecessary variables
data_investment_amount = data_investment_amount.rename(columns={2020: "Investment Amount"})  # rename investment amount
data_investment_amount = data_investment_amount.rename(
    columns={"Target Location ": "Country Name"})  # rename country name
data_investment_amount = data_investment_amount.loc[
    # Drop if both the investment amount and country name is missing. loc is used to select rows. For some reason the
    # raw import kept all these blank rows so I need to delete them
    ~pd.isna(data_investment_amount["Investment Amount"]) | ~pd.isna(data_investment_amount["Country Name"])
    # this selects rows if they have a country name or a investment value that is a number (ie , not isna). Note that
    # I have to use ~ for not and | for or, as described here
    # https://stackoverflow.com/questions/21415661/logical-operators-for-boolean-indexing-in-pandas
    ]
data_investment_amount = data_investment_amount.loc[data_investment_amount["Country Name"] != "Grand Total"]
data_investment_amount["Country Name"] = data_investment_amount[
    "Country Name"].str.title()  # Capitalize all the same to make merging later easier

# =============== Clean number of companies data ===============
data_number_companies = data_raw_number_companies
data_number_companies = data_number_companies[["Target Location", 2020]]  # Drop unnecessary variables
data_number_companies = data_number_companies.rename(columns={2020: "Number of Companies"})
data_number_companies = data_number_companies.rename(columns={"Target Location": "Country Name"})
data_number_companies = data_number_companies.loc[
    # Drop if both the investment amount and country name is missing. loc is used to select rows. For some reason the raw import kept all these blank rows so I need to delete them
    ~pd.isna(data_number_companies["Number of Companies"]) | ~pd.isna(data_number_companies["Country Name"])
    # this selects rows if they have a country name or a investment value that is a number (ie , not isna). Note that I have to use ~ for not and | for or, as described here https://stackoverflow.com/questions/21415661/logical-operators-for-boolean-indexing-in-pandas
    ]
data_number_companies = data_number_companies.loc[data_number_companies["Country Name"] != "Grand Total"]
data_number_companies["Country Name"] = data_number_companies[
    "Country Name"].str.title()  # Capitalize all the same to make merging later easier

# =============== Clean 2020 raking data ===============
data_ranking_2020 = data_raw_ranking_2020

# =============== Merge various cleaned data ===============
data_main = data_number_companies.merge(data_investment_amount, on="Country Name",
                                        how="outer")  # Outer merge keeps data that is in either
data_main = data_main.merge(data_research, on="Country Name",
                            how="outer")
data_main = data_main.merge(data_ranking_2020, on="Country Name",
                            how="outer")  # Outer merge keeps data that is in either

# =============== Clean the merged Data ===============
data_main = data_main.sort_values("Country Name")

data_main = data_main.loc[data_main["Country Name"] != "-"]
data_main = data_main.loc[data_main["Country Name"] != "None Listed"]
data_main = data_main.loc[~pd.isna(data_main["Country Name"])]  # Drop if country name is missing
# data_main = data_main.dropna() ##Drop entries that contain any missing values

# Create normalized version of variables
list_variables_to_normalize = list(data_main.drop(["Country Name","2020 Vibrancy Rank (only absolute metrics)"],axis=1)) # Create list of all variables except "Country Name" and the 2020 ranking. See https://stackoverflow.com/questions/29763620/how-to-select-all-columns-except-one-column-in-pandas
for variable_name in list_variables_to_normalize:
    data_main[''.join(variable_name) + " Normalized"] = 100 * data_main[variable_name].fillna(0) / data_main[variable_name].fillna(0).max() # Normalize values from 0 to 100. Replaces NaNs with 0 for calculation, but leaves NaNs in original columns

# Create new variable that lists the number of NaNs in normalized variables
data_main["Number NaN"]=data_main[list_variables_to_normalize].isnull().sum(axis=1) # Creates new column with number of NANs in each row. See https://stackoverflow.com/questions/30059260/python-pandas-counting-the-number-of-missing-nan-in-each-row

# Create my new indexes using each of the 3 weighting methods
list_normalized_variables = [''.join(variable_name) + " Normalized" for variable_name in list_variables_to_normalize] # Create list of normalized variable names
data_main["Index Equal Metric Weights"] = data_main[list_normalized_variables].mul([1,1,1,1,1,1,1,1,1,1]).sum(1) # Multiply by vector weights and then sums, as described here: https://stackoverflow.com/questions/47026517/multiply-rows-in-dataframe-then-sum-them-together-python
data_main["Index Equal Pillar Weights"] = data_main[list_normalized_variables].mul([2,2,1,1,1,1,1,1,1,1]).sum(1)
data_main["Index Andre Prefers"] = data_main[list_normalized_variables].mul([0,4,1,1,1,1,1,1,1,1]).sum(1)

# Create rankings for each country
data_main[['Rank Equal Metric Weights', 'Rank Equal Pillar Weights','Rank Andre Prefers']] = data_main[['Index Equal Metric Weights','Index Equal Pillar Weights','Index Andre Prefers']].rank(ascending= False).astype(int) # Create rankings for each of the new weighting methods
data_main = data_main.sort_values("Rank Equal Metric Weights") # Sort countries by ranking to make display easier

# Calculate the max difference in Country Rank between the Various weighting schemes
data_main['Rank Difference Max'] = np.maximum(
    np.maximum( #Need to use np maximum command for pairwise vector max, see https://stackoverflow.com/questions/51813621/pandas-series-pairwise-maximum
        abs(data_main['Rank Andre Prefers']-data_main['Rank Equal Pillar Weights']),
        abs(data_main['Rank Andre Prefers']-data_main['Rank Equal Metric Weights'])
    ),
    abs(data_main['Rank Equal Metric Weights']-data_main['Rank Equal Pillar Weights'])
)

# Export results to CSV
data_main.to_csv("data/processed/vibrancy_data_main.csv")
data_main.to_csv("reports/vibrancy_data_main.csv")

pass  # Use this placeholder line with a break to stop the program from completing
