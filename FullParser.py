import re
from bs4 import BeautifulSoup as bs
import requests
import enchant
#import pdftables
eng= enchant.Dict("en_US");

def indices(lst, element):
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset+1)
        except ValueError:
            return result
        result.append(offset)


def checkingOfficical(currentCheck):
    p1 = re.compile(r"\b[A-Za-z]+(vir|cillin|mab|ximab|zumab|tinib|vastatin|prazole|lukast|axine|olol|oxetine|sartan|pril|oxacin|xaban|afil|ine|parib|tide)\b")
    p2 = re.compile(r"\b[A-Za-z]+(grel|barb|prost)[A-Za-z]+\b")
    p3 = re.compile(r"\b(cef)[A-Za-z]+\b")
    p4 = re.compile(r"[A-Z].+\d$")
    drug_target="N/A"
    currentLast=len(currentCheck);
    if  re.match(p1, currentCheck):
        return currentCheck
    elif re.match(p2, currentCheck):
        return currentCheck
    elif re.match(p3, currentCheck):
        return currentCheck
    elif re.match(p4, currentCheck):
        return currentCheck

    return "false", drug_target


def phaseFinder(drugWebsite, current_entry ):



    totalChecks=indices(drugWebsite,current_entry )
   # print(totalChecks)

    for q in range(0, len(totalChecks)):
        start=0;
        if totalChecks[q]>=55:
            start=totalChecks[q]-55
        else:
            start=0;
        end=totalChecks[q]+55
        for x in range(start, end):
             currentEntry=drugWebsite[x]
             futureEntry=drugWebsite[x+1]
             if futureEntry=="1":
                 return "phase 1"
             elif futureEntry=="2":
                return "phase 2"
             elif futureEntry=="3":
                return "phase 3"








    return "false"
def validatePhase(ComparisonHtml, drugTargetList):
    totalDuration=len(drugTargetList)
    validatedDrugs=[]
    for x in range(0, totalDuration):
        currentTruth=phaseFinder(ComparisonHtml,drugTargetList[x])
        if currentTruth!="false":
            adder=drugTargetList[x]+','+currentTruth
            validatedDrugs.append(adder)

    return validatedDrugs
#medicine= enchant("en-medical.multi");

# url = "http://www.roche.com/research_and_development/who_we_are_how_we_work/pipeline.html"
# url = "https://www.biogen.com/en_us/research-pipeline/biogen-pipeline.html"
# url = https://www.astrazeneca.com/our-science/pipeline.html"
url = "http://www.roche.com/research_and_development/who_we_are_how_we_work/pipeline.html"
# url_BaseLine = "https://www.biogen.com/en_us/research-pipeline/biogen-pipeline.html"
company_name="Biogen"
r = requests.get(url)
data = r.text
soup = bs(data, "lxml")




cleantext = bs(data).text
soup2 = bs(cleantext, "lxml")



[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
visible_text = soup.getText()



FirstFilter = []
strdata = soup.prettify();
strdata2 = soup2.prettify();
FinalList=strdata2.split();
FinalList2=visible_text.split();


temperaryString= "jk ><shifoa <AD''EAejg sHGSOLejd"
temperaryStringTwo= re.split('[<>/ "]',strdata);

#print(temperaryStringTwo)
#print(temperaryStringTwo)

#print(FinalList)

iterat=len(FinalList2)



for x in range(0, iterat):
    newstr4 = FinalList2[x].replace(",", "")
    newstr3 = newstr4.replace(":", "")
    newstr2 = newstr3.replace("<", "")
    newstr1 = newstr2.replace(">", "")
  #  newstr7 = newstr1.replace("'", "")
    newstr9 = newstr1.replace("]", "")
    newstr10 = newstr9.replace("[", "")
    newstr = newstr10.replace(")", "")
    #newstr = newstr10.replace("", "")





    sizeCheck=len(newstr)

    if sizeCheck!=0:

        appe=eng.check(newstr)

        if appe==False:
            temp=len(newstr)
            if temp>=5:
                temps=FinalList2.count(FinalList2[x])
                if temps>=2:
                    if "-" in newstr:
                        #Some sort of check to detemine what this really is
                        # print('Processing...')
                        pass
                    elif company_name in newstr:
                        # print('Processing...')
                        pass
                    elif "/" in newstr:
                        newstr.split("/")
                        permA=eng.check(newstr[0])
                        permB=eng.check(newstr[1])
                        if permA & permB==False:
                            news=checkingOfficical(newstr)
                            FirstFilter.append(news)

                    else:
                        news=checkingOfficical(newstr)
                        FirstFilter.append(news)

apple=eng.check(FinalList[x])
SecondFilter=list(set(FirstFilter))
'''
iterat2=len(FirstFilter)

iteratI=len(FinalList2)

for x in range(0, iterat2):
    for x in range(0, iteratI):
        if FirstFilter[iteratI]==FinalList2[iterat2]:
  '''





#print(FirstFilter)
#print(FinalList[5])
#print(FirstFilter)

print(SecondFilter)
print(phaseFinder(visible_text,'monalizumab'))
for x in range(0, len(SecondFilter)):
    print(SecondFilter[x])
    if SecondFilter[x]!=('false', 'N/A'):
        print(phaseFinder(visible_text,SecondFilter[x]))
