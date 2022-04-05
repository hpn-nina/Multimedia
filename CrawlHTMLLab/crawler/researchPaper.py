from lib2to3.pgen2 import driver
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
import os
from decouple import config


import warnings
warnings.filterwarnings("ignore")

# Stratergy
# Get Into the Search page and get all href that have the link type "/document/number"


def crawler (keyword, author=True, num_papers=10): 
    
    def scroll(browser):
        '''
        Scroll to the bottom of the browser
        browser: selenium browser
        '''
        # scroll to the bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        
    def get_number_of_page(browser):
        '''
        From the base browser page get the number of page
        browser: selenium browser
        '''
        page = bs(browser.page_source, 'html')
        pagination = page.select_one('div.pagination-bar')
        if(pagination == None):
            return 0
        else:
            return int(pagination.find_all('a')[-3].get_text())

    
    def go_to_each_page(browser, num_paper, author=True):
        '''
        function for going into each page base on the base url
        browser: selenium browser
        num_page: number of page
        num_paper: number of paper
        author: True if want to get author, False if you want to get all meta data involve
        '''
        real_page_number = np.inf
        search_query = keyword_to_url(keyword,author) + "&pageNumber="
        paper_links = np.array([])
        page = 1
        
        while len(paper_links) < num_paper and page < real_page_number:
            search_query = search_query + f"{page}"
            browser.get(search_query)
            if page == 1:
                time.sleep(3) 
                real_page_number = get_number_of_page(browser)

            scroll(browser)

            link_in_page = get_links_from_page(browser, num_paper - len(paper_links))
            paper_links = np.append(paper_links, np.unique(np.array(link_in_page)))
            page += 1
            
        papers = []
        paper_links = np.unique(np.array(paper_links))
        for link in paper_links:
            paper = get_information_from_link(browser, link)
            papers.append(paper)
            
        return (papers if len(papers) else "There is no paper that fit")
            
    def get_links_from_page(browser, num_paper):
        '''
        Get all the links in the search page
        browser: selenium browser
        num_paper: The number of paper you want to get
        '''
        paper_links = []
        
        scroll(browser)
        page = bs(browser.page_source, 'html')
        raw_links = page.find_all("a", href=re.compile("document"))
        for link in raw_links:
            href = link.get("href") # Get the href field of all the raw links received
            if "citations" not in href and href not in paper_links:
                paper_links.append(href)
            if len(paper_links) == num_paper:
                break
            
        
        return paper_links
    
    def get_information_from_link(browser, paper_link):
        '''
        Get all the fields from the paper link
        browser: selenium browser
        paper_link: The link that fit "/document/" in previous search page
        '''
        url = base_url[:-1] + paper_link
        browser.get(url)
        time.sleep(2)
        scroll(browser)
        page = bs(browser.page_source, 'html')
        title = page.find("h1", class_="document-title")
        if title: 
            title = title.find("span").get_text()
        else: 
            title = ''
            
        authors = page.find("span", class_="authors-info-container")
        if authors : 
            authors = authors.find_all("span", class_="authors-info").get_text()
        else: 
            authors = ''
        
        abstract = page.find("div", class_="u-mb-1")
        if abstract : 
            abstract = abstract.find("div").get_text()
        else: 
            abstract = ''
        
        origin = page.find("div", class_="u-pb-1 stats-document-abstract-publishedIn")
        if origin : 
            origin = origin.find("a").get_text()
        else: 
            origin = ''
            
        date = page.find("div", class_="u-pb-1 doc-abstract-confdate")
        if date : 
            date.get_text()
        else: 
            date = ''
        
        return {
            "link": paper_link,
            'title': title,
            'authors': authors,
            'abstract': abstract,
            "origin": origin,
            "date": date
        }
    
    def keyword_to_url(keyword, author=True):
        string_keyword = keyword.replace(' ', '%20')
        tag = ("%22Authors%22" if author else "%22All%20Metadata%22")
        url = base_url + f"/search/searchresult.jsp?action=search&newsearch=true&matchBoolean=true&queryText=({tag}:{string_keyword})"
        
        return url
    
    papers = []
    base_url = config('IEEE_BASE_URL')
    proxy = config('PROXY')
    
    option = Options()
    #option.add_argument("--proxy-server=%s" % proxy)
    option.add_argument("--disable-infobars")
    option.add_argument('headless') # Add to unsee the browser
    option.add_argument('--disable-gpu')
    option.add_argument("--disable-extensions")
    option.add_argument("--disable-web-security")
    
    current_path = os.getcwd()
    driver_path = ("./driver/chromedriver.exe" if current_path.find("crawler") != -1 else "./crawler/driver/chromedriver.exe")
    browser = webdriver.Chrome(executable_path=driver_path, options=option)

    papers = go_to_each_page(browser, num_papers, author)
    return papers
