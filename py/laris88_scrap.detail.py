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
SQLMODE = "replace"
conn = sqlite3.connect('../data/scrap.laris88.db')
cur = conn.cursor()
# cur.execute("select a.href, a.name from laris88_master a left join laris88_images b on a.name=b.name where b.name is null order by cast(replace(replace(a.rating,'(',''),')','') as integer) limit 10")
cur.execute("select a.href, a.name from laris88_main a where a.option not in ('Stok Kosong','Preorder') order by a.ID")
reader = cur.fetchall()
data_images = []
data_variant = []
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome('chromedriver',options=chrome_options)
driver.implicitly_wait(30)
driver.maximize_window()

for line in reader:

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
        ee = driver.find_element_by_xpath('//div[@data-testid="PDPImageMain"]/div/div/img')
        src = ee.get_attribute("src")
        print(src)
        if src.startswith('data'):
            time.sleep(2)
            src = ee.get_attribute("src")
        product_image.append(src)
        if counting == 5:
            break
    time.sleep(2)
    rows_images = [None] * 14
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
    elem = driver.find_element_by_xpath('//p[@data-testid="PDPDetailWeightValue"]')
    print(elem.text)
    product_weight = elem.text
    rows_images[6]=product_weight

    # fetch category
    print("Fetch Category")
    elem = driver.find_element_by_xpath('//ol[@data-testid="lnkPDPDetailBreadcrumb"]/li[4]')
    product_cat = elem.text
    print(product_cat)
    rows_images[7]=product_cat

    print("Fetch Min Purchase")
    elem = driver.find_element_by_xpath('//div[@data-testid="quantityOrder"]/div/input')
    min_purchase = elem.get_attribute("value")
    print(min_purchase)
    rows_images[8]=min_purchase

    print("Fetch success_rate")
    elem = driver.find_element_by_xpath('//span[@data-testid="lblPDPDetailProductSuccessRate"]')
    success_rate = elem.text.split(" ")[1]
    print(success_rate)
    rows_images[9]=success_rate

    print("Fetch rating_number")
    elem = driver.find_element_by_xpath('//span[@data-testid="lblPDPDetailProductRatingNumber"]')
    rating_number = elem.text
    print(rating_number)
    rows_images[10]=rating_number

    print("Fetch product_views")
    elem = driver.find_element_by_xpath('//span[@data-testid="lblPDPDetailProductSeenCounter"]/b')
    product_views = elem.text.replace('x','')
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

    #fetch productid
    print("Fetch product_id")
    elem = driver.find_element_by_xpath('//meta[@name="branch:deeplink:$ios_deeplink_path"]')
    product_id = elem.get_attribute("content").split("/")[1]
    print(product_id)
    rows_images[12]=product_id
    
    #fetch description and weight must scroll down
    print("Fetch description")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    elem = driver.find_element_by_xpath('//p[@data-testid="lblPDPDeskripsiProduk"]')
    product_desc = elem.text
    print(elem.text)
    rows_images[13]=product_desc

    # append to images table
    data_images.append(rows_images)
            
driver.quit()
# insert to DB

# insert images
df = pd.DataFrame(data_images,columns=['name','images1','images2','images3','images4','images5','weight','category','min_purchase','success_rate','rating_number','product_views','product_id','product_desc'])
df.to_sql('laris88_detail', conn, if_exists=SQLMODE, index = False)

#insert variant
df = pd.DataFrame(data_variant,columns=['name','images'])
df.to_sql('laris88_variasi', conn, if_exists=SQLMODE, index = False)

data_images.clear()
data_variant.clear()
time.sleep(2)
