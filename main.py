# Imports
import requests
from google_bot import GoogleBot
from full_parser import FullParser
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


    return (data, the_link, flags)


""" START SCRIPT """

# Reading links from list
with open("company_names.txt", 'r') as companyNames:
    company_names = companyNames.readlines()
    company_names = [x.strip() for x in company_names]

# Creating the Google Bot
google_bot = GoogleBot("pipeline")

# Getting the link and calling the process for each one
total = []
log_entries = []
for company_name in company_names:
    company_name = company_name.lower()

    pipeline_url = google_bot.find_pipeline(company_name)
    print(pipeline_url)
    flags = []
    the_link = []

    p1 = re.compile(r"(.?)+pipeline(.?)+", re.I)

    if not re.match(p1, pipeline_url):
        data = [[company_name, company_name, ['!'], ['!'], ['!']]]
        the_link = pipeline_url
        flags.append("Can't find pipeline or DNE!")
        print("No pipeline for " + company_name)
    else:
        # (data, found_link, flags) = preprocess(company_name, pipeline_url)
        try:
            (data, the_link, flags) = preprocess(company_name, pipeline_url)
            # try:
            #     (data, the_link, flags) = preprocess(company_name, pipeline_url)
            # except:
            #     print("Checking next link!")
            #     (data, the_link, flags) = preprocess(company_name, pipeline_url)
        except:
            print('There was an error in the parser for this company: ' + company_name)
            data = [[company_name, company_name, ['!'], ['!'], ['!']]]
            the_link = pipeline_url
            flags = ['Error attempting to reach website!']

    for drug_info in data:
        drug_info.append(the_link)
        drug_info.append(flags)
        total.append(drug_info)

    log_entry = [company_name, flags, the_link]
    log_entries.append(log_entry)


drug_data_df = pd.DataFrame(total)
drug_data_df.columns = ['Company Name', 'Product Name', 'Treatment Area', 'Phase', 'Mechanism of Action', 'Pipeline/PDF Url', 'Flags']
drug_data_df.to_csv('drug_data_cache.csv', sep='\t')
# print(drug_data_df)

log_entry_df = pd.DataFrame(log_entries)
log_entry_df.columns = ['Company Name', 'Flags', 'Pipeline/PDF Url']
log_entry_df.to_csv('log_entries_cache.csv', sep='\t')
print(log_entry_df)

print("Completed Succesfully, open csv")
# print(df.head())
