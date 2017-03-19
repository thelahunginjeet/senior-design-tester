# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import re
from bs4 import BeautifulSoup as bs
import requests
import enchant
import pandas

class FullParser:
    eng= enchant.Dict("en_US")

    def __init__(self, _company_name, _url):
        self.url = _url
        self.company_name = _company_name
        r = requests.get(self.url)
        self.data = r.text
        # self.create_lists()

    def start(self):
        self.create_lists()
        self.search_list()
        self.other_stuff()

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
                            if company_name in newstr:
                               # print('Processing...')
                                pass
                            elif "/" in newstr:
                                newstr.split("/")
                                permA=self.eng.check(newstr[0])
                                permB=self.eng.check(newstr[1])
                                if permA & permB==False:
                                    news=self.checking_official(newstr)
                                    if news!='null':
                                        self.FirstFilter.append(news)

                            else:
                                news=self.checking_official(newstr)
                                if news!='null':
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
                self.BlockBreaker(self.FinalList2,self.SecondFilter[x] )

        #print(nearbySearch(FinalList2,"emtricitabine"))
        #apples=['AZD9567', 'MEDI9314']
        #print(advancedFilter(FinalList2,'LY3009806'))
        print(self.LousyFilter('AZD3293', self.data ))
        self.BlockBreaker(self.FinalList2,'AZD3293' )

    def indices(self, lst, element):
        result = []
        offset = -1
        while True:
            try:
                offset = lst.index(element, offset+1)
            except ValueError:
                return result
            result.append(offset)

    def checking_official(self, currentCheck):
        p1 = re.compile(r"\b[A-Za-z]+(vir|cillin|mab|ximab|zumab|tinib|vastatin|prazole|lukast|axine|olol|oxetine|sartan|pril|pib|oxacin|xaban|afil|ine|parib|tide)\b")
        p2 = re.compile(r"\b[A-Za-z]+(grel|barb|prost)[A-Za-z]+\b")
        p3 = re.compile(r"\b(cef)[A-Za-z]+\b")
        p4 = re.compile(r"[A-Z].+\d$")
        drug_target="N/A"
        currentLast=len(currentCheck);

        if re.match(p1, currentCheck): # Suffix testing
            return currentCheck
        elif re.match(p2, currentCheck): # Infix testing
            return currentCheck
        elif re.match(p3, currentCheck): # Prefix testing
            return currentCheck
        elif re.match(p4, currentCheck): # Number ending
            drug_target="Some Weird Number Thing"
            return currentCheck

        return 'null'

    # kept this because there is some drug info yet to be transferred
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

    def reiteratedPhases(self, drugEntry):
        if 'phase' in drugEntry:
            return True
        elif 'Phase' in drugEntry:
            return True
        elif 'PHASE' in drugEntry:
            return True
        elif 'phase2' in drugEntry:
            return True
        else:
            return False

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
                 if self.reiteratedPhases(currentEntry)==True:
                     if '3' in currentEntry:
                         return 'phase 3'
                     elif '3' in futureEntry:
                         return 'phase 3'
                     if '1' in currentEntry:
                         return 'phase 1'
                     elif '1' in futureEntry:
                         return 'phase 1'
                     if '2' in currentEntry:
                         return 'phase 2'
                     elif '2' in futureEntry:
                         return 'phase 2'
                     if 'III' in currentEntry:
                         return 3
                     elif 'III' in futureEntry:
                         return 3
                     elif 'lll' in futureEntry:
                         return 3
                     if 'II' in currentEntry:
                         return 2
                     elif 'II' in futureEntry:
                         return 2
                     elif 'll' in futureEntry:
                         return 2
                     if 'I' in currentEntry:
                         return 'phase 1'
                     elif 'I' in futureEntry:
                         return 'phase 1'

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

    def BlockBreaker(self, drugWebsite, current_entry):
        bob=[]
        baselines=[]
        pwl = enchant.request_pwl_dict("medical.txt")

        totalChecks = self.indices(drugWebsite,current_entry )
       # print(totalChecks)

        for q in range(0, len(totalChecks)):

            start=0;
            joe=0
            if totalChecks[q]>=15:
                start=totalChecks[q]-15
            else:
                start=0;
            end=totalChecks[q]+15
            for x in range(start, end):
                truths=pwl.check(drugWebsite[x])
                baselines.append(drugWebsite[x])
                if truths==True:
                    bob.append(drugWebsite[x])
        print(bob)
        
    def BetterBreak(self, drugWebsite, current_entry, indexNumber):
        bob=[]
        baselines=[]
        pwl = enchant.request_pwl_dict("medical.txt")
        start=0;
        joe=0
        if indexNumber>=11:
                start=indexNumber-11
        else:
                start=0;
        end=indexNumber+15
        for x in range(start, end):
            truths=pwl.check(drugWebsite[x])
            baselines.append(drugWebsite[x])
            if truths==True:
                bob.append(drugWebsite[x])
            
        return bob
    def BestBreakA(self, drugWebsite, current_entry, indexNumber):
        bob=[]
        baselines=[]
        pwl = enchant.request_pwl_dict("medical.txt")
        start=0;
        joe=0
        if indexNumber>=11:
                start=indexNumber-11
        else:
                start=0;
        end=indexNumber+15
        for x in range(indexNumber, end):
            if self.checking_official(drugWebsite[x+1])=='null':
                truths=pwl.check(drugWebsite[x])
                baselines.append(drugWebsite[x])
                if truths==True:
                    bob.append(drugWebsite[x])
            else:
                break
                
                    
        for x in range(1, 10):
            if self.checking_official(drugWebsite[indexNumber-x])=='null':
                truths=pwl.check(drugWebsite[indexNumber-x])
                baselines.append(drugWebsite[indexNumber-x])
                if truths==True:
                
                    bob.append(drugWebsite[indexNumber-x])
            else:
                break
            
        return bob
    def UltimateBreak(self, drugWebsite, current_entry, indexNumber):
         #This breaker will achieve the best result by attempting to 
         #filter out the drug names based om prior entries. IT will scout only 
         # a minimum distance in either direction 
         
        bob=[]
        baselines=[]
        pwl = enchant.request_pwl_dict("medical.txt")
        start=0;
        joe=0
        if indexNumber>=3:
                start=indexNumber-3
        else:
                start=0;
        end=indexNumber+4
        for x in range(start, end):
            truths=pwl.check(drugWebsite[x])
            baselines.append(drugWebsite[x])
            if truths==True:
                bob.append(drugWebsite[x])
            
        return bob
    def BestBreak(self, drugWebsite, current_entry, indexNumber,futureEntry):
        bob=[]
        baselines=[]
        pwl = enchant.request_pwl_dict("medical.txt")
        start=0;
        joe=0
        if indexNumber>=2:
                start=indexNumber-2
        else:
                start=0;
        end=indexNumber+5
        for x in range(start, end):
           
            truths=pwl.check(drugWebsite[x])
            baselines.append(drugWebsite[x])
            if truths==True:
                bob.append(drugWebsite[x])
            if futureEntry in drugWebsite[x]:
                return bob
        return bob
    def PhaseDiognostic(self,drugWebsite, current_entry, indexNumber ):
        bob=[]
        start=0;
        joe=0
        if indexNumber>=15:
            start=indexNumber-15
        else:
            start=0;
        end=indexNumber+15
        for x in range(start, end):

                 currentEntry=drugWebsite[x]
                 futureEntry=drugWebsite[x+1]
                 pattern1=re.compile('^[Phase]')
                 pattern2=re.compile('^[phase]')
                 a=pattern1.findall(currentEntry)
                 lengths=len(a)
                 b=pattern2.findall(currentEntry)
                 lengthsb=len(b)
                 #bob.append(drugWebsite[99])
                 if self.reiteratedPhases(currentEntry)==True:
                     if 'phase3' in currentEntry:
                         return 'phase 3'
                     elif 'phase3' in futureEntry:
                         return 'phase 3'
                     if 'phase1' in currentEntry:
                         return 'phase 1'
                     elif 'phase1' in futureEntry:
                         return 'phase 1'
                     if 'phase2' in currentEntry:
                         return 'phase 2'
                     elif 'phase2' in futureEntry:
                         return 'phase 2'
                     if '3' in currentEntry:
                         return 'phase 3'
                     elif '3' in futureEntry:
                         return 'phase 3'
                     if '1' in currentEntry:
                         return 'phase 1'
                     elif '1' in futureEntry:
                         return 'phase 1'
                     if '2' in currentEntry:
                         return 'phase 2'
                     elif '2' in futureEntry:
                         return 'phase 2'
                     if 'III' in currentEntry:
                         return 3
                     elif 'III' in futureEntry:
                         return 3
                     if 'II' in currentEntry:
                         return 2
                     elif 'II' in futureEntry:
                         return 2
                     if 'I' in currentEntry:
                         return 'phase 1'
                     elif 'I' in futureEntry:
                         return 'phase 1'
                     elif 'P1' in currentEntry:
                         return 'phase 1'
                     elif 'P2' in currentEntry:
                         return 'phase 2'
                     elif 'P3' in currentEntry:
                         return 'phase 3'

                     else :
                         return False
        return False
   
    def AdjasuntCheck(self, drugWebsite, current_entry, indexNumber):
        #Check for adjacunt drug names and combine if appropriate
        bob=[]
        baselines=[]
        pwl = enchant.request_pwl_dict("medical.txt")
        start=0;
        joe=0
        if indexNumber>=2:
                start=indexNumber-2
        else:
                start=0;
        end=indexNumber+2
        for x in range(start, end):
            truths=pwl.check(drugWebsite[x])
            baselines.append(drugWebsite[x])
            if truths==True:
                bob.append(drugWebsite[x])
        print(bob)
    def LousyHelper():
        return 'false'

    def LousyFilter(self, drugWebsite, current_entry):
        #This filter parameter serves primarily as a last resort in case there are
        #high rates of failure
        app=drugWebsite.split();
        lengthing=len(app)

        for qur in range(0, lengthing-2):
         

            if current_entry in app[qur]:

                if 'phase' in app[qur]:
                    if 'III' in app[qur]:
                        return 'phase3'
                    elif 'II' in app[qur]:
                        return 'phase2'
                    elif 'I' in app[qur]:
                        return 'phase1'
                    elif '1' in app[qur]:
                        return 'phase1'
                    elif '2' in app[qur]:
                        return 'phase2'
                    elif '3' in app[qur]:
                        return 'phase3'
                    return'nope'
                    
                elif 'phase' in app[qur+1]:
                    if 'III' in app[qur]:
                        return 'phase3'
                    elif 'II' in app[qur]:
                        return 'phase2'
                    elif 'I' in app[qur]:
                        return 'phase1'
                    elif '1' in app[qur]:
                        return 'phase1'
                    elif '2' in app[qur]:
                        return 'phase2'
                    elif '3' in app[qur]:
                        return 'phase3'
                    return'nope'
                    
                elif 'phase' in app[qur+2]:
                    if 'III' in app[qur+2]:
                        return 'phase3'
                    elif 'II' in app[qur+2]:
                        return 'phase2'
                    elif 'I' in app[qur+2]:
                        return 'phase1'
                    elif '1' in app[qur+2]:
                        return 'phase1'
                    elif '2' in app[qur+2]:
                        return 'phase2'
                    elif '3' in app[qur+2]:
                        return 'phase3'
                    return'nope'
                
                    
                elif 'phase' in app[qur+3]:
                    if 'III' in app[qur+3]:
                        return 'phase3'
                    elif 'II' in app[qur+3]:
                        return 'phase2'
                    elif 'I' in app[qur+3]:
                        return 'phase1'
                    elif '1' in app[qur+3]:
                        return 'phase1'
                    elif '2' in app[qur+3]:
                        return 'phase2'
                    elif '3' in app[qur+3]:
                        return 'phase3'
                    return'nope'

        return 'False'
    def HighPrecisionFilter(self, drugWebsite, current_entry):
        phaseing='Unknown'
        presetValue=''
        presetValues=[]
        for q in range(0, len(drugWebsite)):
            if current_entry in drugWebsite[q]:
                phaseing=self.PhaseDiognostic(drugWebsite,current_entry, q)
                presetValue=self.BetterBreak(drugWebsite, current_entry, q)
                
                if presetValue!=[]:
                    presetValues.append(presetValue)
        presetValue=[]
        for u in range(0, len(presetValues)): 
            presetValue=presetValues[u]
        HighPEntry=[self.company_name,current_entry,presetValue,phaseing]
        return HighPEntry
    def HighPrecisionPhase(self, drugWebsite, current_entry):
        phaseInfo=False
        presetValue=''
        presetValues=[]
        randsc=[]
        for q in range(0, len(drugWebsite)):
            if current_entry in drugWebsite[q]:
                randsc.append(drugWebsite[q])
                phaseInfo=self.PhaseDiognostic(drugWebsite,current_entry, q)
                presetValue=self.BetterBreak(drugWebsite, current_entry, q)
                
                if phaseInfo!=False:
                    return phaseInfo
        presetValue=''
        for u in range(0, len(presetValues)): 
            presetValue=presetValues[u]
       # print(randsc)
        return phaseInfo
   
    def Masterful(self,current_entry, drugWebsite):
        totalChecks = self.indices(drugWebsite,current_entry )
        bob=[]
        truthful=[]
        bobby=[]
        for q in range(0, len(totalChecks)):
           # print(current_entry)
            presetValue=self.BetterBreak(drugWebsite, current_entry, totalChecks[q])
            pre=list(set(presetValue))
            
            #print(pre)
            phasing=self.PhaseDiognostic(drugWebsite,current_entry, totalChecks[q])
            known=self.TruthCheck(pre,phasing)
            #fullList=[True,]
            joe=[self.company_name,current_entry,pre,phasing]
            bob.append(joe)
            truthful.append(known)
            
        print(bob)
        print(truthful)
        bobby=self.FullReference(truthful,bob)
        print(bobby)
    def PreciseMasterful(self,current_entry, drugWebsite,nextEntry):
        totalChecks = self.indices(drugWebsite,current_entry )
        bob=[]
        truthful=[]
        bobby=[]
        for q in range(0, len(totalChecks)):
           # print(current_entry)
            presetValue=self.BestBreak(drugWebsite, current_entry, totalChecks[q],nextEntry)
            pre=list(set(presetValue))
            
            #print(pre)
            phasing=self.PhaseDiognostic(drugWebsite,current_entry, totalChecks[q])
            known=self.TruthCheck(pre,phasing)
            #fullList=[True,]
            joe=[self.company_name,current_entry,pre,phasing]
            bob.append(joe)
            truthful.append(known)
            
        print(bob)
        print(truthful)
        bobby=self.FullReference(truthful,bob)
        print(bobby)
        
        return 'false'
    def UltimateAnalytics(self,current_entry, drugWebsite):
        #This filter performs the most intensive analysis possible
        #It will initially be fed a current drug entry and attempt to extrapolate
        #both the number of occurances and the most likely phase information
        totalChecks = self.indices(drugWebsite,current_entry )
        #Total checks contains all the instances in which the drug entry appears in the text
        
        bob=[]
        truthful=[]
        bobby=[]
        
        for q in range(0, len(totalChecks)):
           # print(current_entry)
            presetValue=self.BestBreakA(drugWebsite, current_entry, totalChecks[q])
            if presetValue==[]:
                #If the appended informatiion is lacking, a more intensive search will be possibly performed
                presetValue=self.BetterBreak(drugWebsite, current_entry, totalChecks[q])
            pre=list(set(presetValue))
            
            #print(pre)
            phasing=self.PhaseDiognostic(drugWebsite,current_entry, totalChecks[q])
            if phasing==False:
                phasing=self.HighPrecisionPhase(self.strdata.split('<'),current_entry)
                if phasing==False:
                    phasing=self.QuickPhasing(current_entry,self.strdata.split('<'))
            known=self.TruthCheck(pre,phasing)
            #fullList=[True,]
            joe=[self.company_name,current_entry,pre,phasing]
            bob.append(joe)
            truthful.append(known)
        bobby=self.FullReference(truthful,bob)
        if bobby==[]:
            bob=self.HighPrecisionFilter(drugWebsite,current_entry)
            bobby.append(bob)
        return bobby
    def FullReference(self,current_entry, listValues):
        wholeV=0
        indi=0
        indi2=0
        indi3=0
        qlur=0
        qlun=0
        deleatable=0
        for q in range(0, len(current_entry)):
            if current_entry[q]==[True,True,False,False]:
                wholeV=1
                
            if current_entry[q]==[True,True,False,False]:
                indi=1
                deleatable=q
                if wholeV==1:
                    listValues.pop(deleatable)
                    current_entry.pop(deleatable)
                    return self.FullReference(current_entry,listValues)
            if current_entry[q]==[True,True,True,False]:
                indi2=1
                qlur=q
            if current_entry[q]==[True,True,False,True]:
                indi3=1
                qlun=q
            if indi3==1 and indi2==1:
                temp=listValues[qlur]
                temp2=listValues[qlun]
                listValues.pop(qlur)
                listValues.pop(qlun)
                current_entry.pop(qlur)
                current_entry.pop(qlun)
                newV=[temp[0],temp[1],temp[2],temp2[3]]
                newT=[True,True,True,True]
                listValues.append(newV)
                current_entry.append(newT)
                return self.FullReference(current_entry,listValues)
        return listValues
    def TruthCheck(self,background, phasing):
        backgoundTruth=True;
        phasingTruth=True;
        if not background:
            backgoundTruth=False;
        if phasing==False:
            phasingTruth=False;
            
        return [True,True,backgoundTruth,phasingTruth]
    def QuickPhasing(self,current_entry, drugWebsite):
         for q in range(0, len(drugWebsite)):
            if current_entry in drugWebsite[q]:
                start=q-10
                stop=q+5
                for spec in range(start, stop):
                   if 'phase' in drugWebsite[spec]:
                     if 'phase3' in drugWebsite[spec]:
                         return 'phase 3'
                     elif 'phase3' in drugWebsite[spec+1]:
                         return 'phase 3'
                     if 'phase1' in drugWebsite[spec]:
                         return 'phase 1'
                     elif 'phase1' in drugWebsite[spec+1]:
                         return 'phase 1'
                     if 'phase2' in drugWebsite[spec]:
                         return 'phase 2'
                     elif 'phase2' in drugWebsite[spec+1]:
                         return 'phase 2'
                     if '3' in drugWebsite[spec]:
                         return 'phase 3'
                     elif '3' in drugWebsite[spec+1]:
                         return 'phase 3'
                     if '1' in drugWebsite[spec]:
                         return 'phase 1'
                     elif '1' in drugWebsite[spec+1]:
                         return 'phase 1'
                     if '2' in drugWebsite[spec]:
                         return 'phase 2'
                     elif '2' in drugWebsite[spec+1]:
                         return 'phase 2'
                     if 'III' in drugWebsite[q]:
                         return 3
                     elif 'III' in drugWebsite[q+1]:
                         return 3
                     if 'II' in drugWebsite[q]:
                         return 2
                     elif 'II' in drugWebsite[q+1]:
                         return 2
                     if 'I' in drugWebsite[q]:
                         return 'phase 1'
                     elif 'I' in drugWebsite[q+1]:
                         return 'phase 1'
                 #    else:
                  #       return 'close'
                
                  
        
        
         return False
# Any testing code goes here
    def TotalWebPageParse(self,ProposedDrugs, DrugWebsite):
        finalList=[]
        phaseCorrect=0
        EntryCorrect=0
        totalEntry=0
        for q in range(0, len(ProposedDrugs)):
            currentDrug=self.UltimateAnalytics(ProposedDrugs[q],DrugWebsite)
            for z in range(0, len(currentDrug)):
                finalList.append(currentDrug[z])
               
        for z in range(0,len(finalList)):
            entrV=finalList[z] 
            if len(entrV)!=[]:
                if entrV[3]==False:
                    phaseCorrect=phaseCorrect+1
                if entrV[2]==[]:
                    EntryCorrect=EntryCorrect+1
            totalEntry=totalEntry+1
            
        self.PhasesRight=phaseCorrect
        self.InfoFilled=EntryCorrect
        self.TotalEntries=totalEntry
        return finalList
if __name__ == "__main__":
    
    
    # Biogen, Abbvie, Teva, Bristol-Meyer --Using Dirty HTML 
    # Roche, Astrazeneca, Lilly, Alexion, novonordisk, lundbeck,valeant ----Normal
    # SHire, daiichisankyo--- P1 sysytem  GlaaskoSmithKliene, Dainippon Sumitomo, 
    #Close Range: , Endo Health Solutions),teijin-pharma (consider III system)
    #Impossible: Amgen, Novaris, Ionis, Bayer, boehringer-ingelheim, allegron, Baxter, Galderma,actelion, Ipsen
    #Better Left to PDF: Merck,Shionogi, Ono
    #No Pipeline: Forrrext, Abbot Labs,STADA
    
    
    # This function will return possible treatments
    # medicine= enchant("en-medical.multi");
    url='http://www.alexion.com/research-development/pipeline'
   # url='https://www.shire.com/research-and-development/pipeline'
   # url='http://www.gsk.com/en-gb/research/what-we-are-working-on/product-pipeline/'
   # url = "http://www.roche.com/research_and_development/who_we_are_how_we_work/pipeline.html"
   # url = "https://www.biogen.com/en_us/research-pipeline/biogen-pipeline.html"
    #url='https://www.abbvie.com/our-science/pipeline.html'
   # url='https://www.abbvie.com/our-science/pipeline/abbv-2451.html'
    #url='http://www.amgenpipeline.com/pipeline/'
   # url = "https://www.astrazeneca.com/our-science/pipeline.html"
   # url = "https://www.lilly.com/pipeline/"
    #url='http://www.tevapharm.com/research_development/rd_focus/pipeline/'
    #url='http://www.bms.com/research/pipeline/Pages/default.aspx'
    #url='https://www.chugai-pharm.co.jp/english/ir/reports_downloads/pipeline.html'
    #url='https://www.drugs.com/manufacturer/edwards-pharmaceuticals-253.html'
    #url='http://mobile.cslbehring.com/productpipeline.htm'
    #url='http://www.novonordisk.com/rnd/rd-pipeline.html'
    #url='http://www.daiichisankyo.com/rd/pipeline/development_pipeline/index.html'
    #url='http://www.gsk.com/en-gb/research/what-we-are-working-on/product-pipeline/'
    #url='http://www.ds-pharma.com/rd/clinical/pipeline.html'
    #url='http://www.valeant.com/operational-expertise/valeant-united-states/pipeline' ---Works Well
    #url='http://investor.lundbeck.com/pipeline.cfm'
 #   url='http://www.endo.com/endopharma/r-d/clinical-research/clinical-trials-and-studies'
    #url= 'https://www1.actelion.com/en/scientists/development-pipeline/index.page'
  #  url='http://www.teijin-pharma.com/business/research.html'
   # url='http://www.ucb.com/our-science/pipeline'
    company_name = "Roche"

    full_parser = FullParser(company_name, url)
    full_parser.start()
    
    
    jo=full_parser.FinalList2
    shmo=full_parser.SecondFilter
    full_parser.Masterful(shmo[1],jo)
    #full_parser.PreciseMasterful(shmo[12],jo,shmo[11])
    #full_parser.Masterful(shmo[3],jo)
    #full_parser.Masterful(shmo[4],jo)
    #full_parser.Masterful(shmo[21],jo)
    #print(full_parser.FullReference([[True, True, False, True], [True, True, True, False], [True, True, False, False]],[['Roche', 'Pertuzumab', [], 'phase 3'], ['Roche', 'Pertuzumab', ['cancer', 'breast'], False],['Roche', 'Pertuzumab', [], False]]))
    #full_parser.BetterBreak(jo,shmo[2], 7655)
    #full_parser.BetterBreak(jo,shmo[2], 7715)
    #full_parser.BetterBreak(jo,shmo[2], 7771)
    #print(full_parser.PhaseDiognostic(jo,shmo[2], 7771))
    #print(full_parser.PhaseDiognostic(jo,shmo[2], 7655))
    #print(full_parser.strdata.split('<'))
    #print(full_parser.HighPrecisionFilter(full_parser.strdata.split('<'),shmo[4]))
    #print(full_parser.HighPrecisionFilter(jo,shmo[4]))
    print(full_parser.UltimateAnalytics(shmo[1],jo))
    print(full_parser.HighPrecisionPhase(full_parser.strdata.split('<'),shmo[0]))
    print(full_parser.QuickPhasing(shmo[0],full_parser.strdata.split('<') ))
    print(shmo[1])
    print(full_parser.TotalWebPageParse(shmo,jo))
    print(full_parser.UltimateAnalytics(shmo[1],jo))
    print(full_parser.HighPrecisionFilter(jo,shmo[1]))
    print(shmo[1])
    print('Percentage of Drugs with phase information available:')
    print((((1-(full_parser.PhasesRight/full_parser.TotalEntries))*100)))
    print('Percentage of Drugs with treatment information available:')
    print((((1-(full_parser.InfoFilled/full_parser.TotalEntries))*100)))
    
    #print(full_parser.TotalEntries)
    
   # print(full_parser.strdata.split('<'))