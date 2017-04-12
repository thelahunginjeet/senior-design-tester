# Imports
import requests
from google_bot import GoogleBot
from ra import FullParser


def preprocess(company_name, pipeline_url):
    print("Parsing...")
    full_parser = FullParser(company_name, pipeline_url)
    print("Parsed succesfully")

    print("Determining accuracy...")
    current_drug_data_scrape_rate = round(full_parser.drug_data_scrape_rate)
    if current_drug_data_scrape_rate < 50:
        print("WARNING: Data is not up to accuracy standards!")
    else:
        print("scrape rate of ", company_name, ":", current_drug_data_scrape_rate)



# Reading links from list
print("Reading company names...")
with open("company_names.txt", 'r') as companyNames:
    company_names = companyNames.readlines()
    company_names = [x.strip() for x in company_names]
print("List of company names imported succesfully")

# Creating the Google Bot
print("Establishing connection with Google Services...")
google_bot = GoogleBot("pipeline")

# Getting the link and calling the process for each one
for company_name in company_names:
    company_name = company_name.lower()

    print("Getting pipeline url...")
    pipeline_url = google_bot.find_pipeline(company_name)
    print(pipeline_url)

    preprocess(company_name, pipeline_url)
