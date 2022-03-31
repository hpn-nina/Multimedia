# selenium-related
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# other necessary ones
import urllib.request
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import time
import re
import datetime
import copy

base_url = 'https://m.facebook.com/'

def login(browser, credentials_destination):
    with open(credentials_destination) as file:
        email = file.readline().split('=')[1][:-1]
        password = file.readline().split('=')[1]
        print(f'Try logging in with email:"{email}" and password:"{password}"')
    try:
        wait = WebDriverWait(browser, 50)
        email_field = wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
        email_field.send_keys(email)
        pass_field = wait.until(EC.visibility_of_element_located((By.NAME, 'pass')))
        pass_field.send_keys(password)
        pass_field.send_keys(Keys.ENTER)
        time.sleep(3)
        if browser.find_elements(By.CSS_SELECTOR, '#email'):
            print('Please check your email and password in facebook_credentials.txt!')
        else:
            checkpoint(browser)
            print('Logged in.')
    except :
        print('Something went wrong.')


def checkpoint(browser):
    t = 0
    while ( browser.find_elements(By.CSS_SELECTOR, '#approvals_code')):
        if t == 0:
            print('Please approve the login with your devices.')
            t+= 1
        else: 
            print('Waiting for approval...', t)
            t += 1
        time.sleep(5)


def scroll(browser):
    # scroll to the bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)


def numExtract(string):
    arr = string.split(' ')
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in arr:
        if i[0] in numbers:
            num = re.sub("[^0-9,]", '', i)
            num = re.sub("[^0-9]", '.', num)
            char = re.sub("[^A-z]", '', i)
            if char == 'K':
                return int(float(num) * 10**3)
            elif char == 'Tr':
                return int(float(num) * 10**6)
            else: return int(num)
    return 0
    



def getPostLink(browser, num_post):
    post_links = []
    likes = []
    comments_num = []

    print('Loading page posts...')

    while len(post_links) < num_post:
        # scoll to get posts with quantity equal to num_post
        scroll(browser)
        page = bs(browser.page_source, 'html')
        time.sleep(1)
        raw_links = page.find_all('a', class_='_5msj')
        chk = False
        try:
            raw_likes, raw_comments_num = page.find_all('div', class_='_1g06'), page.find_all('span', {'data-sigil':'comments-token'})
            if len(raw_likes) < len(raw_comments_num):
                temp = copy.copy(raw_comments_num[-1])
                temp.string.replace_with('0')
                raw_likes.append(temp)
            elif len(raw_likes) > len(raw_comments_num):
                temp = copy.copy(raw_likes[-1])
                temp.string.replace_with('0')
                raw_comments_num.append(temp)
            a = len(raw_likes) - len(raw_links)
            b = len(raw_comments_num) - len(raw_links)
            if a < 0:
                for i in range(-a):
                    temp = copy.copy(raw_links[-1])
                    temp.string = '0'
                    raw_likes.append(temp)
            if b < 0:
                for i in range(-b):
                    temp = copy.copy(raw_links[-1])
                    temp.string = '0'
                    raw_likes.append(temp)

        except: 
            likes.append(0)
            comments_num.append(0)
            chk = True

        for link in range(len(raw_links[0:len(raw_links)])):
            if len(post_links) > num_post:
                break
            link_ = base_url + raw_links[link]['href']
            if link_ not in post_links:
                post_links.append(link_)
            if not chk:
                likes.append(numExtract(raw_likes[link].text))
                #comments_num.append(numExtract(raw_comments_num[link].text))
            else: chk = False
        
    return post_links[:num_post], likes[:num_post]#, comments_num[:num_post]


def checkArr(arr):
    if len(arr) == 0:
        return 'null'
    return arr[0].text


def getComment(browser, num_comment):
    # scroll to load comment
    scroll(browser)
    switch = True
    af0 = bf0 = af1 = bf1 = 0

    # click on load more comment section
    while switch:
        try:
            raw_comments = browser.find_elements(By.CLASS_NAME, '_14v5')
            af0 = len(raw_comments)
            if af0 == 0: return []
            if af0 < num_comment and bf0 != af0:
                #if bf0 == af0: 
                #    switch = False
                #else:
                    load_more = browser.find_elements(By.CLASS_NAME, '_108_')[0]
                    load_more.click()
                    time.sleep(1)
                    scroll(browser)
                    print('Loading comments...')
            else: 
                try:
                    # load reply comments
                    load_more_rpl = browser.find_elements(By.XPATH, "//a[@data-sigil='ajaxify']")
                    af1 = len(load_more_rpl)
                    if af1 == bf1: switch = False
                    else:
                        bf1 = af1
                        for button in load_more_rpl:
                            button.click()
                            print('Loading reply-comments...')
                except:
                    if af0 == bf0: switch = False
                    print('Continue...')
            bf0 = af0
        except:
            try:
                # load reply comments
                load_more_rpl = browser.find_elements(By.XPATH, "//a[@data-sigil='ajaxify']")
                for button in load_more_rpl:
                    button.click()
                    print('Loading reply-comments...')
            except:    
                print('Continue...')
            switch = False
    print('Loadded all comments')
    time.sleep(2)
    comments_find = raw_comments[0].find_elements(By.XPATH,'//div[@data-sigil="comment-body"]')
    comments = [comments_find[i].text for i in range(len(comments_find))]
    name_find = raw_comments[0].find_elements(By.XPATH,'//div[@class="_2b05"]')
    commenter_name = [name_find[i].text for i in range(len(name_find))]
    
    comments_return = []
    for i in range(len(comments)):
        comments_return.append({
            'username': commenter_name[i],
            'comment': comments[i]
        })

    return comments_return



def getPost(browser, ith, likes, comments_num):

    section = {'content':[], 
               'comments':[],
               'post_likes': likes,
               'comments_num': comments_num}
    #content = []


    print(f'Crawling {ith}th post.')

    post = bs(browser.page_source, 'html')

    # get post content
    content_texts = post.findChildren('div', class_='_5rgt _5nk5')
    #content.append()

    # get post comment --> get user name, id and comment
    comments = getComment(browser, comments_num)

    # fill data into posts list
    section['content'] = [content_texts[0].text]
    section['comments'] = comments
    section['post_likes'] = likes
    section['comments_num'] = len(comments)

    return section

import os

def crawler(credentials_destination, target_page, num_post):

    page_crawl = []

    # set options as you wish
    option = Options()
    option.add_argument("--disable-infobars")
    #option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    print(os.getcwd())

    # open Facebook
    browser = webdriver.Chrome(executable_path="./Crawl/chromedriver.exe", options=option)
    browser.get("https://facebook.com")
    #browser.maximize_window()

    # log in
    login(browser, credentials_destination)
    time.sleep(1)

    # open target page
    browser.get(target_page) # once logged in, free to open up any target page

    # get all post links
    post_links, likes = getPostLink(browser, num_post)

    # get post content and comment
    for link in range(len(post_links)):
        browser.get(post_links[link])
        page_crawl.append(getPost(browser, link+1, likes[link], 20))
    print(page_crawl)
    return page_crawl
    #time.sleep(5)

def convertToJSON(data):
    json_format = json.dumps(data, ensure_ascii=False).encode('utf8')
    print(json_format)

def crawl(target_page, number_post):

    # your account email and password destination
    credentials_destination = './Crawl/facebook_credentials.txt'

    # your target page
    target_page = 'https://m.facebook.com/Original-C-100436262620945/'
    #target_page = 'https://m.facebook.com/' + target_page.split('/')[-2] + '/'

    # number of post to crawl
    number_post = 1

    # crawler
    return convertToJSON(crawler(credentials_destination, target_page, number_post))
crawl(0,0)