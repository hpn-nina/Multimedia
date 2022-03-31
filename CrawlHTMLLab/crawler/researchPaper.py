from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
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
        time.sleep(0.5)
        
    def getNumberOfPage(browser):
        page = bs(browser.page_source, 'html')
        pagination = page.select_one('div.pagination-bar')
        if(pagination == None):
            return 0
        else:
            return int(pagination.find_all('a')[-3].get_text())

    
    def goToEachPage(browser, numPage, numPaper, author=True):
        realPagesNumber = 2
        pageQuery = "&pageNumber="
        base_search_query = kwToURL(keyword,author) + pageQuery
        paper_links = np.array([])
        page = 1
        loop = 0
        
        while len(paper_links) < numPaper and loop < 100 and page < realPagesNumber:
            search_query = base_search_query + f"{page}"
            browser.get(search_query)
            time.sleep(5)
            scroll(browser)
            if page == 1:
                realPagesNumber = min(numPage, getNumberOfPage(browser))
                
            papersInPage = getAllPaperLinks(browser, numPaper)
            paper_links = np.append(paper_links, np.unique(np.array(papersInPage)))
            page += 1
            loop += 1
            
        papers = []
        paper_links = np.unique(np.array(paper_links))
        for link in paper_links:
            paper = getInformationOfPaper(browser, link)
            papers.append(paper)
            
        return papers
            
    def getAllPaperLinks(browser, numPaper):
        paper_links = []
        while len(paper_links) < numPaper:
            scroll(browser)
            page = bs(browser.page_source, 'html')
            raw_links = page.find_all("a", href=re.compile("document"))
            
            for link in raw_links[len(paper_links):numPaper]:
                href = link.get("href")
                if(len(href) < 25):
                    paper_links.append(href)
        
        return paper_links
    
    def getInformationOfPaper(browser, paper_link):
        url = base_url[:-1] + paper_link
        browser.get(url)
        time.sleep(2)
        scroll(browser)
        page = bs(browser.page_source, 'html')
        title = page.find("h1", class_="document-title")
        if title: 
            title = title.find("span").get_text()
        else: title = ''
        authors = page.find("span", class_="authors-info-container")
        if authors : 
            authors = authors.find_all("span", class_="authors-info").get_text()
        else: authors = ''
        abstract = page.find("div", class_="u-mb-1")
        if abstract : 
            abstract = abstract.find("div").get_text()
        else: abstract = ''
        origin = page.find("div", class_="u-pb-1 stats-document-abstract-publishedIn")
        if origin : 
            origin = origin.find("a").get_text()
        else: origin = ''
        date = page.find("div", class_="u-pb-1 doc-abstract-confdate")
        if date : date.get_text()
        else: date = ''
        return {
            "link": paper_link,
            'title': title,
            'authors': authors,
            'abstract': abstract,
            "origin": origin,
            "date": date
        }
    
    def kwToURL(keyword, author=True):
        string_keyword = keyword.replace(' ', '%20')
        if author == True:
            tag = "%22Authors%22"
        else:
            tag = "All%20Metadata"
        url = base_url + f"/search/searchresult.jsp?action=search&newsearch=true&matchBoolean=true&queryText=({tag}:{string_keyword})"
        url = "https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&newsearch=true&matchBoolean=true&queryText=(%22All%20Metadata%22:nguyen%20van)"
        return url
    
    papers = []
    base_url = config('IEEE_BASE_URL')
    proxy = config('PROXY')
    
    option = Options()
    #option.add_argument("--proxy-server=%s" % proxy)
    option.add_argument("--disable-infobars")
    option.add_argument('headless')
    option.add_argument("--disable-extensions")
    browser = webdriver.Chrome(executable_path="./crawler/driver/chromedriver.exe", options=option)

    papers = goToEachPage(browser, 1000, num_papers, author)
    return papers
