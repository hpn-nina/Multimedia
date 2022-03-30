from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer as ss
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import copy

from decouple import config


import warnings
warnings.filterwarnings("ignore")

# Stratergy
# Get Into the Search page and get all href that have the link type "/document/number"


def crawler (keyword, author=True, num_papers=10): 
    
    def scroll(browser):
        # scroll to the bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
    def getNumberOfPage(soup):
        pagination = soup.select_one('div.pagination-bar')
        print(pagination)
        if(not pagination):
            total_pages = 0
        else:
            total_pages = pagination.select_one('a.last').get('text')[-1:]
        return total_pages
    
    def getAllPaperLinks(soup):
        paper_links = []
        for link in soup.select('a[href*="/document/"]'):
            paper_links.append(link.get('href'))
        return paper_links
    
    paper_links = []
    papers = []
    exec_path = "./crawler/driver/chromedriver"
    base_url = config('IEEE_BASE_URL')
    proxy = config('PROXY')
    page_num = 1
    
    option = Options()
    option.add_argument("--proxy-server=%s" % proxy)
    option.add_argument("--disable-infobars")
    option.add_argument('headless')
    option.add_argument("--disable-extensions")
    browser = webdriver.Chrome(executable_path="./crawler/driver/chromedriver", options=option)
    search_query = f"{base_url}/search/searchresult.jsp?action=search&newsearch=true&matchBoolean=true&queryText=(%22Authors%22:{keyword})&highlight=true&returnFacets=ALL&returnType=SEARCH&matchPubs=true&pageNumber={page_num}"
    print(search_query)
    browser.get(search_query)
    
    html = browser.page_source
    soup = BeautifulSoup(html)
    time.sleep(15)
    print(soup)
    numberOfPage = getNumberOfPage(soup)

    return numberOfPage