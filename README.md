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
3. run ```pip install -r requirements.txt```



CONFIGURATION
*************

1. Open terminal at location
2. run 'python main.py'
3. Open your choice of R IDE at the project location
4. import two dataframes into R
```
    drug_data = read.csv("drug_data_cache.csv", header=TRUE, sep="\t", stringsAsFactors = FALSE)
    log_file = read.csv("log_entries_cache.csv", header=TRUE, sep="\t", stringsAsFactors = FALSE)
```


KNOWN ISSUES
************

* Does not run on Windows
* Program sometimes points to wrong version of Python isntalled in system. In these cases, replace 'python' with known python installation loacation


