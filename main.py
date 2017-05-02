# Imports
import requests
from google_bot import GoogleBot
from full_parser import FullParser
import pandas as pd
import sys
import re


def preprocess(company_name, pipeline_url):
    """
    This function takes each link and runs the parser on it.
    :param company_name: string
    :param pipeline_url: string
    :return: tuple
    """
    # Initializing variables and creating objects
    full_parser = FullParser(company_name, pipeline_url)
    flags = []

    # Getting scraped data
    current_drug_data_scrape_rate = round(full_parser.drug_data_scrape_rate)
    (found_link_pdf, the_link_pdf) = full_parser.feedback_link_info
    (found_link_pic, the_link_pic) = full_parser.feedback_pic_info


    # Checking if parser found any pdf or jpg links
    if found_link_pic:
        if current_drug_data_scrape_rate < 20:
            the_link = the_link_pic
            flags.append('Picture link provided')
    if found_link_pdf:
        the_link = the_link_pdf
        flags.append('PDF link provided')
    else:
        the_link = pipeline_url

    # Checking accuracy and appending flags
    if current_drug_data_scrape_rate > 0 and current_drug_data_scrape_rate < 20:
        flags.append('Data is not up to accuracy standards: ' + str(current_drug_data_scrape_rate))

    # Getting data
    print("scrape rate of ", company_name, ":", current_drug_data_scrape_rate)
    data_all = full_parser.final_drug_data_all
    data_high = full_parser.final_drug_data_high
    data_low = full_parser.final_drug_data_low

    if current_drug_data_scrape_rate == -1:
        flags.append('No data found on website!')
        data_all = [[company_name, company_name, ['!'], ['!'], ['!']]]
        data_high = data_all
        data_low = data_all

    return (data_all, data_high, data_low, the_link, flags)


""" START SCRIPT """

try:
    filename = sys.argv[1]
except IndexError:
    filename = 'company_names.txt'
except:
    print("Please fix the arguments entry!")


try:
    # Reading links from list
    with open(filename, 'r') as companyNames:
        company_names = companyNames.readlines()
        company_names = [x.strip() for x in company_names]
except FileNotFoundError:
    print("Please enter a valid file name!")
    sys.exit()

# Creating the Google Bot
google_bot = GoogleBot("pipeline")

# Initializing variables
total_all = []
total_high = []
total_low = []
log_entries = []
data_high = None
data_low = None
list_size = len(company_names)
counter = 0

# Getting the link and calling the process for each one
for company_name in company_names:
    if company_name == "":
        continue

    # Initializing variables
    flags = []
    the_link = []
    counter = counter + 1  # Counter

    print("")
    company_name = company_name.lower()  # Standardizing company names

    # Getting pipeline and feedback to the user
    pipeline_url = google_bot.find_pipeline(company_name)
    print("Processing " + str(counter) + "/" + str(list_size) + ": " + company_name)

    # Hard coding pfizer's recent change in pipeline url
    if company_name == "pfizer":
        pipeline_url = "http://www.pfizer.com/science/drug-product-pipeline"

    # Pattern to validate link
    p1 = re.compile(r"(.?)+pipeline(.?)+", re.I)
    p2 = re.compile(r"(.?)+product(.?)+", re.I)

    if not (re.match(p1, pipeline_url) or re.match(p2, pipeline_url)):  # If the url received is not the url
        data_all = [[company_name, company_name, ['!'], ['!'], ['!']]]
        the_link = pipeline_url  # Return defective link
        flags.append("Can't find pipeline or DNE!")  # Append flag
        print("No pipeline for " + company_name)
    else:
        # (data_all, data_high, data_low, the_link, flags) = preprocess(company_name, pipeline_url)
        try:
            (data_all, data_high, data_low, the_link, flags) = preprocess(company_name, pipeline_url)
        except:  # Catch all errors with the parser
            print('There was an error in the parser for this company: ' + company_name)
            data_all = [[company_name, company_name, ['!'], ['!'], ['!']]]
            the_link = pipeline_url
            flags = ['Error attempting to reach website!']

    # Adding extra rows and flags to data
    for drug_info in data_all:
        drug_info.append(flags)
        drug_info.append(the_link)
        total_all.append(drug_info)

    if not data_high is None:
        for drug_info_1 in data_high:
            total_high.append(drug_info_1)

    if not data_low is None:
        for drug_info_2 in data_low:
            total_low.append(drug_info_2)

    log_entry = [company_name, flags, the_link]
    log_entries.append(log_entry)


# OUTPUT TO CSV FILE
drug_data_all_df = pd.DataFrame(total_all)
drug_data_all_df.columns = ['Company Name', 'Product Name', 'Treatment Area', 'Phase', 'Mechanism of Action', 'Flags', 'Pipeline/PDF Url']
drug_data_all_df.to_csv('i_files/drug_data_all_cache.csv', sep='\t')

if len(total_high) > 0:
    drug_data_high_df = pd.DataFrame(total_high)
    drug_data_high_df.columns =  ['Company Name', 'Product Name', 'Treatment Area', 'Phase', 'Mechanism of Action', 'Flags', 'Pipeline/PDF Url']
    drug_data_high_df.to_csv('i_files/drug_data_high_cache.csv', sep='\t')

if len(total_low) > 0:
    drug_data_low_df = pd.DataFrame(total_low)
    drug_data_low_df.columns =  ['Company Name', 'Product Name', 'Treatment Area', 'Phase', 'Mechanism of Action', 'Flags', 'Pipeline/PDF Url']
    drug_data_low_df.to_csv('i_files/drug_data_low_cache.csv', sep='\t')

log_entry_df = pd.DataFrame(log_entries)
log_entry_df.columns = ['Company Name', 'Flags', 'Pipeline/PDF Url']
log_entry_df.to_csv('i_files/log_entries_cache.csv', sep='\t')

print("Completed Succesfully, open csv")
