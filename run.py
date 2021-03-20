#!/usr/bin/env python
# coding: utf-8

# In[32]:


import selenium.webdriver as webdriver
import urllib

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Levenshtein import distance as levenshtein_distance

import pandas as pd
import time
import sys
import json   



def make_search_query(url, term):
    
    """The function computes the relevant search query string.

    Args:
        url (str): Address of the main page of the website to scrap. (https://www.nyse.com)
        term (str): Entity name to be scrapped. (Eg: Wells Fargo & Company)

    Returns:
       search_query (str) : resultant URL to be parsed
    """
    search_query = url + search + urllib.parse.quote(term)
    return search_query



def get_results(link, term):
    
    """The function scrapes the information corresponding to the quote and last-datetime of the input entity term.

    Args:
        link (str): URL of the page to scrape the information from. 
        term (str): Entity name to be scrapped. (Eg: Wells Fargo & Company)

    Returns:
       result (dict) : a dictionary mapping datapoints to their corresponding extracted information. 
    """
    result = {}
    result["search_term"] = term
    result["link"] = link

    
    try:

        element = WebDriverWait(driver, 600).until(
                EC.presence_of_element_located((By.CLASS_NAME, "section-bleed"))
            )

        driver.get(link)

        element = WebDriverWait(driver, 600).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "d-dquote-x3"))
            )

    except Exception as e:
        print(e)

    search_quote = driver.find_element_by_class_name("d-dquote-x3")
    print(search_quote.text)
    last_trade_time = driver.find_element_by_class_name("d-dquote-time")
    print(last_trade_time.find_elements_by_tag_name("span")[1].text)  

    result["quote"] = search_quote.text
    result["last_trade_time"] = last_trade_time.find_elements_by_tag_name("span")[1].text
    
    return result

def find_best_match(term, candidate_results):
    """The function sorts the search results with repective to their levenshtein distances from the Entity term. 

    Args:
        term (str): Entity name to be scrapped. (Eg: Wells Fargo & Company)
        candidate_results (selenium.webelement): A selenium webelement which contains a list of all relavant results for the given Entity 
        name.
        
    Returns:
       best_match (tuple) : The tuple (distance, url) corresponding to the most relevant search result.
    """
    
    results = []
    
    for x in candidate_results:
        results.append((levenshtein_distance(term, x.text) , x.find_element_by_tag_name("a").get_attribute("href")))
        
    results = sorted(results, key = lambda x : x[0])
    best_match = results[0]
    
    return best_match


global url
global search

url = "https://www.nyse.com"
search = "/site-search?q="


# In[38]:



if __name__ == "__main__":
    
    term = sys.argv[1]
    results = []
    
    try:
        driver = webdriver.Chrome()
        search_query = make_search_query(url, term)
        driver.get(search_query)
        print("\nFetching term:", term)

        try:

            element = WebDriverWait(driver, 600).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "search-results"))
                )

        except Exception as e:
            print(e)

        search_element = driver.find_element_by_class_name("search-results")
        candidate_results = search_element.find_elements_by_class_name("search-results-title")

        best_match = find_best_match(term, candidate_results)

        result  = get_results(best_match[1], term)
        print("\n\n",result)


        with open("./results/"+term + ".results.json", "w") as outfile:  
            json.dump(result, outfile)

        print("\nCompleted")

        driver.close()
        
    except Exception as e:
        print("Exception while parsing data\n", e)


# In[ ]:




