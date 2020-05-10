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


# %%
#get all product
# pages = []
# data = []
# pages.append('https://www.tokopedia.com/laris88/page/1')
# pages.append('https://www.tokopedia.com/laris88/page/2')
# pages.append('https://www.tokopedia.com/laris88/page/3')
# pages.append('https://www.tokopedia.com/laris88/page/4')
# pages.append('https://www.tokopedia.com/laris88/page/5')
# pages.append('https://www.tokopedia.com/laris88/page/6')
# pages.append('https://www.tokopedia.com/laris88/page/7')

# conn = sqlite3.connect('scrap.laris88.db')
# for page in pages:
#     chrome_options = webdriver.ChromeOptions()
#     prefs = {"profile.default_content_setting_values.notifications" : 2}
#     chrome_options.add_experimental_option("prefs",prefs)
#     driver = webdriver.Chrome('chromedriver',options=chrome_options)
#     driver.implicitly_wait(30)
#     driver.maximize_window()
#     driver.get(page)
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(3)

#     elems = driver.find_elements_by_xpath("//a")
#     for elem in elems:

#         data_test = elem.get_attribute("data-testid")
#         if data_test == "lnkProductContainer":
#             href = elem.get_attribute("href")
#             product_name = elem.text
#             product_name = product_name.replace('Produk Unggulan\n','')
#             product_name = product_name.replace('Stok Kosong\n','')
#             products = product_name.split('\n')
#             row = [href,products[0],products[1]]
#             data.append(row)

#     driver.quit()
#     df = pd.DataFrame(data,columns=['href','name','price'])
#     df.to_sql('LARIS88_MASTER', conn, if_exists='append', index = False)
#     data.clear()
#     time.sleep(2)


# %%
#grab detail
conn = sqlite3.connect('scrap.laris88.db')
cur = conn.cursor()
cur.execute('select a.href, a.name from LARIS88_MASTER a left join LARIS88_IMAGES b on a.name=b.name where b.name is null limit 50')
reader = cur.fetchall()
data_images = []
data_weight = []
data_variant = []
data_desc = []
data_cat = []
for line in reader:
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    # chrome_options.add_argument("--headless")  
#     chrome_options.add_argument("--user-data-dir=/Users/titusadiprasetyo/Library/Application Support/Google/Chrome/Default") # change to profile path
#     chrome_options.add_argument('--profile-directory=Default')
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
    
    # fetch weight
    print("Fetch Weight")
    elems = driver.find_elements_by_xpath('//p[@data-testid="PDPDetailWeightValue"]')
    for elem in elems:
        data_test = elem.get_attribute("data-testid")
        if data_test == "PDPDetailWeightValue":
            print(elem.text)
            product_weight = elem.text
            row = [line[1], product_weight]
            data_weight.append(row)
            
    # fetch category
    print("Fetch Category")
    elems = driver.find_elements_by_xpath('//ol[@data-testid="lnkPDPDetailBreadcrumb"]')
    for elem in elems:
        data_test = elem.get_attribute("data-testid")
        if data_test == "lnkPDPDetailBreadcrumb":
            product_cat = elem.text.replace(line[1],'')
            print(product_cat)
            row = [line[1], product_cat]
            data_cat.append(row)
    
    #fetch description and weight
    print("Fetch description")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    elems = driver.find_elements_by_xpath('//p[@data-testid="lblPDPDeskripsiProduk"]')
    for elem in elems:
        data_test = elem.get_attribute("data-testid")
        if data_test == "lblPDPDeskripsiProduk":
            product_desc = elem.text
            print(elem.text)
            row = [line[1], product_desc]
            data_desc.append(row)
            
    driver.quit()
    # insert to DB
#     conn = sqlite3.connect('scrap.laris88.db')
    
    # insert images
    df = pd.DataFrame(data_images,columns=['name','images1','images2','images3','images4','images5'])
    df.to_sql('LARIS88_IMAGES', conn, if_exists='append', index = False)

    #insert weight
    df = pd.DataFrame(data_weight,columns=['name','images'])
    df.to_sql('LARIS88_WEIGHT', conn, if_exists='append', index = False)
    
    #insert description
    df = pd.DataFrame(data_desc,columns=['name','images'])
    df.to_sql('LARIS88_DESC', conn, if_exists='append', index = False)

    #insert variant
    df = pd.DataFrame(data_variant,columns=['name','images'])
    df.to_sql('LARIS88_VARIANT', conn, if_exists='append', index = False)
    
    #insert category
    df = pd.DataFrame(data_cat,columns=['name','images'])
    df.to_sql('LARIS88_CATEGORY', conn, if_exists='append', index = False)
    
    data_images.clear()
    data_weight.clear()
    data_variant.clear()
    data_desc.clear()
    data_cat.clear()
    time.sleep(2)


# %%


