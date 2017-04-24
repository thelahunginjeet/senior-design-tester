# Imports
import requests
from google_bot import GoogleBot
from Gamma import FullParser
import pandas as pd
import re


def preprocess(company_name, pipeline_url):
    full_parser = FullParser(company_name, pipeline_url)

    current_drug_data_scrape_rate = round(full_parser.drug_data_scrape_rate)
    (found_link, the_link) = full_parser.feedback_link_info
    flags = []

    if current_drug_data_scrape_rate < 20:
        print("scrape rate of ", company_name, ":", current_drug_data_scrape_rate)
        data = [[company_name, company_name, ['!'], ['!'], ['!']]]
        if found_link:
            flags.append('PDF link provided')
        else:
            flags.append('Data is not up to accuracy standards: ' + str(current_drug_data_scrape_rate))
    else:
        print("scrape rate of ", company_name, ":", current_drug_data_scrape_rate)
        data = full_parser.final_drug_data_all

    return (data, found_link, flags)

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
    flags = []

    p1 = re.compile(r"(.?)+pipeline(.?)+", re.I)

    if not re.match(p1, pipeline_url):
        data = [[company_name, company_name, ['!'], ['!'], ['!']]]
        found_link = pipeline_url
        flags.append("Can't find pipeline or DNE!")
        print("No pipeline for " + company_name)
    else:
        # (data, found_link, flags) = preprocess(company_name, pipeline_url)


        try:
            (data, found_link, flags) = preprocess(company_name, pipeline_url)
        except:
            print('There was an error in the parser for this company: ' + company_name)
            data = [[company_name, company_name, ['!'], ['!'], ['!']]]
            found_link = pipeline_url
            flags = ['Error attempting to reach website!']

    for drug_info in data:
        drug_info.append(pipeline_url)
        drug_info.append(flags)
        total.append(drug_info)


df = pd.DataFrame(total)
# cols = ['Company Name', 'Product Name', 'Treatment Area', 'Phase', 'Mechanism of Action']
df.columns = ['Company Name', 'Product Name', 'Treatment Area', 'Phase', 'Mechanism of Action', 'Pipeline/PDF Url', 'Flags']
df.to_csv('drug_data_cache.csv', sep='\t')
print(df)
print("Completed Succesfully, open csv")
# print(df.head())
