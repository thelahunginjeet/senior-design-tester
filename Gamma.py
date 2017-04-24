#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 22:32:13 2017

@author: fatirahmed
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 15:58:43 2017
@author: fatirahmed
"""
import re
from bs4 import BeautifulSoup as bs
import requests
import enchant
import pandas as pd

class FullParser:

    def __init__(self, _company_name, url):
        # Getting data from website
        r = requests.get(url)

        # Setting information into class variable
        self.eng = enchant.Dict("en_US")  # English dictionary to compare
        self.mechs = enchant.request_pwl_dict("mechanisms.txt")
        self.company_name = _company_name
        data = r.text
        self.find_pdf(data)

        # Creating and searching lists
        final_list = self.create_list(data)
        (final_list, second_filter) = self.search_list(final_list)

        # Starts computation
        self.start(final_list, second_filter)

    # MAIN
    def start(self, final_list, second_filter):
        """
        Runs program and determines anlytics
        """
        # Getting drug data
        self.__final_drug_data_high = self.total_web_page_parse(second_filter, final_list)

        # Getting analytics
        self.ultimate_analytics(second_filter[1], final_list)
        self.high_precision_filter(final_list, second_filter[1])

        # Saving drug phase scrape rate
        self.__drug_data_scrape_rate = (((1-(self.PhasesRight/self.TotalEntries))*100))

        # Saving drug mechanism scrape rate
        self.__drug_mech_scrape_rate = (((1-(self.InfoFilled/self.TotalEntries))*100))

    """ PRE PROCESSERS """

    def create_list(self, data):
        """
        Creates list of words to search and compare against dictionaries.
        """
        # Creating versions of BS Objects
        primitive_soup = bs(data, "lxml")  # Creating primitive BS Object
        clean_text = primitive_soup.text  # Extracting just the text
        soup2 = bs(clean_text, "lxml")  # Creating new BS Object from raw text

        # Extracting texts from objects
        [s.extract() for s in primitive_soup(['style', 'script', '[document]', 'head', 'title'])]
        visible_text = primitive_soup.getText()  # Raw text
        self.strdata = primitive_soup.prettify()  # BS Object

        # Creating lists of words to search
        final_list = visible_text.split()

        # Stating completion
        return final_list

    def search_list(self, final_list):
        """
        This method searches a list of words and chooses which words to processing
        :param final_list: list
        :return: tuple
        """
        # Initializing empty filter
        FirstFilter = []

        # Iterating through every word in the list and processing word
        for x in range(0, len(final_list)):
            # Removing punctuation
            current_word = final_list[x]
            current_word = current_word.replace(",", "").replace(":", "").replace("<", "")
            current_word = current_word.replace(">", "").replace("]", "").replace("[", "")
            current_word = current_word.replace(")", "")

            # if there is a word in this index, then process it
            if len(current_word) != 0:
                # Check if it is not in the english dictionary
                if not self.eng.check(current_word):
                    # If the word is longer than 5 letters
                    if len(current_word) >= 5:
                        # If it appears in the list more than once
                        if final_list.count(final_list[x]) >= 1:
                            # If the selected word contains a backslash
                            if "/" in current_word:
                                current_word.split("/")  # Split it into seperate words
                                # If both words are not in the english dictionary
                                if not (self.eng.check(current_word[0]) & self.eng.check(current_word[1])):
                                    processed_word = self.checking_official(current_word)
                                    # Only add it to the filter if word matches
                                    if processed_word != 'null':

                                        FirstFilter.append(processed_word)

                            else:  # If selected word is only one word
                                processed_word = self.checking_official(current_word)
                                if processed_word != 'null':
                                    FirstFilter.append(processed_word)

        second_filter = list(set(FirstFilter))  # Conversion to new list

        # Test all words against second filter and check
        for x in range(0, len(second_filter)):
            if second_filter[x] != ('false', 'N/A'):
                self.block_breaker(final_list, second_filter[x])

        return (final_list, second_filter)

    def indices(self, lst, element):
        """
        This method does something
        :param lst: list
        :param element: string
        :return: list
        """
        result = []
        offset = -1
        while True:
            try:
                offset = lst.index(element, offset+1)
            except ValueError:
                return result
            result.append(offset)

    def checking_official(self, current_check):
        """
        Checks to see if word follows certain patterns
        :param current_check: string
        :return: string
        """
        # Compiling patterns
        p1 = re.compile(r"\b[A-Za-z]+(vir|cillin|mab|ximab|zumab|tinib|vastatin|prazole|lukast|axine|olol|oxetine|sartan|pril|pib|oxacin|xaban|afil|ine|parib|tide|imod)\b")
        p2 = re.compile(r"\b[A-Za-z]+(grel|barb|prost)[A-Za-z]+\b")
        p3 = re.compile(r"\b(cef)[A-Za-z]+\b")
        p4 = re.compile(r"[A-Z].+\d$")

        # Testing each pattern
        if not self.mechs.check(current_check):
            if re.match(p1, current_check): # Suffix testing
                return current_check
            elif re.match(p2, current_check): # Infix testing
                return current_check
            elif re.match(p3, current_check): # Prefix testing
                return current_check
            elif re.match(p4, current_check): # Number ending
                return current_check
            else:
                return 'null'  # If no match
        else:
            return 'null'

    def find_pdf(self, data):
        primitive_soup = bs(data, "lxml")


    """ PHASE IDENTIFIERS """

    def reiterated_phases(self, drug_entry):
        """
        Tests word to see if it tells you a phase
        :param drug_entry: string
        :return: Boolean
        """
        p1 = re.compile(r"phase2?$", re.I)
        # print(bool(re.match(p1, drug_entry)))
        return bool(re.match(p1, drug_entry))

    def phase_finder(self, drug_website, current_entry ):
        """
        Finds the phase number next to a drug name
        :param drug_website: string
        :param current_entry: string
        :return: string
        """
        # Find the number of indices
        total_checks = self.indices(drug_website, current_entry )

        # For every index in the range, test it
        for q in range(0, len(total_checks)):
            # Starting variables
            bob = []
            start = 0

            # If the checks at that index is greater than 15
            if total_checks[q] >= 15:
                start = total_checks[q]-15
            else:
                start = 0;
            end = total_checks[q]+15

            for x in range(start, end):
                 current_entry = drug_website[x]
                 future_entry = drug_website[x+1]

                 pattern1 = re.compile('^[Phase]')
                 pattern2 = re.compile('^[phase]')

                 a = pattern1.findall(current_entry)
                 b = pattern2.findall(current_entry)
                 bob.append(drug_website[99])

                 if self.reiterated_phases(current_entry):

                     # Extracting if phase number comes after the word phase
                     test1 = re.search(r"(\d)", current_entry)
                     test2 = re.search(r"(\d)", future_entry)
                     if test1:
                         return ("phase " + test1.group(1))
                     elif test2:
                        return ("phase " + test2.group(1))

                    # Extracting if phase number is roman numeral
                     test3 = re.search(r"([Il]+)", current_entry)
                     test4 = re.search(r"([Il]+)", future_entry)
                     if test3:
                         return int(test3.group(1))
                     elif test4:
                         return int(test4.group(1))
                     else:
                         return 7
        return "false"

    # FLAGGED FOR REMOVAL IN FINAL COMMIT (NOT USED)
    def nearby_search(self, drug_website, current_entry):
        """
        This method searches the nearby words and creates a new list
        :param drug_website: string
        :param current_entry: string
        :return: list
        """
        total_checks = self.indices(drug_website, current_entry )
        entry = []
        for q in range(0, len(total_checks)):
            start = 0
            if total_checks[q] >= 20:
                start = total_checks[q] - 20
            else:
                start = 0
            end = total_checks[q] + 20
            for x in range(start, end):
                 _current_entry = drug_website[x]
                 _future_entry = drug_website[x+1]
                 entry.append(_current_entry)

        return entry

    def mech_action(self, drug_website, current_entry, index_number):
        """
        This method can extract a block of words around the drug name regarding
        the mechanism
        :param drug_website: list
        :param current_entry: string
        :param index_number: int
        :return: list
        """
        return_list = []
        pwl = enchant.request_pwl_dict("mechanisms.txt")
        start = 0
        if index_number >= 11:
                start = index_number - 11
        else:
                start = 0
        end = index_number + 15
        for x in range(index_number, end):
            if self.checking_official(drug_website[x+1]) == 'null':
                if pwl.check(drug_website[x]):
                    return_list.append(drug_website[x])
            else:
                break

        for x in range(1, 10):
            if self.checking_official(drug_website[index_number-x]) == 'null':
                if pwl.check(drug_website[index_number-x]):
                    return_list.append(drug_website[index_number-x])
            else:
                break
        if return_list==[]:
            return [];

        return return_list

    """ BREAKERS """
    # FLAGGED FOR BETTER VERSION (ONLY USED ONCE)
    def block_breaker(self, drug_website, current_entry):
        return_list = []
        pwl = enchant.request_pwl_dict("medical.txt")

        total_checks = self.indices(drug_website, current_entry )

        for q in range(0, len(total_checks)):

            start = 0;
            joe = 0
            if total_checks[q] >= 15:
                start = total_checks[q] - 15
            else:
                start = 0;
            end = total_checks[q] + 15
            for x in range(start, end):
                if pwl.check(drug_website[x]):
                    return_list.append(drug_website[x])
        # print(return_list)

    def better_break(self, drug_website, current_entry, index_number):
        """
        This method can extract a block of words around the drug name
        :param drug_website: list
        :param current_entry: string
        :param index_number: int
        :return: list
        """
        return_list = []
        pwl = enchant.request_pwl_dict("medical.txt")
        start = 0

        if index_number >= 11:
            start = index_number - 11
        else:
            start = 0

        end = index_number + 15
        if end >= len(drug_website):
            end = len(drug_website)-1



        for x in range(start, end):
            if pwl.check(drug_website[x]):
                return_list.append(drug_website[x])

        return return_list

    def best_break(self, drug_website, current_entry, index_number):
        """
        This does what better_break does but better
        :param drug_website: list
        :param current_entry: string
        :param index_number: int
        :return: list
        """
        return_list = []
        pwl = enchant.request_pwl_dict("medical.txt")
        start = 0

        if index_number >= 11:
            start = index_number-11
        else:
            start = 0

        end = index_number+17

        for x in range(index_number, end):
            if self.checking_official(drug_website[x+1]) == 'null':
                if pwl.check(drug_website[x]):
                    return_list.append(drug_website[x])
            else:
                break

        for x in range(1, 10):
            if self.checking_official(drug_website[index_number-x]) == 'null':
                if pwl.check(drug_website[index_number-x]):
                    return_list.append(drug_website[index_number-x])
            else:
                break

        return return_list

    def phase_diagnostic(self, drugWebsite, current_entry, indexNumber):
        bob=[]
        start=0;
        joe=0
        if indexNumber>=15:
            start=indexNumber-15
        else:
            start=0;
        end=indexNumber+15
        if end>=len(drugWebsite):
            end=len(drugWebsite)-1;
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
                 if self.reiterated_phases(currentEntry)==True:
                     if 'phase3' in currentEntry:
                         return '3'
                     elif 'phase3' in futureEntry:
                         return '3'
                     if 'phase1' in currentEntry:
                         return '1'
                     elif 'phase1' in futureEntry:
                         return '1'
                     if 'phase2' in currentEntry:
                         return '2'
                     elif 'phase2' in futureEntry:
                         return '2'
                     if '3' in currentEntry:
                         return '3'
                     elif '3' in futureEntry:
                         return '3'
                     if '1' in currentEntry:
                         return '1'
                     elif '1' in futureEntry:
                         return '1'
                     if '2' in currentEntry:
                         return '2'
                     elif '2' in futureEntry:
                         return '2'
                     if 'III' in currentEntry:
                         return 3
                     elif 'III' in futureEntry:
                         return 3
                     if 'II' in currentEntry:
                         return 2
                     elif 'II' in futureEntry:
                         return 2
                     if 'I' in currentEntry:
                         return '1'
                     elif 'I' in futureEntry:
                         return '1'
                     elif 'P1' in currentEntry:
                         return '1'
                     elif 'P2' in currentEntry:
                         return '2'
                     elif 'P3' in currentEntry:
                         return '3'

                     else :
                         return False
        return False

    def best_break2(self, drug_website, current_entry, index_number, future_entry):
        """
        This does what better_break does but better than best
        :param drug_website: list
        :param current_entry: string
        :param index_number: int
        :param future_entry: string
        :return: list
        """
        return_list = []
        pwl = enchant.request_pwl_dict("medical.txt")
        start = 0

        if index_number >= 2:
            start = index_number - 2
        else:
            start = 0

        end = index_number + 5

        for x in range(start, end):
            if pwl.check(drug_website[x]):
                return_list.append(drug_website[x])
            if future_entry in drug_website[x]:
                return return_list
        return return_list
        """
        Checks the phase number for the drug
        :param drug_website: list
        :param current_entry: string
        :param index_number: int
        :return: string
        """
        start = 0

        if index_number >= 15:
            start = index_number - 15
        else:
            start = 0;

        end = index_number + 15

        for x in range(start, end):

             _current_entry = drug_website[x]
             future_entry = drug_website[x+1]
             p1 = re.compile('^[Phase]')
             p2 = re.compile('^[phase]')
             a = p1.findall(_current_entry)
             b = p2.findall(_current_entry)

             if self.reiterated_phases(_current_entry):
                 # Extracting if phase number comes after the word phase
                 test1 = re.search(r"(\d)", _current_entry)
                 test2 = re.search(r"(\d)", future_entry)
                 test3 = re.search(r"P([123])", _current_entry)
                 if test1:
                     return ("phase " + test1.group(1))
                 elif test2:
                    return ("phase " + test2.group(1))
                 elif test3:
                    return ("phase " + test3.group(1))

                 # Extracting if phase number is roman numeral
                 test4 = re.search(r"([Il]+)", _current_entry)
                 test5 = re.search(r"([Il]+)", future_entry)
                 if test4:
                     return int(test4.group(1))
                 elif test5:
                     return int(test5.group(1))
        return False


    """ FILTERS """
    def high_precision_filter(self, drug_website, current_entry):
        """
        This filter is very precise
        :param drug_website: string
        :param current_entry: string
        :return: list
        """
        # Pre-set values
        phase_info = 'Unknown'
        preset_value = ''
        preset_values = []
        mechanisms=False

        for q in range(0, len(drug_website)):
            if current_entry in drug_website[q]:
                phase_info = self.phase_diagnostic(drug_website, current_entry, q)
                preset_value = self.better_break(drug_website, current_entry, q)
                mechanisms = self.mech_action( drug_website, current_entry, q)

                if preset_value != []:
                    preset_values.append(preset_value)

        preset_value = []

        for u in range(0, len(preset_values)):
            preset_value = preset_values[u]

        hp_entry = [self.company_name, current_entry, preset_value, phase_info,mechanisms]

        return hp_entry

    def high_precision_phase(self, drug_website, current_entry):
        """
        Some high precision phase detector
        :param drug_website: string
        :param current_entry: string
        :return: list
        """
        phase_info = False
        preset_value = ''
        preset_values = []
        randsc = []

        for q in range(0, len(drug_website)):
            if current_entry in drug_website[q]:
                randsc.append(drug_website[q])
                phase_info = self.phase_diagnostic(drug_website, current_entry, q)
                preset_value = self.better_break(drug_website, current_entry, q)

                if phase_info != False:
                    return phase_info

        preset_value = ''

        for u in range(0, len(preset_values)):
            preset_value = preset_values[u]
        # print(phase_info)
        return phase_info


    """ ANALYTICS """
    # FLAGGED FOR REMOVAL IN FINAL COMMIT (NOT USED)
    def masterful(self, drug_website, current_entry):
        """
        :param drug_website: string
        :param current_entry: string
        :return: list
        """
        total_checks = self.indices(drug_website, current_entry )
        bob = []
        truthful = []
        bobby = []

        for q in range(0, len(total_checks)):
            preset_value = self.better_break(drug_website, current_entry, total_checks[q])
            preset_list = list(set(preset_value))

            phase_info = self.phase_diagnostic(drug_website, current_entry, total_checks[q])
            known = self.truth_check(preset_list, phase_info)
            joe = [self.company_name, current_entry, preset_list, phase_info]
            bob.append(joe)
            truthful.append(known)

        # print(bob)
        # print(truthful)
        bobby = self.full_reference(truthful, bob)
        # print(bobby)

    # FLAGGED FOR REMOVAL IN FINAL COMMIT (NOT USED)
    def precise_masterful(self, current_entry, drug_website, nextEntry):
        total_checks = self.indices(drug_website,current_entry )
        bob=[]
        truthful=[]
        bobby=[]
        for q in range(0, len(total_checks)):
           # print(current_entry)
            preset_value = self.best_break2(drug_website, current_entry, total_checks[q],nextEntry)
            preset_list = list(set(preset_value))

            #print(preset_list)
            phase_info = self.phase_diagnostic(drug_website,current_entry, total_checks[q])
            known = self.truth_check(preset_list,phase_info)
            #fullList=[True,]
            joe=[self.company_name,current_entry,preset_list,phase_info]
            bob.append(joe)
            truthful.append(known)

        # print(bob)
        # print(truthful)
        bobby = self.full_reference(truthful,bob)
        # print(bobby)

        return 'false'

    def ultimate_analytics(self, current_entry, drug_website):
        """
        This filter performs the most intensive analysis possible
        It will initially be fed a current drug entry and attempt to extrapolate
        both the number of occurances and the most likely phase information
        :param current_entry: string
        :param drug_website: string
        :return: list
        """
        # Total checks contains all the instances in which the drug entry appears in the text
        total_checks = self.indices(drug_website,current_entry )
        bob=[]
        truthful=[]
        bobby=[]

        for q in range(0, len(total_checks)):
            preset_values = self.best_break(drug_website, current_entry, total_checks[q])
            final_drug_name = self.adder_check(drug_website, current_entry, total_checks[q])
            mechanics_info = self.mech_action( drug_website, current_entry, total_checks[q])

            # If the appended informatiion is lacking, a more intensive search will be possibly performed
            if preset_values == []:
                preset_values = self.better_break(drug_website, current_entry, total_checks[q])
            if mechanics_info ==[]:
                mechanics_info=self.mechi_backup(current_entry)
            preset_list = list(set(preset_values))
            phase_info = self.phase_diagnostic(drug_website, current_entry, total_checks[q])
            if not phase_info:
                phase_info = self.high_precision_phase(self.strdata.split('<'), current_entry)
                if not phase_info:
                    # print("running")
                    phase_info = self.quick_phasing(current_entry, self.strdata.split('<'))
                    # print(phase_info)
            known = self.advanced_truth_check(preset_list, phase_info,mechanics_info )
            joe = [self.company_name, final_drug_name, preset_list, phase_info, mechanics_info]
            bob.append(joe)
            truthful.append(known)
        bobby = self.complete_reference(truthful, bob)


        new_k = []
        for elem in bobby:
            if elem not in new_k:
                new_k.append(elem)
        bobby = new_k
        bobby=self.fixingContent(bobby,current_entry)
        

        if bobby == []:
            bob = self.high_precision_filter(drug_website, current_entry)
            bobby.append(bob)

        return bobby

    def full_reference(self, current_entry, list_values):
        """
        :param current_entry: string
        :param list_values: list
        :return: list
        """
        # Initializing variables
        wholeV = 0
        indi = 0
        indi2 = 0
        indi3 = 0
        qlur = 0
        qlun = 0
        deletable = 0

        for q in range(0, len(current_entry)):
            if current_entry[q] == [True, True, False, False]:
                wholeV = 1

            if current_entry[q] == [True, True, False, False]:
                indi = 1
                deletable = q
                if wholeV == 1:
                    list_values.pop(deletable)
                    current_entry.pop(deletable)
                    return self.full_reference(current_entry, list_values)

            if current_entry[q] == [True, True, True, False]:
                indi2 = 1
                qlur = q

            if current_entry[q] == [True, True, False, True]:
                indi3 = 1
                qlun = q

            if indi3 == 1 and indi2 == 1:
                temp = list_values[qlur]
                temp2 = list_values[qlun]
                list_values.pop(qlur)
                list_values.pop(qlun)
                current_entry.pop(qlur)
                current_entry.pop(qlun)
                holder = temp[4] + ' ' + temp2[4]
                nnewV = [temp[0], temp[1], temp[2], temp2[3], holder]
                newT = [True, True, True, True]
                listValues.append(newV)
                current_entry.append(newT)
                return self.full_reference(current_entry, list_values)

        return list_values

    def complete_reference(self, current_entry, list_values):
        """
        :param current_entry: string
        :param list_values: list
        :return: list
        """
        wholeV=0
        indi=0
        indi2=0
        indi3=0
        qlur=0
        qlun=0
        deleatable=0
        for q in range(0, len(current_entry)):
            if current_entry[q]==[True,True,False,False,False]:
                wholeV=1

            if current_entry[q]==[True,True,False,False,False]:
                indi=1
                deleatable=q
                if wholeV==1:
                    list_values.pop(deleatable)
                    current_entry.pop(deleatable)
                    return self.complete_reference(current_entry,list_values)
            if current_entry[q]==[True,True,True,False,True] or current_entry[q]==[True,True,True,False,False]:
                indi2=1
                qlur=q
            if current_entry[q]==[True,True,False,True, True] or current_entry[q]==[True,True,False,True,False]:
                indi3=1
                qlun=q
            if indi3==1 and indi2==1:
                mechi_final=[]
                temp=list_values[qlur]
                temp2=list_values[qlun]
                list_values.pop(qlur)
                list_values.pop(qlun)
                current_entry.pop(qlur)
                current_entry.pop(qlun)
                mechi_truth=False
                inner_truth=False


                if temp[4]!=False:
                        mechi_truth_possible=temp[4]
                        mechi_final.append(mechi_truth_possible)
                if temp2[4]!=False:
                    mechi_truth_possibleB=temp2[4]
                    mechi_final.append(mechi_truth_possibleB)
                if mechi_final!=[]:
                    mechi_truth=mechi_final.append(mechi_truth_possibleB)
                    inner_truth=True

                newV=[temp[0],temp[1],temp[2],temp2[3],mechi_final]
                newT=[True,True,True,True,inner_truth ]
                list_values.append(newV)
                current_entry.append(newT)
                return self.complete_reference(current_entry,list_values)
        return list_values

    def merge_same_name(self, total_drugs):
        for q in range(0, len(total_drugs)):
            if q<(len(total_drugs)-1):
                current_entry=total_drugs[q]
                future_entry=total_drugs[q+1]
                if future_entry[1]==current_entry[1]:
                    if future_entry[3]==current_entry[3]:
                        if future_entry[4]==current_entry[4]:
                            if future_entry[2]==current_entry[2]:
                                new_total_drugs=total_drugs.pop(q)
                                return self.merge_same_name(new_total_drugs)
                            else:
                                mergedlist = future_entry[2] + future_entry[2]
                                new_target= list(set(mergedlist))
                                total_drugs.pop(q)
                                total_drugs.pop(q)
                                new_entry=[current_entry[0],current_entry[1],new_target, current_entry[3],current_entry[4]]

                                total_drugs.insert(q,new_entry)
                                return self.merge_same_name(total_drugs)
        return total_drugs

    def truth_check(self, background, phase_info):
        """
        :param background: string
        :param phase_info: string
        :return: list
        """
        backgound_truth = True
        phasing_truth = True
        if not background:
            backgound_truth = False
        if not phase_info:
            phasing_truth = False

        return [True, True, backgound_truth, phasing_truth]

    def advanced_truth_check(self, background, phase_info,mechi_info):
        """
        :param background: string
        :param phase_info: string
        :return: list
        """
        backgound_truth = True
        phasing_truth = True
        mechi_truth = True
        if not background:
            backgound_truth = False
        if not phase_info:
            phasing_truth = False
        if not mechi_info:
            mechi_truth=False

        return [True, True, backgound_truth, phasing_truth,mechi_truth]

    # FLAGGED (NOTATION NOT FIXED YET)
    def quick_phasing(self, _current_entry, drug_website):
        """
        :param _current_entry: string
        :param drug_website: string
        :return: string
        """
        for q in range(0, len(drug_website)):

            if _current_entry in drug_website[q]:
                start = q - 10
                stop = q + 5

                for spec in range(start, stop):
                    current_entry = drug_website[spec]
                    future_entry = drug_website[spec]


                    if 'phase' in drug_website[spec]:
                         if 'phase3' in drug_website[spec]:
                             return 3
                         elif 'phase3' in drug_website[spec+1]:
                             return 3
                         if 'phase1' in drug_website[spec]:
                             return 1
                         elif 'phase1' in drug_website[spec+1]:
                             return 1
                         if 'phase2' in drug_website[spec]:
                             return 2
                         elif 'phase2' in drug_website[spec+1]:
                             return 2
                         if '3' in drug_website[spec]:
                             return 3
                         elif '3' in drug_website[spec+1]:
                             return 3
                         if '1' in drug_website[spec]:
                             return 1
                         elif '1' in drug_website[spec+1]:
                             return 1
                         if '2' in drug_website[spec]:
                             return 2
                         elif '2' in drug_website[spec+1]:
                             return 2
                         if 'III' in drug_website[q]:
                             return 3
                         elif 'III' in drug_website[q+1]:
                             return 3
                         if 'II' in drug_website[q]:
                             return 2
                         elif 'II' in drug_website[q+1]:
                             return 2
                         if 'I' in drug_website[q]:
                             return 1
                         elif 'I' in drug_website[q+1]:
                             return 1

        return False

    def adder_check(self, drug_website, current_entry, index_number):
        """
        """
        if '+' in drug_website[index_number+1]:
            if self.checking_official(drug_website[index_number+2]) != 'null':

                temp = drug_website[index_number]
                temp2 = drug_website[index_number+2]
                temp3 = '+'
                intermediate = temp + temp3 + temp2
                return intermediate
            else:
                return drug_website[index_number]
        elif '+' in drug_website[index_number]:
            if self.checking_official(drug_website[index_number+2]) != 'null':
                if '+' in drug_website[index_number]:
                     temp = drug_website[index_number]
                temp2 = drug_website[index_number+2]
                temp3 = '+'
                intermediate = temp + temp3 + temp2
                return intermediate
        else:
            return current_entry

    # FLAGGED (NOTATION NOT FIXED YET)
    def fixingContent(self, drug_list,commonName):
        phase1Content=[]
        phase2Content=[]
        phase3Content=[]
        phaseUContent=[]
        PhaseMContent=[]
        totalSize=len(drug_list)
        if totalSize<=1:
            
            return drug_list
        else: 
            for q in range(0, len(drug_list)):
                currentEntry=drug_list[q]
                if currentEntry[1]!=commonName:
                    PhaseMContent.append(currentEntry)
                else:
                    if currentEntry[3]==1:
                        phase1Content.append(currentEntry)
                    
                    elif currentEntry[3]==2:
                        phase2Content.append(currentEntry)
                    
                    elif currentEntry[3]==3:
                        phase3Content.append(currentEntry)
                    else:
                        phaseUContent.append(currentEntry)
        if len(phase1Content)>0:
            PhaseMContent=self.appending_updates(phase1Content,PhaseMContent,1) 
        if len(phase2Content)>0:
            PhaseMContent=self.appending_updates(phase2Content,PhaseMContent,2) 
        if len(phase3Content)>0:
            PhaseMContent=self.appending_updates(phase3Content,PhaseMContent,3) 
        return PhaseMContent
    def fixingContents(self, drug_list,commonName):
        phase1Content=[]
        phase2Content=[]
        phase3Content=[]
        phaseUContent=[]
        PhaseMContent=[]
        for q in range(0, len(drug_list)):
            currentEntry=drug_list[q]
            if currentEntry[1]==commonName:
                if currentEntry[3]==1:
                    phase1Content.append(currentEntry)
                    
                if currentEntry[3]==2:
                    phase2Content.append(currentEntry)
                    
                if currentEntry[3]==3:
                    phase3Content.append(currentEntry)
                else:
                    phaseUContent.append(currentEntry)
            else:
                PhaseMContent.append(currentEntry)
        a=len(phase1Content)
        b=len(phase2Content)
        c=len(phase3Content)
        if a==0 and b==0 and c==0:
            for q in range(0, len(phaseUContent)):
                PhaseMContent.append(phaseUContent)
            
            
            return PhaseMContent
        else:
            if a>0:
                a=a
             #   PhaseMContent=self.appending_updates(phase1Content,PhaseMContent,1)
            if b>0:
                b=b
              #  PhaseMContent=self.appending_updates(phase2Content,PhaseMContent,2)
            if c>0:
                PhaseMContent=self.appending_updates(phase3Content,PhaseMContent,3)
                
        return PhaseMContent
            #Merge the various
    def mechi_backup(self,currentCheck):
        p1 = re.compile(r"\b[A-Za-z]+(vir)/b")
        p2 = re.compile(r"\b[A-Za-z]+(cillin)/b")
        p3 = re.compile(r"\b[A-Za-z]+(mab)/b")
        p4 = re.compile(r"\b[A-Za-z]+(tide)/b")
        p5 = re.compile(r"\b(cef)[A-Za-z]+\b")
        drug_target=[]
        if re.match(p1, currentCheck):
            drug_target=['Antiviral'];
            return drug_target
        elif re.match(p2, currentCheck):
            drug_target=['Penicillin-derived antibiotics'];
            return drug_target
        elif re.match(p5, currentCheck):
            drug_target=['Cephem-type antibiotics'];
            return currentCheck
        
        elif "ximab" in currentCheck:
            drug_target=['Chimeric antibody'];
            return drug_target
        elif "zumab" in currentCheck:
            drug_target=['humanized antibody'];
            return drug_target
        elif re.match(p3, currentCheck):
            drug_target=['monoclonal antiboies'];
            return drug_target
        elif "tinib" in currentCheck:
            drug_target=['tyrosine-kinase inhibitor'];
            return drug_target
        elif "vastatin" in currentCheck:
            drug_target=['tyrosine-kinase inhibitor'];
            return drug_target
        elif "prazole" in currentCheck:
            drug_target=['Proton-pump inhibitor'];
            return drug_target
        elif "lukast" in currentCheck:
            return ['Leukotriene receptor antagonists']
        elif "grel" in currentCheck:
            return drug_target
        elif "axine" in currentCheck:
            return ['Dopamine and serotonin–norepinephrine reuptake inhibitor']
        elif "olol" in currentCheck:
            return ['Beta-blockers']
        elif "oxetine" in currentCheck:
            return ['Antidepressant related to fluoxetine']
        elif "sartan" in currentCheck:
            return ['Angiotensin receptor antagonists']
        elif "pril" in currentCheck:
            return ['Angiotensin converting enzyme inhibitor']
        elif "oxacin" in currentCheck:
            return ['Quinolone-derived antibiotics']
        elif "barb" in currentCheck:
            return ['Barbiturates']
        elif "xaban" in currentCheck:
            return ['Direct Xa inhibitor']
        elif "afil" in currentCheck:
            return ['PDE5 Inhibitor']
        elif "prost" in currentCheck:
            return ['Prostaglandin analogue']
        elif "ine" in currentCheck:
            return ['chemical substance']
        elif "parib" in currentCheck:
            return ['PARP inhibitor']
        elif re.match(p4, currentCheck):
            return ['Peptides']
        else:
            return []
    
    def appending_updates(self, phase1Content,PhaseMContent,phase_int):
            entry1Mech=[]
            entry1treat=[]
            a=len(phase1Content)
            intermidiatM=[]
            currentEntry=phase1Content[0]
            entry1Final=[currentEntry[0], currentEntry[1],entry1Mech,phase_int,entry1treat]
            oneConstant=0
            oneConstant_=0
            anyconstant=0
            for q in range(0, a):
                currentEntry=phase1Content[q]
                if currentEntry[2]==[] and currentEntry[4]==[] and q<(len(currentEntry)-1):
                    oneConstant=oneConstant
                
                elif currentEntry[2]!= [] and currentEntry[4]!= []:
                    PhaseMContent.append(currentEntry)
                    oneConstant_=len(PhaseMContent)
                    anyconstant=1
                    oneConstant=q
                
                    
                    
                elif currentEntry[2]!= [] and currentEntry[4]== []: 
                    if oneConstant_>0:
                        temperary=PhaseMContent.pop(oneConstant_-1)
                        sub=[]
                        sub=temperary[2]+currentEntry[2]
                        sub=list(set(sub))
                        subV=[temperary[0],temperary[1],sub,temperary[3],temperary[4]]
                        PhaseMContent.append(temperary)
                        oneConstant_=0
                        anyconstant=1
                    else:
                        entry1treat=entry1treat+currentEntry[2]
                        entry1Mech=entry1Mech+currentEntry[4]
                        entry1Final=[currentEntry[0], currentEntry[1],entry1treat,phase_int,entry1Mech]
                        anyconstant=1

                elif currentEntry[2]== [] and currentEntry[4]!= []: 
                    if oneConstant_>0:
                        temperary=PhaseMContent.pop(oneConstant_-1)
                        sub=[]
                        sub=temperary[4]+currentEntry[4]
                        sub=list(set(sub))
                        subV=[temperary[0],temperary[1],temperary[2],temperary[3],sub]
                        PhaseMContent.append(subV)
                        oneConstant_=0
                        anyconstant=1
                    else:
                        entry1treat=entry1treat+currentEntry[2]
                        entry1Mech=entry1Mech+currentEntry[4]
                        entry1Final=[currentEntry[0], currentEntry[1],entry1treat,phase_int,entry1Mech]
                        anyconstant=1
               
            PhaseMContent.append(entry1Final)
            return PhaseMContent
    def total_web_page_parse(self, ProposedDrugs, DrugWebsite):
        finalList = []
        lowList=[]
        highList = []
        phaseCorrect = 0
        EntryCorrect = 0
        totalEntry = 0
        for q in range(0, len(ProposedDrugs)):
            currentDrug = self.ultimate_analytics(ProposedDrugs[q], DrugWebsite)
            for z in range(0, len(currentDrug)):
                finalList.append(currentDrug[z])
                drug_entry=currentDrug[z]
                if drug_entry[2]!=[] and drug_entry[3]!=False:
                    highList.append(currentDrug[z])
                else:
                    lowList.append(currentDrug[z])

        for z in range(0,len(finalList)):
            entrV = finalList[z]
            if len(entrV) != []:
                if not entrV[3]:
                    phaseCorrect = phaseCorrect + 1
                if entrV[2] == []:
                    EntryCorrect = EntryCorrect + 1
            totalEntry = totalEntry+1

        self.PhasesRight = phaseCorrect
        self.InfoFilled = EntryCorrect
        self.TotalEntries = totalEntry
        self.FinalList = finalList
        self.HighList = highList
        self.LowList=lowList
        return finalList

    @property
    def final_drug_data_high(self):
        return self.__final_drug_data_high

    @property
    def final_drug_data_low(self):
        return self.__final_drug_data_low

    @property
    def drug_data_scrape_rate(self):
        return self.__drug_data_scrape_rate

    @property
    def drug_mech_scrape_rate(self):
        return self.__drug_mech_scrape_rate

# Class method to run only when called from terminal
def main():
    #url='http://www.gsk.com/en-gb/research/what-we-are-working-on/product-pipeline/'
    url = "https://www.biogen.com/en_us/research-pipeline/biogen-pipeline.html"
    company_name = "biogen"
    full_parser = FullParser(company_name, url)

    df = pd.DataFrame(full_parser.HighList)
    # cols = ['Company Name', 'Product Name','Treatment area','Phase','Mechanism of Action' ]
    #df.columns = cols
    print(df)
    # df.to_csv('testingAlpha', sep='\t')

if __name__ == "__main__":
    main()