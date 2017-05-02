# Pharmacuetical Web Scraper

### INTRODUCTION
This program will scrape pharmaceutical drug information from each respective company website and save this information into a csv file. This can be later read using R to analyze this information. It currently only reads websites in HTML format.


### REQUIREMENTS
This software requires a working distribution of Python 3 or later running on Linux or Mac. This program does not work on Windows as pyenchant does not have a working wheel for the 64 bit of python running on Windows. 


### INSTALLATION
Clone or extract repo in designated location. No installation is necessary.


### CONFIGURATION

**_company_names.txt_**

By default, the program will use a pre-populated list of the top pharmaceutical websites. If you would like to use a custom list, you can do this as well. The company names must be a text file (.txt) with one company name on each line. For example, the format must be as follows:
```
company 1
company 2
company 3
```
This file can be called anything, without spaces, but we chose to name it the same as the default file. Once this file is created, it can be located anywhere on your system. Just remember the path to that file. For example: `~/Documents/company_names.txt`


**_python version_**

Because this project is able to run on any version of python 3, there is some freedom as to what distro you would like to use. By default, a working version of Anaconda Python 3.6 is included with all the required packages and libraries pre-installed. If you would like to use this included distro, proceed with the instructions.

If you would like to specify your own version of python, then certain configuration steps must be taken to have the necessary packages. 
1. Open Terminal at the project location
2. Run `python3 --version`
3. This will tell you the version of python you are using; make sure this is python 3. If python 3 is default in your system, you may use the python keyword instead of python3.
4. If you have a custom path of python, replace the 'python3' with your path of python. 
5. Run `sudo pip3 install -r requirements.txt` to install the necessary packages. A password may be required to install them. If you do not have root permission, you can use the included python distro which already has the necessary python packages. 
6. When you follow the instructions in the Usage section, replace the python path used with 'python3' or your custom path.


### USAGE
Option 1: (Running program from terminal)
1. Open terminal at project location.
2. Read Configuration Section
3. If you would like to use your own company names list, refer to the 'company_names.txt' section under Configuration.
4. If you would like to use your own version of python, refer to the 'python factor' section under Configuration.
5. Run `project_path/anaconda3/bin/python main.py txtfile` where project\_path is the path to the project location and txtfile is the path to the company\_names.txt file you want to use. If you want to keep the default, you can ignore this parameter.
6. Wait until finish. 

Option 2: (Running program directly from R)
1. Open R console
2. Navigate to the working directory by running `setwd("~/project_path")` where project_path is the location of the project root.
3. Run `system("project_path/anaconda3/bin/python main.py txtfile")` where project_path is the path to the project location and txtfile is the path to the company\_names.txt file you want to use. If you want to keep the default, you can ignore this parameter.
4. Since there is no real time response from the system to R, no visual feedback will be seen until program is finished running. Depending on the size of the list of company names, this could take a while. 


### OUTPUT
1. The csv's will be loaded into the folder called 'i_files'. There will be four files, log\_entries\_cache.csv, drug\_data\_all\_cache.csv, drug\_data\_high\_cache.csv, and drug\_data\_low\_cache.csv.
2. In R console, you can load these dataframes by using these commands:
```R
    log_file = read.csv("i_files/log_entries_cache.csv", header=TRUE, sep="\t", stringsAsFactors = FALSE)
    drug_data_all = read.csv("i_files/drug_data_all_cache.csv", header=TRUE, sep="\t", stringsAsFactors = FALSE)
    drug_data_high = read.csv("i_files/drug_data_high_cache.csv", header=TRUE, sep="\t", stringsAsFactors = FALSE)
    drug_data_low = read.csv("i_files/drug_data_low_cache.csv", header=TRUE, sep="\t", stringsAsFactors = FALSE)
```
log_file will contain a dataframe of all the companies that were scraped along with flags
drug_data_all will be all the drugs scraped from the program
drug_data_high will be all the drugs scraped that were known to be accurate about a certain threshold
drug_data_low will be all the drugs scraped that did not reach this accuracy threshold

flags
```
'PDF link provided' : A PDF link was found on the website. This is only checked when the html scrape rate is below 20
'Data is not up to accuracy standards'  :  The html scraper couldn't find enough phase information for the drugs found.
'Can't find pipeline or DNE!'  :  The google_bot could not find a pipeline link. This may be because it does not exist.
'Error attempting to reach website!'  :  Umbrella term for all errors within the full_parser.py
```
### FULL R METHOD
If you would like to use this program fully from a R console, then this is possible too. 
1. Open R console at the project location. 
2. Find the path to the python distro you would like to use. Lets call this pythonpath for this instructions.
3. Find the path to the python distro you would like to use. In that directory should be a pip file. Lets call the path to that pip file pippath.
3. Run `sudo **pippath** install -r requirements` where **pippath** is the location of pip in the python distro.
4. Run `pythonpath main.py txtfile` where pythonpath is the location of python and txtfile is the location of the txt file of the company names you would like to use.
5. Either run the R script in the 'r_code' folder or manually import the csv's files located in the 'i_files' folder into R. 

NOTE: We noticed this process does not work sometimes in RStudio and some other R IDE's as they are unable to process password requests and provide real time feedback of the program running. We prefer running this from the terminal calling R. If you encounter any errors during this process, then try the other procedures located in the "USAGE" section above. 


### KNOWN ISSUES
* Does not run on Windows
* Program sometimes points to wrong version of Python installed in system. In these cases, replace 'python' with known python installation location.

### FUTURE ADDITIONS
* Option to save pdf file for known pdf links.
* Option to add more mechanisms and medical terminology into the dictionary.

