# selenium-related
from click import password_option
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
import requests
import re
import datetime
import copy
from PIL import Image
from io import BytesIO
import base64

def scroll(browser):
    # scroll to the bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

def getSrc(src):
    if src[:4] == 'data':
        raw = bytes('/' + src.split('/', 2)[-1], encoding='utf-8')
        return raw[raw.find(b'/9'):]
    else: return base64.b64encode(requests.get(src).content)

def getImage(browser, quantity):
    images = []

    while len(images) < quantity:
        scroll(browser)
        page = bs(browser.page_source, 'html')
        raw_link = page.find_all('img', class_='rg_i Q4LuWd')

        for i in raw_link[len(images):quantity]:
            try:
                img = getSrc(i.attrs['src'])
            except:
                img = getSrc(i.attrs['data-src'])
            #im = Image.open(BytesIO(base64.b64decode(raw)))
            #im.save('image1.png', 'PNG')
            images.append({
                'image': img.decode("utf-8"),
                'title': i.attrs['alt'],
            })

    return images


def kwToURL(keyword):
    url = 'https://www.google.com.vn/search?q='
    url += keyword.replace(' ', '+') + '&tbm=isch'
    return url


def crawler(keyword, quantity):
    

    # set options as you wish
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument('headless')
    option.add_argument('--log-level=3')
    #option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    # set up browser
    browser = webdriver.Chrome(executable_path="./crawler/driver/chromedriver.exe", options=option)

    # open target page
    browser.get(kwToURL(keyword))
    time.sleep(2)

    images = getImage(browser, quantity)

    return images
    #time.sleep(5)

def convertToJSON(data):
    #json_format = json.dumps(data, ensure_ascii=False).encode('utf8')
    return data

def crawl(keyword, quantity=3):
    quantity = int(quantity)


    # crawler
    return convertToJSON(crawler(keyword, quantity))