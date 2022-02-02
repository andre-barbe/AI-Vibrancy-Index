# Main program that does everything

import pandas as pd
import numpy as np

pass

# ===============Import raw data from Excel sheets of Vibrancy website files===============
# How to read from excel https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html
# Need to use engine option as described here: https://stackoverflow.com/questions/48066517/python-pandas-pd-read-excel-giving-importerror-install-xlrd-0-9-0-for-excel
version_year = 2022 #flag to import either the 2021 or 2022 version of the data
if version_year == 2021:
    data_raw_research = pd.read_excel("data/raw/MAG - 2021 AI Index Report (Main).xlsx", sheet_name="By CountryRegion", engine='openpyxl')
    data_raw_investment_amount = pd.read_excel("data/raw/NetBase Quid - 2021 AI Index Report.xlsx", sheet_name="Investment Amount", engine='openpyxl')
    data_raw_number_companies = pd.read_excel("data/raw/NetBase Quid - 2021 AI Index Report.xlsx", sheet_name="Number of Companies", engine='openpyxl')
    data_raw_ranking_2020 = pd.read_excel("data/raw/2020 Global Vibrancy Ranking - Absolute.xlsx", sheet_name="Data", engine='openpyxl')
if version_year == 2022:
    data_raw_citations = pd.read_csv("data/raw/2022 Report Data/Number of AI Citations.csv")
    data_raw_publications = pd.read_csv("data/raw/2022 Report Data/Number of AI Publications.csv")
    data_raw_investment_amount = pd.read_excel("data/raw/2022 Report Data/NetBase Data for Vibrancy Tool.xlsx", sheet_name="Private Investment Across Count", engine='openpyxl')
    data_raw_number_companies = pd.read_excel("data/raw/2022 Report Data/NetBase Data for Vibrancy Tool.xlsx", sheet_name="Newly Funded AI Companies Acros", engine='openpyxl')
    data_raw_ranking_2020 = pd.read_excel("data/raw/2020 Global Vibrancy Ranking - Absolute.xlsx", sheet_name="Data", engine='openpyxl')


# =============== Clean Data used in both version=====
data_ranking_2020 = data_raw_ranking_2020

# =============== Clean 2022 Data =====================
if version_year == 2022:
    # =============== Clean investment amount data ===============
    data_investment_amount = data_raw_investment_amount  # save raw investment data safely and only manipulate working data
    data_investment_amount = data_investment_amount[["Country", 2021]]  # Drop unnecessary variables
    data_investment_amount = data_investment_amount.rename(columns={2021: "Investment Amount"})  # rename investment amount
    data_investment_amount = data_investment_amount.rename(
        columns={"Country": "Country Name"})  # rename country name
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
    data_number_companies = data_number_companies[["Country", 2021]]  # Drop unnecessary variables
    data_number_companies = data_number_companies.rename(columns={2021: "Number of Companies"})
    data_number_companies = data_number_companies.rename(columns={"Country": "Country Name"})
    data_number_companies = data_number_companies.loc[
        # Drop if both the investment amount and country name is missing. loc is used to select rows. For some reason the raw import kept all these blank rows so I need to delete them
        ~pd.isna(data_number_companies["Number of Companies"]) | ~pd.isna(data_number_companies["Country Name"])
        # this selects rows if they have a country name or a investment value that is a number (ie , not isna). Note that I have to use ~ for not and | for or, as described here https://stackoverflow.com/questions/21415661/logical-operators-for-boolean-indexing-in-pandas
        ]
    data_number_companies = data_number_companies.loc[data_number_companies["Country Name"] != "Grand Total"]
    data_number_companies["Country Name"] = data_number_companies[
        "Country Name"].str.title()  # Capitalize all the same to make merging later easier


    # =============== Clean Citations data ===============
    data_citations = data_raw_citations
    data_citations = data_citations.rename(columns={"country":"Country Name", "doctype":"Doc Type", "year":"Publish Year", "num_citations":"Number of Citations"}) # rename variables # rename variables
    data_citations = data_citations[data_citations["Publish Year"] == 2021]  # Drop non-2021 data
    #Note that the 2021 version of the data uses *all* publications and does not directly, filter by field of study to just AI publications. that was already done by Daniel in the raw data
    data_citations = data_citations[["Country Name", "Doc Type", "Number of Citations"]]  # Drop unnecessary variables

    # =============== Clean Publication data ===============
    data_publications = data_raw_publications
    data_publications = data_publications.rename(columns={"country": "Country Name", "doctype":"Doc Type", "year":"Publish Year", "num_papers":"Number of Papers"}) # rename variables # rename variables
    data_publications = data_publications[data_publications["Publish Year"] == 2021]  # Drop non-2021 data
    #Note that the 2021 version of the data uses *all* publications and does not directly, filter by field of study to just AI publications that was already done.
    data_publications = data_publications[["Country Name", "Doc Type", "Number of Papers"]]  # Drop unnecessary variables


    # =============== Reshape research data ===============
    #data_research_long = data_publications.merge(data_citations, on=[["Country Name","Document Type"]], how="outer")
    data_research_long = pd.merge(data_publications, data_citations, on=["Country Name","Doc Type"])

    # Reshape research data from long to wide
    data_research_wide = data_research_long.pivot(index="Country Name", columns="Doc Type",
                                                  values=["Number of Papers",
                                                          "Number of Citations"])  # Learned how to do this here: https://www.datasciencemadesimple.com/reshape-long-wide-pandas-python-pivot-function/
    data_research = data_research_wide.reset_index()  # the pivot changed country name to the df index. This changes Country name from the df's index back to a variable
    data_research["Country Name"] = data_research["Country Name"].str.title()  # Capitalize all the same to make merging later easier

pass

# =============== Clean 2021 Data =====================
# =============== Filter research data ===============
if version_year == 2021:
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

# ============Create new variables and do analysis =======
# Prior steps were different in the 2021 and 2022 versions of the model but this will be used in all.
# =============== Merge various cleaned data ===============
data_main = data_number_companies.merge(data_investment_amount, on="Country Name",
                                        how="outer")  # Outer merge keeps data that is in either
data_main = data_main.merge(data_research, on="Country Name",
                            how="outer")
data_main = data_main.merge(data_ranking_2020, on="Country Name",
                            how="outer")  # Outer merge keeps data that is in either

pass

# =============== Clean the merged Data ===============
data_main = data_main.sort_values("Country Name")

data_main = data_main.loc[data_main["Country Name"] != "-"]
data_main = data_main.loc[data_main["Country Name"] != "None Listed"]
data_main = data_main.loc[~pd.isna(data_main["Country Name"])]  # Drop if country name is missing

# Create normalized version of variables
list_variables_to_normalize = list(data_main.drop(["Country Name","2020 Vibrancy Rank (only absolute metrics)"],axis=1)) # Create list of all variables except "Country Name" and the 2020 ranking. See https://stackoverflow.com/questions/29763620/how-to-select-all-columns-except-one-column-in-pandas
for variable_name in list_variables_to_normalize:
    data_main[''.join(variable_name) + " Normalized"] = 100 * data_main[variable_name].fillna(0) / data_main[variable_name].fillna(0).max() # Normalize values from 0 to 100. Replaces NaNs with 0 for calculation, but leaves NaNs in original columns

# Create new variable that lists the number of NaNs in normalized variables
data_main["Number NaN"]=data_main[list_variables_to_normalize].isnull().sum(axis=1) # Creates new column with number of NANs in each row. See https://stackoverflow.com/questions/30059260/python-pandas-counting-the-number-of-missing-nan-in-each-row

# Create my new indexes using each of the 3 weighting methods
list_normalized_variables = [''.join(variable_name) + " Normalized" for variable_name in list_variables_to_normalize] # Create list of normalized variable names
if version_year==2021:
    data_main["Index Equal Metric Weights"] = data_main[list_normalized_variables].mul([1,1,1,1,1,1,1,1,1,1]).sum(1) # Multiply by vector weights and then sums, as described here: https://stackoverflow.com/questions/47026517/multiply-rows-in-dataframe-then-sum-them-together-python
    data_main["Index Equal Pillar Weights"] = data_main[list_normalized_variables].mul([8/2,8/2,1,1,1,1,1,1,1,1]).sum(1) #There are 8 doc types, so research has a total weight of 8
    data_main["Index Andre Prefers"] = data_main[list_normalized_variables].mul([0,8,1,1,1,1,1,1,1,1]).sum(1) #There are 8 doc types, so research has a total weight of 8
if version_year==2022:
    data_main["Score 1 - No Citations, Equal Metrics"] = data_main[list_normalized_variables].mul([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]).sum(1) # Multiply by vector weights and then sums, as described here: https://stackoverflow.com/questions/47026517/multiply-rows-in-dataframe-then-sum-them-together-python
    data_main["Score 2 - No Citations, Equal Pillars"] = data_main[list_normalized_variables].mul([14/2,14/2,1,1,1,1,1,1,1,1,1,1,1,1,1,1]).sum(1) #There are 7 doc types and ctiation vs publ, so research has a total weight of 14
    data_main["Score 3 - With Citations, Equal Metrics"] = data_main[list_normalized_variables].mul([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]).sum(1) # Multiply by vector weights and then sums, as described here: https://stackoverflow.com/questions/47026517/multiply-rows-in-dataframe-then-sum-them-together-python
    data_main["Score 4 - With Citations, Equal Pillars"] = data_main[list_normalized_variables].mul([14/2,14/2,1,1,1,1,1,1,1,1,1,1,1,1,1,1]).sum(1) #There are 7 doc types and ctiation vs publ, so research has a total weight of 14


# Create rankings for each country
if version_year==2021:
    data_main[['Rank Equal Metric Weights', 'Rank Equal Pillar Weights','Rank Andre Prefers']] = data_main[['Index Equal Metric Weights','Index Equal Pillar Weights','Index Andre Prefers']].rank(ascending= False).astype(int) # Create rankings for each of the new weighting methods
    data_main = data_main.sort_values("Rank Equal Metric Weights") # Sort countries by ranking to make display easier
if version_year==2022:
    list_score_variables = data_main.columns[pd.Series(list(data_main)).str.contains("Score", na=False).tolist()] #Use NA=False so that for tuple variable names, it will be false. Lots of conversion between series and list. Very annoying. See https://pandas.pydata.org/docs/reference/api/pandas.Series.tolist.html and https://pandas.pydata.org/docs/reference/api/pandas.Series.str.match.html
    for variable_name in list_score_variables:
        data_main['Rank '+ variable_name] = data_main[variable_name].rank(ascending= False).astype(int) # Create rankings for each of the new weighting methods
    data_main = data_main.sort_values("Rank "+ list_score_variables[0]) # Sort countries by ranking to make display easier

# Calculate the max difference in Country Rank between the Various weighting schemes
if version_year==2021:
    data_main['Max Rank']= np.maximum(data_main['Rank Andre Prefers'],data_main['Rank Equal Pillar Weights'],data_main['Rank Equal Metric Weights']) #Need to use np maximum command for pairwise vector max, see https://stackoverflow.com/questions/51813621/pandas-series-pairwise-maximum
    data_main['Min Rank']= np.minimum(data_main['Rank Andre Prefers'],data_main['Rank Equal Pillar Weights'],data_main['Rank Equal Metric Weights'])
    data_main['Rank Difference Max'] = data_main['Max Rank'] - data_main['Min Rank']
if version_year==2022:
    list_rank_variables = data_main.columns[pd.Series(list(data_main)).str.contains("Rank", na=False).tolist()] #Use NA=False so that for tuple variable names, it will be false. Lots of conversion between series and list. Very annoying. See https://pandas.pydata.org/docs/reference/api/pandas.Series.tolist.html and https://pandas.pydata.org/docs/reference/api/pandas.Series.str.match.html
    data_main['Rank Difference Max'] = data_main[list_rank_variables].max(axis=1) - data_main[list_rank_variables].min(axis=1)

# Export results to CSV
data_main.to_csv("reports/vibrancy_data_main_" + str(version_year) + ".csv")

pass  # Use this placeholder line with a break to stop the program from completing
