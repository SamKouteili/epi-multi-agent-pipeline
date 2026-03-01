#
# Update data objects in package EPI
# Martin Wolf, March 24, 2021
# Further updates by Jay and team, April 4, 2023
#
# This script helps explore and update critically important input files,
# specifically MasterFile.csv and cdictionary_expanded.csv, and
# constituent country information, and provides
# a mechanism for easily updating the data objects of package EPI.
#
# TO DO: Consider removing entries in expanded cdictionary that have have
# problematic foreign language characters. I.e. we want the package check to
# run without warnings. 
# 
# TO DO: low-tech: any script to process source data with nasty foreign language
# characters simply cleans the offending entries. High-tech: build a utility
# into the package to automate this.

dict <- read.csv("cdictionary_expanded.csv", as.is = TRUE)
MasterFile <- read.csv("MasterFile.csv", as.is = TRUE)
con <- read.csv("constituent_countries.csv", as.is = TRUE)

nrow(MasterFile)
length(unique(dict$right))
setdiff(dict$right, MasterFile$country) # Examine these for problems

save("dict", file = "../RPackage/EPI/data/dict.RData")
save("MasterFile", file = "../RPackage/EPI/data/MasterFile.RData")
save("con", file = "../RPackage/EPI/data/constituents.RData")

################################################################################

