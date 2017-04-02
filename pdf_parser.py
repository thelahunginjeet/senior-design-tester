import re
from bs4 import BeautifulSoup
import requests
import enchant
import os
from io import BytesIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter#process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

class PdfParser:

    def __init__(self):
        self.eng = enchant.Dict("en_US")

    def run(self, _download_url):
        # pdf_name = self.download_file(_download_url)
        pdf_name = "input.pdf"
        raw_text = self.convert(pdf_name)
        visible_text = self.prime_text(raw_text)
        FinalList = self.process(visible_text)
        self.search_list(FinalList)


    def prime_text(self, raw_text):
        soup = BeautifulSoup(raw_text, "lxml").text

        # For seeing output
        # with open("input.txt", 'w') as f:
        #     f.write(soup)
        # os.remove("input.pdf")
        return soup

    def download_file(self, download_url):
        """
        :param download_url: string
        :Generates a xlsx file from the pdf to examine
        """
        response = requests.get(download_url)
        pdf_name = "input.pdf"
        with open(pdf_name, 'wb') as f:
            f.write(response.content)
        return pdf_name

    # https://www.binpress.com/tutorial/manipulating-pdfs-with-python/167
    def convert(self, pdfname):

        # PDFMiner boilerplate
        rsrcmgr = PDFResourceManager()
        sio = BytesIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # Extract text
        fp = open(pdfname, 'rb')
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
        fp.close()

        # Get text from StringIO
        raw_text = sio.getvalue()

        # Cleanup
        device.close()
        sio.close()
        # os.remove(pdfname)

        return raw_text


    def process(self, visible_text):
        list_of_words = visible_text.split()

        # Removing punctuation
        fixed_list =  []
        for word in list_of_words:
            word = word.replace(",","")
            word = word.replace(":", "")
            word = word.replace("<", "")
            word = word.replace(">", "")
            word = word.replace("]", "")
            word = word.replace("[", "")
            word = word.replace(")", "")
            word = word.replace("(", "")
            word = word.replace(";", "")

            p1 = re.compile(r"[\w]+?[\.!,]$")
            p2 = re.compile("^\d+$")
            if re.match(p1, word):
                # pass
                word = word.replace(".","")

            if re.match(p2, word):
                pass
            else:
                fixed_list.append(word)

        return fixed_list
        # for i in range(0, len(fixed_list)):
        #     current_word = fixed_list[i]
        #     if not self.eng.check(current_word):
        #         if self.is_relevant(fixed_list, i):
        #             print(current_word)
                # pattern1 = re.compile(r'MK.+')
                # pattern2 = re.compile(r'V\d.+')
                # if re.match(pattern1, current_word):
                #     print(current_word)
                # elif re.match(pattern2, current_word):
                #     print(current_word)




        # print(list_of_words)

    def is_relevant(self, main_list, index):
        limit = 100
        for x in range(index-limit, index+limit):
            if x < len(main_list):
                if re.match("phase", main_list[x], re.IGNORECASE):
                    return True
        return False


    def search_list(self, FinalList2):
        iterat=len(FinalList2)
        FirstFilter = []
        company_name = "Merck"
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

                appe = self.eng.check(newstr)

                if appe==False:
                    temp=len(newstr)
                    if temp>=5:
                        temps=FinalList2.count(FinalList2[x])
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
                                    FirstFilter.append(news)

        #apple=eng.check(FinalList[x])
        SecondFilter=list(set(FirstFilter))
        print(SecondFilter)

    def checking_official(self, currentCheck):
        p1 = re.compile(r"\b[A-Za-z]+(vir|cillin|mab|ximab|zumab|tinib|vastatin|prazole|lukast|axine|olol|oxetine|sartan|pril|pib|oxacin|xaban|afil|ine|parib|tide)\b")
        p2 = re.compile(r"\b[A-Za-z]+(grel|barb|prost)[A-Za-z]+\b")
        p3 = re.compile(r"\b(cef)[A-Za-z]+\b")
        p4 = re.compile(r"[A-Z].+\d$")
        p5 = re.compile(r'V\d.+')
        drug_target="N/A"
        currentLast=len(currentCheck);

        if re.match(p1, currentCheck): # Suffix testing
            return currentCheck
        elif re.match(p2, currentCheck): # Infix testing
            return currentCheck
        elif re.match(p3, currentCheck): # Prefix testing
            return currentCheck
        elif re.match(p5, currentCheck): # Prefix testing
            return currentCheck
        elif re.match(p4, currentCheck): # Number ending
            drug_target="Some Weird Number Thing"
            return currentCheck

        return 'null'





if __name__ == "__main__":
    pipeline_url = "http://www.merck.com/research/pipeline/MerckPipeline.pdf"
    # pipeline_url = "http://www.pfizer.com/sites/default/files/product-pipeline/013117-Pipeline-Update.pdf"
    # pipeline_url = "http://www.shionogi.co.jp/en/company/pmrltj0000000u4v-att/e_kaihatsu.pdf"

    pdf_parser = PdfParser()
    pdf_parser.run(pipeline_url)
    print("Completed")
