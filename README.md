# senior-design-tester
A sandbox for the 2016-2017 Senior Design team to experiment with git. 

INTRODUCTION
************

This program will scrape pharmacuetical drug information from each respective company website and save this information into a csv file. This can be later read using R to analyze this information. It currently only reads websites in HTML format.



REQUIREMENTS
************

This software requires a working distribution of Python 3 or later running on Linux or Mac. This program does not work on Windows as pyenchant does not have a working wheel for the 64 bit of python running on Windows.



INSTALLATION
************

1. Clone or extract repo in designated location
2. Open terminal at location
3. Run ```pip install -r requirements.txt```
4. Populate company_names.txt file with names of company names you want to scrap. By defualt, all top pharmacueticals will be loaded. 



CONFIGURATION
*************

1. Open terminal at location
2. Run ```python main.py```
3. Open your choice of R IDE at the project location
4. import two dataframes into R
```
    drug_data = read.csv("drug_data_cache.csv", header=TRUE, sep="\t", stringsAsFactors = FALSE)
    log_file = read.csv("log_entries_cache.csv", header=TRUE, sep="\t", stringsAsFactors = FALSE)
```

The drug_data will be all the drugs scraped from the program. 
The log_file will contain a dataframe of all the companies that were scraped along with flags

flags
```
'PDF link provided' : A PDF link was found on the website. This is only checked when the html scrape rate is below 20
'Data is not up to accuracy standards'  :  The html scraper couldnt find enough phase information for the drugs found.
'Can't find pipeline or DNE!'  :  The google_bot could not find a pipeline link. This may be because it does not exist.
'Error attempting to reach website!'  :  Umbrella term for all errors within the full_parser.py
```

KNOWN ISSUES
************

* Does not run on Windows
* Program sometimes points to wrong version of Python isntalled in system. In these cases, replace 'python' with known python installation location

FUTURE ADDITIONS
****************

* Option to save pdf file for known pdf links
* Option to add a high and low precision list instead of an aggregate list

