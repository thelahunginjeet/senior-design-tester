import re
from bs4 import BeautifulSoup
import requests
import enchant
import pdftables_api
from io import BytesIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter#process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

eng= enchant.Dict("en_US");

class PdfParser:

    def __init__(self, _download_url):
        pdf_name = self.download_file(_download_url)
        raw_text = self.convert(pdf_name)
        self.prime_text(raw_text)

    def prime_text(self, raw_text):
        soup = BeautifulSoup(raw_text, "lxml")
        strdata = soup.prettify();
        # print(soup.text)
        with open("input.txt", 'w') as f:
            f.write(strdata)

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

        return raw_text

if __name__ == "__main__":
    pdf_parser = PdfParser("http://www.merck.com/research/pipeline/MerckPipeline.pdf")
    # pdf_parser = PDFParser("http://www.pfizer.com/sites/default/files/product-pipeline/013117-Pipeline-Update.pdf")
    print("Completed")
