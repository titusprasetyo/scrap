
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time
import sqlite3
import re



def scrap_aliexpress_main(url):

    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    # chrome_options.add_experimental_option("prefs",prefs)
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
    driver = webdriver.Chrome('chromedriver',options=chrome_options)
    driver.implicitly_wait(30)
    driver.maximize_window()


    driver.get(url)

    last_height = driver.execute_script("return document.body.scrollHeight")
    print("last height {}".format(last_height))
    SCROLL_PAUSE_TIME = 0.5
    SCROLL_INTERVAL = 1000
    start = 0
    end = 0
    while True:
        end = start + SCROLL_INTERVAL
        driver.execute_script("window.scrollTo({}, {});".format(start,end))
        time.sleep(SCROLL_PAUSE_TIME)
        if start >= last_height:
            break
        start = end

    data = []
    # rows = [None] * 2
    elems = driver.find_elements_by_xpath('//a[@class="item-title"]')
    for elem in elems:
        href = elem.get_attribute("href")
        href = re.sub(r'\?\S+', '', href)
        name = elem.text
        # rows[0] = name
        # rows[1] = href
        if len(href.split("/"))==5:
            rows = [name,href]
            print(rows)
            data.append(rows)

    driver.quit()

    conn = sqlite3.connect('../data/scrap.aliexpress.db')
    df = pd.DataFrame(data,columns=['name','href'])
    df.to_sql('aliexpress_consumer_electronic_main', conn, if_exists="append", index = False)
    data.clear()


if __name__ == '__main__':
    pages = 60
    url = "https://www.aliexpress.com/af/category/44.html?trafficChannel=af&catName=consumer-electronics&CatId=44&ltype=affiliate&isFreeShip=y&isFavorite=y&SortType=total_tranpro_desc&page={}&groupsort=1&isrefine=y"
    for page in range(1, pages+1):
        urls = url.format(page)
        scrap_aliexpress_main(urls)
        # print(urls)