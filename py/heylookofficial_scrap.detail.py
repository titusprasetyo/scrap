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

#grab detail
SQLMODE = "append"
conn = sqlite3.connect('../data/scrap.heylookofficial.db')
cur = conn.cursor()
cur.execute('select a.href, a.name from heylookofficial_master a left join heylookofficial_images b on a.name=b.name where b.name is null order by "a.index" limit 1')
# cur.execute('select a.href, a.name from heylookofficial_master a order by "a.index" limit 1')
reader = cur.fetchall()
data_images = []
data_variant = []
for line in reader:
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome('chromedriver',options=chrome_options)
    driver.implicitly_wait(30)
    driver.maximize_window()
    print("Fetch {}".format(line[0]))
    driver.get(line[0])
    
    # fetch images
    print("Fetch images")
    elems = driver.find_elements_by_xpath('//div[@data-testid="PDPImageThumbnail"]')
    counting = 0
    product_image = []
    for elem in elems:
        counting = counting + 1
        elem.click()
        time.sleep(3)
        elems = driver.find_element_by_xpath('//img[@alt="product image"]')
        src = elems.get_attribute("src")
        print(src)
        if src.startswith('data'):
            time.sleep(2)
            src = elems.get_attribute("src")
        product_image.append(src)
        if counting == 5:
            break
    time.sleep(2)
    rows_images = [None] * 13
    if len(product_image) == 5:
        # rows_images = [line[1],product_image[0],product_image[1],product_image[2],product_image[3],product_image[4]]
        rows_images[0] = line[1]
        rows_images[1] = product_image[0]
        rows_images[2] = product_image[1]
        rows_images[3] = product_image[2]
        rows_images[4] = product_image[3]
        rows_images[5] = product_image[4]
    if len(product_image) == 4:
        # rows_images = [line[1],product_image[0],product_image[1],product_image[2],product_image[3],None]
        rows_images[0] = line[1]
        rows_images[1] = product_image[0]
        rows_images[2] = product_image[1]
        rows_images[3] = product_image[2]
        rows_images[4] = product_image[3]
        rows_images[5] = None
    if len(product_image) == 3:
        # rows_images = [line[1],product_image[0],product_image[1],product_image[2],None, None]
        rows_images[0] = line[1]
        rows_images[1] = product_image[0]
        rows_images[2] = product_image[1]
        rows_images[3] = product_image[2]
        rows_images[4] = None
        rows_images[5] = None
    if len(product_image) == 2:
        # rows_images = [line[1],product_image[0],product_image[1],None, None, None]
        rows_images[0] = line[1]
        rows_images[1] = product_image[0]
        rows_images[2] = product_image[1]
        rows_images[3] = None
        rows_images[4] = None
        rows_images[5] = None
    if len(product_image) == 1:
        # rows_images = [line[1],product_image[0],None, None, None, None]
        rows_images[0] = line[1]
        rows_images[1] = product_image[0]
        rows_images[2] = None
        rows_images[3] = None
        rows_images[4] = None
        rows_images[5] = None

    # fetch weight
    print("Fetch Weight")
    elems = driver.find_elements_by_xpath('//p[@data-testid="PDPDetailWeightValue"]')
    for elem in elems:
        data_test = elem.get_attribute("data-testid")
        if data_test == "PDPDetailWeightValue":
            print(elem.text)
            product_weight = elem.text
            # row = [line[1], product_weight]
            # data_weight.append(row)
            rows_images[6]=product_weight

    # fetch category
    print("Fetch Category")
    elems = driver.find_elements_by_xpath('//ol[@data-testid="lnkPDPDetailBreadcrumb"]')
    for elem in elems:
        data_test = elem.get_attribute("data-testid")
        if data_test == "lnkPDPDetailBreadcrumb":
            product_cat = elem.text.replace(line[1],'')
            print(product_cat)
            # row = [line[1], product_cat]
            # data_cat.append(row)
            rows_images[7]=product_cat

    print("SPAN")
    elems = driver.find_elements_by_xpath('//span')
    for elem in elems:
        data_test = elem.get_attribute("data-testid")
        min_purchase = ""
        if data_test == "lblPDPMinPurchase":
            min_purchase = elem.text
            print(min_purchase)
            rows_images[8]=min_purchase
        success_rate = ""
        if data_test == "lblPDPDetailProductSuccessRate":
            success_rate = elem.text
            print(success_rate)
            rows_images[9]=success_rate
        rating_number = ""
        if data_test == "lblPDPDetailProductRatingNumber":
            rating_number = elem.text
            print(rating_number)
            rows_images[10]=rating_number
        product_views = ""
        if data_test == "lblPDPDetailProductSeenCounter":
            product_views = elem.text
            print(product_views)
            rows_images[11]=product_views
    
    #fetch variant
    print("Fetch Variant")
    elems = driver.find_elements_by_xpath("//div")
    for elem in elems:
        data_test = elem.get_attribute("data-testid")
        if data_test == "lblPDPProductVariantukuran":
            print(elem.text)
            row = [line[1], elem.text]
            data_variant.append(row)
        if data_test == "lblPDPProductVariantwarna":
            print(elem.text)
            row = [line[1], elem.text]
            data_variant.append(row)
    
    #fetch description and weight must scroll down
    print("Fetch description")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    elems = driver.find_elements_by_xpath('//p[@data-testid="lblPDPDeskripsiProduk"]')
    for elem in elems:
        data_test = elem.get_attribute("data-testid")
        if data_test == "lblPDPDeskripsiProduk":
            product_desc = elem.text
            print(elem.text)
            # row = [line[1], product_desc]
            # data_desc.append(row)
            rows_images[12]=product_desc

    # append to images table
    data_images.append(rows_images)
            
    driver.quit()
    # insert to DB
    
    # insert images
    df = pd.DataFrame(data_images,columns=['name','images1','images2','images3','images4','images5','weight','category','min_purchase','success_rate','rating_number','product_views','product_desc'])
    df.to_sql('heylookofficial_images', conn, if_exists=SQLMODE, index = False)
    
    #insert variant
    df = pd.DataFrame(data_variant,columns=['name','images'])
    df.to_sql('heylookofficial_variant', conn, if_exists=SQLMODE, index = False)
    
    data_images.clear()
    data_variant.clear()
    time.sleep(2)
