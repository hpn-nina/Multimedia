import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import os
import time



link_list = []
def getLink(keyword, quantity):
    address = "https://timkiem.vnexpress.net/?q=" + keyword
    res = requests.get(address)  
    objBFSoup = BeautifulSoup(res.text, 'html.parser')  
    tag_h3 = objBFSoup.find_all('h3', attrs={'class': 'title-news'})

    for tag_a_item in tag_h3:
        link_ = tag_a_item.a.get('href')
        if link_.startswith('https://vnexpress.net/topic'):
            continue
        if link_.startswith('https://video'):
            continue
        link_list.append(link_)
        if len(link_list) == quantity:
            break



def getArticle(link):
    # get title
    res_ = requests.get(link)
    soup = BeautifulSoup(res_.text, 'html.parser')
    tag_div = soup.find_all('div', attrs={'class': 'sidebar-1'})
    if len(tag_div) == 2: 
        res_ = requests.get(link)
        soup = BeautifulSoup(res_.text, 'html.parser')
        tag_div = soup.find_all('div', attrs={'class': 'container'})
        for tag_div_h1 in tag_div:
            tag_h1 = tag_div_h1.find_all('h1')
            for tag_h1_title in tag_h1:
                title = tag_h1_title.get_text()
    else:
        for tag_div_h1 in tag_div:
            tag_h1 = tag_div_h1.find_all('h1')
            for tag_h1_title in tag_h1:
                title = tag_h1_title.get_text()

    # get content
    content_ = []
    res_ = requests.get(link)
    soup = BeautifulSoup(res_.text, 'html.parser')
    tag_div = soup.find_all('div', attrs={'class': 'sidebar-1'})
    if len(tag_div) == 2:
        res_ = requests.get(link)
        soup = BeautifulSoup(res_.text, 'html.parser')
        tag_div = soup.find_all('div', attrs={'class': 'container'})
        for tag_div_article in tag_div:
            tag_article = tag_div_article.find_all('article')
            for tag_article_p in tag_article:
                tag_p = tag_article_p.find_all('p')
        for tag_p_text in tag_p:
            content_.append(tag_p_text.get_text())
    else:
        for tag_div_article in tag_div:
            tag_article = tag_div_article.find_all('article')
            for tag_article_p in tag_article:
                content_.append(tag_article_p.get_text())
    
    # get comment
    driver_path = "./crawler/driver/chromedriver"
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(link)
    comment = {}
    #driver.maximize_window()
    xpath = "//*[@id='list_comment']"
    try:
        cmt = driver.find_element(by=By.XPATH, value=xpath)
        driver.execute_script("arguments[0].scrollIntoView();", cmt)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find_all('div', class_="content-comment")
        for div_p in div:
            tag_p = div_p.find('p', class_="full_content")
            tag_span = tag_p.find('span')
            user_name = tag_span.find('a', class_="nickname").b.get_text()
            #comment.append(user_name)
            cnt = tag_p.contents[1].strip()
            comment[user_name] = str(cnt)
    except NoSuchElementException:
        comment = 'There is no comment on this post'

    return {
        "title" : title,
        "content" : content_,
        "comment" : comment
    }


def crawl(keyword, quantity):
    full = []
    getLink(keyword_, quantity)
    for crawl_ in link_list:
        full.append(getArticle(crawl_))
    return full


