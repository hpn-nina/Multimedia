import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import time



link_list = []
def getLink(keyword, quantity):
    address = "https://timkiem.vnexpress.net/?q=" + keyword
    res = requests.get(address)  
    objBFSoup = BeautifulSoup(res.text, 'html.parser')  
    tag_h3 = objBFSoup.find_all('h3', attrs={'class': 'title-news'})

    sl = 0
    for tag_a_item in tag_h3:
        link_ = tag_a_item.a.get('href')
        if link_.startswith('https://vnexpress.net/topic'):
            continue
        if link_.startswith('https://video'):
            continue
        link_list.append(link_)
        sl = sl + 1
        if sl == quantity:
            break



# get article title
def getArticleTitle(link):
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
                return tag_h1_title.get_text()
    else:
        for tag_div_h1 in tag_div:
            tag_h1 = tag_div_h1.find_all('h1')
            for tag_h1_title in tag_h1:
                return tag_h1_title.get_text()
           


# get article content
def getArticleContent(link):
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
        return content_
    else:
        for tag_div_article in tag_div:
            tag_article = tag_div_article.find_all('article')
            for tag_article_p in tag_article:
                content_.append(tag_article_p.get_text())
        return content_



comment = {}
# get Comment
def getComment(link):
    #current_path = os.getcwd()
    driver_path = "D:\chromedriver_win32\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(link)
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
    except:
        return comment
    return comment

# get article + comment
def getFullArticle(link):
    article = {"title": [], "content": [], "comment": []}
    article["title"].append(getArticleTitle(link))
    article["content"].append(getArticleContent(link))
    article["comment"].append(getComment(link))
    return article


keyword_ = "thích"
link_='https://vnexpress.net/sat-thu-thich-lo-minh-tren-amazon-4444751.html'
def crawl(keyword, quantity):
    full = []
    getLink(keyword_, quantity)
    for crawl_ in link_list:
        full.append(getFullArticle(crawl_))
    return full

print(crawl(keyword_, 3))


