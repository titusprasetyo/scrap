
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time
import sqlite3



#get all product
pages = []
data = []
pages.append('https://www.tokopedia.com/laris88/page/1?sort=8')
pages.append('https://www.tokopedia.com/laris88/page/2?sort=8')
pages.append('https://www.tokopedia.com/laris88/page/3?sort=8')
pages.append('https://www.tokopedia.com/laris88/page/4?sort=8')
pages.append('https://www.tokopedia.com/laris88/page/5?sort=8')
pages.append('https://www.tokopedia.com/laris88/page/6?sort=8')
pages.append('https://www.tokopedia.com/laris88/page/7?sort=8')

conn = sqlite3.connect('../data/scrap.laris88.db')
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome('chromedriver',options=chrome_options)
driver.implicitly_wait(30)
driver.maximize_window()
data = []
for page in pages:

    driver.get(page)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    
    elems = driver.find_elements_by_xpath("//a")
    for elem in elems:

        data_test = elem.get_attribute("data-testid")
        if data_test == "lnkProductContainer":
            href = elem.get_attribute("href")
            product_name = elem.text
            option = ""
            if "Produk Unggulan" in product_name:
                option = "Produk Unggulan"
            if "Stok Kosong" in product_name:
                option = "Stok Kosong"
            if "Grosir" in product_name:
                option = "Grosir"
            if "Preorder" in product_name:
                option = "Preorder"
            product_name = product_name.replace('Produk Unggulan\n','')
            product_name = product_name.replace('Stok Kosong\n','')
            product_name = product_name.replace('\nGrosir','')
            product_name = product_name.replace('\nPreorder','')
            products = product_name.split('\n')
            products.append(href)

            # full info
            if len(products) == 6:
                rows = rows = [products[0],products[1],products[2],products[3],products[4],products[5], option]
            # no ratings with discount
            if len(products) == 5:
                rows = [products[0],products[1],products[2],products[3],None,products[4], option]
            # no discount with rating
            if len(products) == 4:
                rows = [products[0],None,None,products[1],products[2],products[3], option]
            if len(products) == 2:
                rows = [products[0],None,None,products[1],None,products[3], option]
                                        
            data.append(rows)
            # break;
            
# print(data)
df = pd.DataFrame(data,columns=['name','disc_percent','price_bef_disc','price_sell','rating','href','option'])
df.to_sql('laris88_main', conn, if_exists='append', index = True, index_label="ID")
# df.head(n=20)
data.clear()
time.sleep(2)
driver.quit()
