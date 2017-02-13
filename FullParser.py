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
    drug_target="N/A"
    currentLast=len(currentCheck);
    if  "vir" in currentCheck:
        drug_target="Antiviral";
        return currentCheck
    elif "cillin" in currentCheck:
        drug_target="Penicillin-derived antibiotics";
        return currentCheck
    elif "cef" in currentCheck:
        drug_target="Cephem-type antibiotics";
        return currentCheck
        
    elif "ximab" in currentCheck:
        drug_target="Chimeric antibody";
        return currentCheck
    elif "zumab" in currentCheck:
        drug_target="humanized antibody";
        return currentCheck
    elif "mab" in currentCheck:
        drug_target="monoclonal antiboies";
        return currentCheck
    elif "tinib" in currentCheck:
        drug_target="tyrosine-kinase inhibitor";
        return currentCheck
    elif "vastatin" in currentCheck:
        return currentCheck
    elif "prazole" in currentCheck:
        return currentCheck
    elif "lukast" in currentCheck:
        return currentCheck
    elif "grel" in currentCheck:
        return currentCheck
    elif "axine" in currentCheck:
        return currentCheck
    elif "olol" in currentCheck:
        return currentCheck
    elif "oxetine" in currentCheck:
        return currentCheck
    elif "sartan" in currentCheck:
        return currentCheck
    elif "pril" in currentCheck:
        return currentCheck
    elif "oxacin" in currentCheck:
        return currentCheck
    elif "barb" in currentCheck:
        return currentCheck
    elif "xaban" in currentCheck:
        return currentCheck
    elif "afil" in currentCheck:
        return currentCheck
    elif "prost" in currentCheck:
        return currentCheck
    elif "ine" in currentCheck:
        return currentCheck
    elif "parib" in currentCheck:
        return currentCheck
    elif "tide" in currentCheck:
        return currentCheck
    elif "vastatin" in currentCheck:
        return currentCheck
    elif currentCheck[currentLast-1]=="1":
        return currentCheck
    elif currentCheck[currentLast-1]=="2":
        return currentCheck
    elif currentCheck[currentLast-1]=="0":
        return currentCheck
    elif currentCheck[currentLast-1]=="3":
        return currentCheck
    elif currentCheck[currentLast-1]=="4":
        return currentCheck
    elif currentCheck[currentLast-1]=="5":
        return currentCheck
    elif currentCheck[currentLast-1]=="6":
        return currentCheck
    elif currentCheck[currentLast-1]=="7":
        return currentCheck
    elif currentCheck[currentLast-1]=="8":
        return currentCheck
    elif currentCheck[currentLast-1]=="9":
        return currentCheck
    elif currentCheck[currentLast-1]=="0":
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

#http://www.roche.com/research_and_development/who_we_are_how_we_work/pipeline.html"
#https://www.biogen.com/en_us/research-pipeline/biogen-pipeline.html
#https://www.astrazeneca.com/our-science/pipeline.html
url = "http://www.roche.com/research_and_development/who_we_are_how_we_work/pipeline.html"
url_BaseLine = "https://www.biogen.com/en_us/research-pipeline/biogen-pipeline.html"
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
                        print('Processing...')
                    elif company_name in newstr:
                        print('Processing...')
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
        
