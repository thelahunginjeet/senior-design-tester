import re
from bs4 import BeautifulSoup as bs
import requests
import enchant


class FullParser:
    eng= enchant.Dict("en_US")

    def __init__(self, _company_name, _url):
        self.url = _url
        self.company_name = _company_name
        r = requests.get(self.url)
        self.data = r.text
        self.create_lists()

    def start(self):
        self.create_lists()
        self.search_list()
        self.other_stuff()

    def create_lists(self):
        self.soup = bs(self.data, "lxml")
        cleantext = bs(self.data).text
        self.soup2 = bs(cleantext, "lxml")
        self.visible_text = self.extract_text()
        strdata = self.soup.prettify();
        strdata2 = self.soup2.prettify();
        self.FinalList = strdata2.split();
        self.FinalList2 = self.visible_text.split();

    def extract_text(self):
        [s.extract() for s in self.soup(['style', 'script', '[document]', 'head', 'title'])]
        visible_text = self.soup.getText()
        return visible_text

    def search_list(self):
        iterat=len(self.FinalList2)
        self. FirstFilter = []

        for x in range(0, iterat):
            newstr4 = self.FinalList2[x].replace(",", "")
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

                appe = self.eng.check(newstr)

                if appe==False:
                    temp=len(newstr)
                    if temp>=5:
                        temps=self.FinalList2.count(self.FinalList2[x])
                        if temps>=1:
                            if "-" in newstr:
                                #Some sort of check to detemine what this really is
                                print('Processing...')
                            elif company_name in newstr:
                                print('Processing...')
                            elif "/" in newstr:
                                newstr.split("/")
                                permA=self.eng.check(newstr[0])
                                permB=self.eng.check(newstr[1])
                                if permA & permB==False:
                                    news=self.checkingOfficical(newstr)
                                    self.FirstFilter.append(news)

                            else:
                                news=self.checkingOfficical(newstr)
                                self.FirstFilter.append(news)

        #apple=eng.check(FinalList[x])
        self.SecondFilter=list(set(self.FirstFilter))

    def other_stuff(self):
        print(self.SecondFilter)
        print(self.phaseFinder(self.visible_text,'Dapirolizumab'))
        for x in range(0, len(self.SecondFilter)):
            print(self.SecondFilter[x])
            if self.SecondFilter[x]!=('false', 'N/A'):
                print(self.phaseFinder(self.FinalList2,self.SecondFilter[x]))

        #print(nearbySearch(FinalList2,"emtricitabine"))
        #apples=['AZD9567', 'MEDI9314']

        print(self.LousyFilter('Tanezumab', self.data ))

    def indices(self, lst, element):
        result = []
        offset = -1
        while True:
            try:
                offset = lst.index(element, offset+1)
            except ValueError:
                return result
            result.append(offset)

    def checkingOfficical(self, currentCheck):
        pattern1=re.compile('^[A-Z].+\d')
        a=pattern1.findall(currentCheck)
        lengths=len(a)
        drug_target="N/A"
        currentLast=len(currentCheck);
        if  lengths>0:
            drug_target="Some Weird Number Thing";
            return currentCheck
        elif  "vir" in currentCheck:
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


        return "false", drug_target


    def phaseFinder(self, drugWebsite, current_entry ):

        bob=[]

        totalChecks = self.indices(drugWebsite,current_entry )
       # print(totalChecks)

        for q in range(0, len(totalChecks)):
            bob=[]
            start=0;
            joe=0
            if totalChecks[q]>=15:
                start=totalChecks[q]-15
            else:
                start=0;
            end=totalChecks[q]+15
            for x in range(start, end):

                 currentEntry=drugWebsite[x]
                 futureEntry=drugWebsite[x+1]
                 pattern1=re.compile('^[Phase]')
                 pattern2=re.compile('^[phase]')
                 a=pattern1.findall(currentEntry)
                 lengths=len(a)
                 b=pattern2.findall(currentEntry)
                 lengthsb=len(b)
                 bob.append(drugWebsite[99])
                 if 'Phase' in currentEntry:
                     if '3' in currentEntry:
                         return 3
                     elif '3' in futureEntry:
                         return 3
                     if '1' in currentEntry:
                         return 1
                     elif '1' in futureEntry:
                         return 1
                     if '2' in currentEntry:
                         return 2
                     elif '2' in futureEntry:
                         return 2
                     else :
                         return 7


        return "false"

    def validatePhase(self, ComparisonHtml, drugTargetList):
        totalDuration=len(drugTargetList)
        validatedDrugs=[]
        for x in range(0, totalDuration):
            currentTruth=phaseFinder(ComparisonHtml,drugTargetList[x])
            if currentTruth!="false":
                adder=drugTargetList[x]+','+currentTruth
                validatedDrugs.append(adder)

        return validatedDrugs

    def nearbySearch(self, drugWebsite, current_entry):
        totalChecks=indices(drugWebsite,current_entry )
        entry=[]
        entry2=[]
        for q in range(0, len(totalChecks)):
            start=0;
            if totalChecks[q]>=20:
                start=totalChecks[q]-20
            else:
                start=0;
            end=totalChecks[q]+20
            for x in range(start, end):
                 currentEntry=drugWebsite[x]
                 futureEntry=drugWebsite[x+1]
                 entry.append(currentEntry)

        return entry, entry2

    def advancedFilter(self, drugWebsite, current_entry):
        totalChecks=indices(drugWebsite,current_entry )
        entry=[]
        entry2=[]
        for q in range(0, len(totalChecks)):
            start=0;
            if totalChecks[q]>=10:
                start=totalChecks[q]-10
            else:
                start=0;
            end=totalChecks[q]+10
            for x in range(start, end):
                 currentEntry=drugWebsite[x]
                 futureEntry=drugWebsite[x+1]
                 if currentEntry=="treatment":
                     if futureEntry=="of":

                         for y in range(x+1, x+5):
                             entry2.append(drugWebsite[y])
        return entry, entry2

    def LousyFilter(self, drugWebsite, current_entry):
        #This filter parameter serves primarily as a last resort in case there are
        #high rates of failure
        app=current_entry.split();
        lengthing=len(app)

        for qur in range(0, lengthing-2):

            if 'BIIB067' in app[qur]:

                if 'phase' in app[qur]:
                    return 'phase'
                elif 'phase' in app[qur+1]:
                    if '1' in app[qur+1]:
                        return 'phase 1'
                    elif '2' in app[qur+1]:
                        return 'phase2'
                elif 'phase' in app[qur+2]:
                    return 'phase'
                elif 'phase' in app[qur+3]:
                    return 'phase'

        return 'failure'

# Any testing code goes here
if __name__ == "__main__":
    # This function will return possible treatments
    # medicine= enchant("en-medical.multi");

    url = "http://www.roche.com/research_and_development/who_we_are_how_we_work/pipeline.html"
    # url = "https://www.biogen.com/en_us/research-pipeline/biogen-pipeline.html"
    # url = "https://www.astrazeneca.com/our-science/pipeline.html"
    # url = "https://www.lilly.com/pipeline/"
    company_name = "Roche"

    full_parser = FullParser(company_name, url)
    full_parser.start()
