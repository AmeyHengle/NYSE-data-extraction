# Task 2: Scrape data from the NYSE website


## Problem Statement:

Build a generic Scraper in python to Collect the below listed data points from this website : https://www.nyse.com
a. Actual name in listing Inside “Quote” section.
b. Last Trade Time.
 

## Proposed System:

For dynamically parsing the contents of nyse website, I use selenium, a python implementation of bindings for the Selenium WebDriver. Using selenium, the program is able to automatically navigate to the results page corresponding to the input entity name. 

After getting the search results, I sort them using levenshtein distance to get the most appropriate match for the input search query. The best match corresponds to the lowest levenshtein distance. For example, the search query ‘WFC: Wells Fargo & Company’ will get mapped to the result ‘WELLS FARGO & COMPANY’  instead of WELLS FARGO & COMPANY 7.5% PERP CONV PRF CLS 'A' SERIES 'L'. 

## Usage:

1. Install dependencies stated in requirements.txt. 
2. Run the run.py file and pass the term-name as a command line argument.
<br>Eg: 	python  run.py  “Wells Fargo & Company” <br>
3. Collect the results from the results folder.

## Requirements:
selenium
urllib
python-Levenshtein
json


