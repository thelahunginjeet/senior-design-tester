# Imports
import requests
from google_bot import GoogleBot
from ra import FullParser


def preprocess(company_name, pipeline_url):
    full_parser = FullParser(company_name, pipeline_url)
    full_parser.start()





# Reading links from list
with open("company_names.txt", 'r') as companyNames:
    company_names = companyNames.readlines()
    company_names = [x.strip() for x in company_names]

google_bot = GoogleBot("pipeline")

for company_name in company_names:
    company_name = company_name.lower()
    pipeline_url = google_bot.find_pipeline(company_name)
    preprocess(company_name, pipeline_url)
