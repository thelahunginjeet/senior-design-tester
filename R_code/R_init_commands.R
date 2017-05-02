
setwd("~/Desktop/BME-SD-2016")

drug_data_all = read.csv("i_files/drug_data_all_cache.csv", header=TRUE, sep="\t", stringsAsFactors = FALSE)
drug_data_high = read.csv("i_files/drug_data_high_cache.csv", header=TRUE, sep="\t", stringsAsFactors = FALSE)
drug_data_low = read.csv("i_files/drug_data_low_cache.csv", header=TRUE, sep="\t", stringsAsFactors = FALSE)
log_file = read.csv("i_files/log_entries_cache.csv", header=TRUE, sep="\t", stringsAsFactors = FALSE)