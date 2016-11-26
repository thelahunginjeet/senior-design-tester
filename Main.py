from bs4 import BeautifulSoup
import requests

url = "https://www.biogen.com/en_us/research-pipeline/biogen-pipeline.html"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, "lxml")
strdata = soup.prettify();


def findnth(haystack, needle, n):
    parts = haystack.split(needle, n+1)
    if(len(parts) <= n+1):
        return -1;
    return len(haystack)-len(parts[-1])-len(needle)


def parseSpace(haystack, i):
    phase_data = findnth(haystack, "product-pipeline__products", i)
    if(phase_data == -1):
        return
    superstring = haystack[phase_data:phase_data+100]
    substrings = superstring.split()

    #Printing header
    print("")

    #Getting Name
    name_field = substrings[3]
    drug_name = (name_field[4:len(name_field)-2])
    print("Name: " + drug_name)

    #Getting Phase
    phase_data = substrings[1]
    phase_number = phase_data[len(phase_data)-1:]
    fixed_drug_name = phase_data[:len(phase_data)-1] + " " + phase_number
    print("Phase: " + fixed_drug_name)

    #Getting condition
    cond_data = substrings[2][13:len(substrings[2])-1]
    print("Mechanism: " + cond_data)

    if(phase_data == -1):
        return
    else:
        i += 2;

        if(i >= len(haystack)):
            return
        else:
            parseSpace(haystack, i)


parseSpace(strdata, 4)
