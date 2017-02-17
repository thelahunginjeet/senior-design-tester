# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 23:26:46 2017

@author: Siddhardha
"""
from google import search

class GoogleBot:
    
    keyword = ""
    
    def __init__(self, keyword_):
        self.keyword = keyword_
        
    def find_pipeline(self, company_name):
        search_term = company_name + " " + self.keyword
        count = 0;
        for url in search(search_term, stop=1):
            if count == 0:
                pipeline_url = url
            count += 1
        return pipeline_url
            
    