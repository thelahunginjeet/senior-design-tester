#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 18:33:34 2017

@author: fatirahmed
"""

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests

class attempter:
    def __init__(self, _company_name, _url):
        self.url = _url
        self.company_name = _company_name
        r = requests.get(self.url)
        self.data = r.text
        # self.create_lists()

    def start(self):
        self.create_lists()
        self.create_Panda()

    def create_lists(self):
        self.soup = bs(self.data, "lxml")
        self.cleantext = bs(self.data).text
        self.soup2 = bs(self.cleantext, "lxml")
        self.visible_text = self.extract_text()
        self.strdata = self.soup.prettify();
        strdata2 = self.soup2.prettify();
        self.FinalList = strdata2.split();
        self.FinalList2 = self.visible_text.split();
    def extract_text(self):
        [s.extract() for s in self.soup(['style', 'script', '[document]', 'head', 'title'])]
        visible_text = self.soup.getText()
        return visible_text
        
    def create_Panda(self):
        sample = {'Name': 'Zara', 'Age': 7, 'Class':self.FinalList2[3] }
        s = pd.Series(sample)
        self.pand=s
if __name__ == "__main__":
    attemp_=attempter('biogen','http://biogen.com/en_us/research-pipeline/biogen-pipeline.html')
    attemp_.start()
    something=attemp_.pand
    print(something )