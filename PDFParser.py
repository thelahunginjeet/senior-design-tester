import re
from bs4 import BeautifulSoup as bs
import requests
import enchant
import pdftables_api

eng= enchant.Dict("en_US");

class PdfParser:

    def __init__(self):
        self.c = pdftables_api.Client('unr1ilqvoitk')

    def getPDF(self, url):
        self.r = requests.get(url)
        self.data = r.text
        self.soup = BeautifulSoup(data, "lxml")
        self.strdata = soup.prettify();

    def extract
