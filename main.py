# Imports
import requests
from google_bot import GoogleBot
from beta_version import FullParser
import pandas as pd


def preprocess(company_name, pipeline_url):
    full_parser = FullParser(company_name, pipeline_url)

    current_drug_data_scrape_rate = round(full_parser.drug_data_scrape_rate)
    if current_drug_data_scrape_rate < 50:
        print("WARNING: Data is not up to accuracy standards!")
    else:
        print("scrape rate of ", company_name, ":", current_drug_data_scrape_rate)
        return full_parser.final_drug_data


""" START SCRIPT """

# Reading links from list
with open("company_names.txt", 'r') as companyNames:
    company_names = companyNames.readlines()
    company_names = [x.strip() for x in company_names]

# Creating the Google Bot
google_bot = GoogleBot("pipeline")

# Getting the link and calling the process for each one
total = []
for company_name in company_names:
    company_name = company_name.lower()

    pipeline_url = google_bot.find_pipeline(company_name)
    print(pipeline_url)

    temp = preprocess(company_name, pipeline_url)
    for drug_info in temp:
        # print(drug_info[3])
        total.append(drug_info)

df = pd.DataFrame(total)
cols = ['Company Name', 'Product Name', 'Treatment Area', 'Phase', 'Mechanism of Action']
df.columns = cols
df.to_csv('testingAlpha.csv', sep='\t')
# print(df)
print("Completed Succesfully, open csv")
