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
import numpy as np

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
        if(not pagination):
            total_pages = 0
        else:
            total_pages = pagination.select_one('a.last').get('text')[-1:]
        return total_pages
    
    def goToEachPage(browser, numPage, numberOfPaperLeft):
        realPagesNumber = 1000
        pageQuery = "&pageNumber="
        base_search_query = kwToURL(keyword) + pageQuery
        
        paper_links = []
        while page <= realPagesNumber & len(paper_links) <= numberOfPaperLeft:
            search_query = base_search_query + f"{page}"
            browser.get(search_query)
            time.sleep(5)
            if page == 1:
                realPagesNumber = min(numPage, getNumberOfPage(browser))
                
            papersInPage = getAllPaperLinks(browser, numPapersLeft)
            papers += papersInPage
            
        papers = []
        for link in paper_links:
            paper = getInformationOfPaper(browser, link)
            papers.append(paper)
            
        return papers
            
    def getAllPaperLinks(browser, numPapersLeft):
        paper_links = []

        
        while len(paper_links) < numPapersLeft:
            scroll(browser)
            page = bs(browser.page_source, 'html')
            raw_links = page.find_all("a", href=re.compile("document"))
            
            for link in raw_links[len(paper_links):numPapersLeft]:
                paper_links.append(link.get('href'))
        
        return paper_links
    
    def getInformationOfPaper(browser, paper_link):
        browser.get(base_url, paper_link)
        time.sleep(2)
        scroll(browser)
        page = bs(browser.page_source, 'html')
        title = page.find("div", class_="document-title").get_text()
        authors = page.find("div", class_="authors-info-container").get_text()
        abstract = page.find("div", class_="abstract-text row").get_text()
        origin = page.find("div", class_="u-pb-1 stats-document-abstract-publishedIn").get_text()
        publisher = page.find("div", class_="publisher-title-tooltip").get_text()
        date = page.find("div", class_="u-pb-1 doc-abstract-confdate").get_text()
        
        return {
            "link": paper_link,
            'title': title,
            'authors': authors,
            'abstract': abstract,
            "origin": origin,
            "publisher": publisher,
            "date": date
        }
    
    def kwToURL(keyword):
        string_keyword = keyword.replace(' ', '%20')
        url = base_url + f"/search/searchresult.jsp?action=search&newsearch=true&matchBoolean=true&queryText=(%22Authors%22:{string_keyword})&highlight=true&returnFacets=ALL&returnType=SEARCH&matchPubs=true1"
        return url
    
    paper_links = []
    papers = []
    exec_path = "./crawler/driver/chromedriver"
    base_url = config('IEEE_BASE_URL')
    proxy = config('PROXY')
    
    option = Options()
    option.add_argument("--proxy-server=%s" % proxy)
    option.add_argument("--disable-infobars")
    option.add_argument('headless')
    option.add_argument("--disable-extensions")
    browser = webdriver.Chrome(executable_path="./crawler/driver/chromedriver.exe", options=option)
    
    papers = goToEachPage(browser, np.inf, num_papers)
    return papers