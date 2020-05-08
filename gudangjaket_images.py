# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time
import sqlite3
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# %%
#grab detail
conn = sqlite3.connect('scrap.gudangjaket.db')
cur = conn.cursor()
cur.execute('select a.href, a.name from GUDANGJAKET_MASTER a left join GUDANGJAKET_IMAGES b on a.name=b.name where b.name is null limit 20')
reader = cur.fetchall()
data_images = []

for line in reader:
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    # chrome_options.add_argument('headless')
    driver = webdriver.Chrome('chromedriver',options=chrome_options)
    driver.implicitly_wait(30)
    driver.maximize_window()
    driver.get(line[0])
    elems = driver.find_elements_by_xpath('//div[@data-testid="PDPImageThumbnail"]')
    counting = 0
    product_image = []
    for elem in elems:
        counting = counting + 1
        elem.click()
        time.sleep(3)
        # WebDriverWait(driver, 3).until(EC.presence_of_element_located(driver.find_elements_by_xpath('//img[@alt="product image"]')))
        elems = driver.find_element_by_xpath('//img[@alt="product image"]')
        product_image.append(elems.get_attribute("src"))
        # print(elems.get_attribute("src"))
        if counting == 5:
            break
    driver.quit()
    time.sleep(2)
    if len(product_image) == 5:
        rows = [line[1],product_image[0],product_image[1],product_image[2],product_image[3],product_image[4]]
    if len(product_image) == 4:
        rows = [line[1],product_image[0],product_image[1],product_image[2],product_image[3],None]
    if len(product_image) == 3:
        rows = [line[1],product_image[0],product_image[1],product_image[2],None, None]
    if len(product_image) == 2:
        rows = [line[1],product_image[0],product_image[1],None, None, None]
    if len(product_image) == 1:
        rows = [line[1],product_image[0],None, None, None, None]
    # print(rows)
    data_images.append(rows)

    #insert images
    df = pd.DataFrame(data_images,columns=['name','images1','images2','images3','images4','images5'])
    conn = sqlite3.connect('scrap.gudangjaket.db')
    df.to_sql('GUDANGJAKET_IMAGES', conn, if_exists='append', index = False)
    time.sleep(2)
    data_images.clear()


# %%


