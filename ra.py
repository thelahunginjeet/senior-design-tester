# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup as bs
import requests
import enchant
import pandas

class FullParser:
    eng = enchant.Dict("en_US")  # English dictionary to compare

    def __init__(self, _company_name, url):
        # Getting data from website
        r = requests.get(url)

        # Setting information into class variable
        self.company_name = _company_name
        data = r.text

        # Creating and searching lists
        final_list = self.create_list(data)
        (self.final_list, self.second_filter) = self.search_list(final_list)


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
        p1 = re.compile(r"\b[A-Za-z]+(vir|cillin|mab|ximab|zumab|tinib|vastatin|prazole|lukast|axine|olol|oxetine|sartan|pril|pib|oxacin|xaban|afil|ine|parib|tide)\b")
        p2 = re.compile(r"\b[A-Za-z]+(grel|barb|prost)[A-Za-z]+\b")
        p3 = re.compile(r"\b(cef)[A-Za-z]+\b")
        p4 = re.compile(r"[A-Z].+\d$")

        # Testing each pattern
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


    """ PHASE IDENTIFIERS """

    def reiterated_phases(self, drug_entry):
        """
        Tests word to see if it tells you a phase
        :param drug_entry: string
        :return: Boolean
        """
        p1 = re.compile(r"phase2?$", re.I)
        return re.match(p1, drug_entry)

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

    # FLAGGED FOR REMOVAL IN NEXT COMMIT (NOT USED)
    def validate_phase(self, comparision_html, drug_target_list):
        """
        This method determines if there is a phase next to the word
        :param comparision_html: string
        :param drug_target_list: list
        :return: list
        """
        validated_drugs = []
        for x in range(0, len(drug_target_list)):
            current_truth = self.phase_finder(comparision_html, drug_target_list[x])
            if current_truth != "false":
                temp = drug_target_list[x] + ',' + current_truth
                validated_drugs.append(temp)

        return validated_drugs

    # FLAGGED FOR REMOVAL IN NEXT COMMIT (NOT USED)
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

    # FLAGGED FOR REMOVAL IN NEXT COMMIT (NOT USED)
    def advanced_filter(self, drug_website, current_entry):
        total_checks = indices(drug_website, current_entry )
        entry = []
        for q in range(0, len(total_checks)):
            start = 0;
            if total_checks[q] >= 10:
                start = total_checks[q] - 10
            else:
                start = 0;
            end = total_checks[q] + 10
            for x in range(start, end):
                 _current_entry = drug_website[x]
                 _future_entry = drug_website[x+1]
                 if _current_entry == "treatment":
                     if _future_entry == "of":
                         for y in range(x+1, x+5):
                             entry.append(drug_website[y])
        return entry


    """ BREAKERS """
    # FLAGGED FOR REMOVAL IN NEXT COMMIT (NOT USED)
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
        print(return_list)

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

        end = index_number+15

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

    def phase_diagnostic(self, drug_website, current_entry, index_number):
        """
        This breaker will achieve the best result by attempting to
        filter out the drug names based om prior entries. IT will scout only
        a minimum distance in either direction
        :param drug_website: list
        :param current_entry: string
        :param index_number: int
        :return: list
        """
        return_list = []
        pwl = enchant.request_pwl_dict("medical.txt")
        start = 0

        if index_number >= 3:
            start = index_number - 3
        else:
            start = 0

        end = index_number + 4

        for x in range(start, end):
            if pwl.check(drug_website[x]):
                return_list.append(drug_website[x])

        return return_list

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

    # FLAGGED FOR REMOVAL IN NEXT COMMIT (NOT USED)
    def adjacent_check(self, drug_website, current_entry, index_number):
        """
        Check for adjacunt drug names and combine if appropriate
        """
        bob = []
        baselines = []
        pwl = enchant.request_pwl_dict("medical.txt")
        start = 0;
        if index_number >= 2:
                start = index_number - 2
        else:
                start = 0;
        end = index_number + 2
        for x in range(start, end):
            truths = pwl.check(drug_website[x])
            baselines.append(drug_website[x])
            if truths == True:
                bob.append(drug_website[x])
        print(bob)


    """ FILTERS """
    # FLAGGED FOR REMOVAL IN NEXT COMMIT (NOT USED)
    def lousy_helper(self):
        return 'false'

    # FLAGGED FOR REMOVAL IN NEXT COMMIT (NOT USED)
    def lousy_filter(self, drug_website, current_entry):
        #This filter parameter serves primarily as a last resort in case there are
        #high rates of failure
        app = drug_website.split();
        lengthing = len(app)

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

        for q in range(0, len(drug_website)):
            if current_entry in drug_website[q]:
                phase_info = self.phase_diagnostic(drug_website, current_entry, q)
                preset_value = self.better_break(drug_website, current_entry, q)

                if preset_value != []:
                    preset_values.append(preset_value)

        preset_value = []

        for u in range(0, len(preset_values)):
            preset_value = preset_values[u]

        hp_entry = [self.company_name, current_entry, preset_value, phase_info]

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

        return phase_info


    """ ANALYTICS """
    # FLAGGED FOR REMOVAL IN NEXT COMMIT (NOT USED)
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
           # print(current_entry)
            preset_value = self.better_break(drug_website, current_entry, total_checks[q])
            preset_list = list(set(preset_value))

            #print(preset_list)
            phase_info = self.phase_diagnostic(drug_website, current_entry, total_checks[q])
            known = self.truth_check(preset_list, phase_info)
            #fullList=[True,]
            joe = [self.company_name, current_entry, preset_list, phase_info]
            bob.append(joe)
            truthful.append(known)

        print(bob)
        print(truthful)
        bobby = self.full_reference(truthful, bob)
        print(bobby)

    # FLAGGED FOR REMOVAL IN NEXT COMMIT (NOT USED)
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

        print(bob)
        print(truthful)
        bobby = self.full_reference(truthful,bob)
        print(bobby)

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

            preset_list = list(set(preset_values))
            phase_info = self.phase_diagnostic(drug_website, current_entry, total_checks[q])

            if not phase_info:
                phase_info = self.high_precision_phase(self.strdata.split('<'), current_entry)
                if not phase_info:
                    phase_info = self.quick_phasing(current_entry, self.strdata.split('<'))

            known = self.TruthCheck(preset_list,phase_info)
            joe = [self.company_name, final_drug_name, preset_list, phase_info, mechanics_info]
            bob.append(joe)
            truthful.append(known)

        bobby = self.full_reference(truthful, bob)

        if bobby == []:
            bob = self.HighPrecisionFilter(drug_website, current_entry)
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
                             return 'phase 3'
                         elif 'phase3' in drug_website[spec+1]:
                             return 'phase 3'
                         if 'phase1' in drug_website[spec]:
                             return 'phase 1'
                         elif 'phase1' in drug_website[spec+1]:
                             return 'phase 1'
                         if 'phase2' in drug_website[spec]:
                             return 'phase 2'
                         elif 'phase2' in drug_website[spec+1]:
                             return 'phase 2'
                         if '3' in drug_website[spec]:
                             return 'phase 3'
                         elif '3' in drug_website[spec+1]:
                             return 'phase 3'
                         if '1' in drug_website[spec]:
                             return 'phase 1'
                         elif '1' in drug_website[spec+1]:
                             return 'phase 1'
                         if '2' in drug_website[spec]:
                             return 'phase 2'
                         elif '2' in drug_website[spec+1]:
                             return 'phase 2'
                         if 'III' in drug_website[q]:
                             return 3
                         elif 'III' in drug_website[q+1]:
                             return 3
                         if 'II' in drug_website[q]:
                             return 2
                         elif 'II' in drug_website[q+1]:
                             return 2
                         if 'I' in drug_website[q]:
                             return 'phase 1'
                         elif 'I' in drug_website[q+1]:
                             return 'phase 1'

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
    def total_web_page_parse(self, ProposedDrugs, DrugWebsite):
        finalList = []
        phaseCorrect = 0
        EntryCorrect = 0
        totalEntry = 0
        for q in range(0, len(ProposedDrugs)):
            currentDrug = self.ultimate_analytics(ProposedDrugs[q], DrugWebsite)
            for z in range(0, len(currentDrug)):
                finalList.append(currentDrug[z])

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
        return finalList

# Class method to run only when called from terminal
def main():
    url = "https://www.biogen.com/en_us/research-pipeline/biogen-pipeline.html"

    company_name = "Biogen"

    full_parser = FullParser(company_name, url)

    jo = full_parser.final_list
    shmo = full_parser.second_filter

    print(full_parser.total_web_page_parse(shmo,jo))
    print(full_parser.ultimate_analytics(shmo[1],jo))
    print(full_parser.high_precision_filter(jo,shmo[1]))
    print(shmo[1])
    print('Percentage of Drugs with phase information available:')
    print((((1-(full_parser.PhasesRight/full_parser.TotalEntries))*100)))
    print('Percentage of Drugs with treatment information available:')
    print((((1-(full_parser.InfoFilled/full_parser.TotalEntries))*100)))


if __name__ == "__main__":
    main()