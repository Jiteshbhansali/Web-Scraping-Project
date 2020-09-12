# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 19:35:09 2020

@author: hp
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Create values Selenium
COMPANY = input("Enter Company ID: ") #Uber = 1815218
USERNAME = input("Enter username: ")
PASSWORD = input("Enter password: ")
EMPLOYEE = 300 #int(raw_input("Enter number of results: "))
linkedin = 'https://www.linkedin.com'

# Open Selenium
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(linkedin)
time.sleep(3)






email = browser.find_element_by_name('session_key')
password = browser.find_element_by_name('session_password')
email.send_keys(USERNAME + Keys.RETURN)
password.send_keys(PASSWORD + Keys.RETURN)




df = pd.DataFrame(columns = ['name', 'title', 'location', 'profile'])

for i in range(1,3):
    
    search = "https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%22" + str(COMPANY) + "%22%5D&page="+str(i)           
    browser.get(search)
    time.sleep(3)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    
    
    page = BeautifulSoup(browser.page_source, 'html5lib')
    page_names = page.find_all('span', {"class": ["name actor-name", "actor-name"]})
    page_titles = page.find_all('p', class_ = 'subline-level-1 t-14 t-black t-normal search-result__truncate')
    page_locations = page.find_all('p', class_ = 'subline-level-2 t-12 t-black--light t-normal search-result__truncate')
    page_profiles = page.find_all('a', {"class": ['search-result__result-link ember-view','search-result__result-link loading disabled ember-view']})
    
    
    
    
    
    names = list(map(lambda x: x.text, page_names))
    titles = list(map(lambda x: x.text.replace('\n', ''), page_titles))
    locations = list(map(lambda x: x.text.replace('\n', ''), page_locations))
    profiles = list(map(lambda x: linkedin + x['href'], page_profiles))[::2]
    #print(names,len(names))
    #print(titles,len(titles))
    #print(locations,len(locations))
    #print(profiles,len(profiles))
    temp = pd.DataFrame({'name':names, 'title':titles, 'location':locations, 'profile':profiles})
    temp = temp[temp['name'] != 'LinkedIn Member']
    

    df = df.append(temp)


df.reset_index()

# Export results
df.to_csv("output_search.csv", index = False)

# Close Selenium
browser.quit()