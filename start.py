# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 23:49:06 2017

@author: Siddhardha
"""

from GoogleBot import GoogleBot

print("Extracting company names...")

with open("company_names.txt", 'r') as companyNames:
    company_names = companyNames.readlines()
    company_names = [x.strip() for x in company_names]
    
    
print("Creating Google bot...")
googleBot = GoogleBot("pipeline")

print("Extracting pipeline urls...")
for company_name in company_names:
    pipeline_url = googleBot.find_pipeline(company_name)
    print(company_name + ": " + pipeline_url)