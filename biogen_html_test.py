from bs4 import BeautifulSoup
import requests

url = "https://www.biogen.com/en_us/research-pipeline/biogen-pipeline.html"
r = requests.get(url)

data = r.text

soup = BeautifulSoup(data)

strdata = soup.prettify();

if 'phase' in strdata:
    print ('false')


print (strdata.find("phase"))
