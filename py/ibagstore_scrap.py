
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
pages.append('https://www.tokopedia.com/lbagstore/page/1?sort=8')
pages.append('https://www.tokopedia.com/lbagstore/page/2?sort=8')
pages.append('https://www.tokopedia.com/lbagstore/page/3?sort=8')
pages.append('https://www.tokopedia.com/lbagstore/page/4?sort=8')
pages.append('https://www.tokopedia.com/lbagstore/page/5?sort=8')
pages.append('https://www.tokopedia.com/lbagstore/page/6?sort=8')
pages.append('https://www.tokopedia.com/lbagstore/page/7?sort=8')
pages.append('https://www.tokopedia.com/lbagstore/page/8?sort=8')
pages.append('https://www.tokopedia.com/lbagstore/page/9?sort=8')
pages.append('https://www.tokopedia.com/lbagstore/page/10?sort=8')
pages.append('https://www.tokopedia.com/lbagstore/page/11?sort=8')
pages.append('https://www.tokopedia.com/lbagstore/page/12?sort=8')
pages.append('https://www.tokopedia.com/lbagstore/page/13?sort=8')
pages.append('https://www.tokopedia.com/lbagstore/page/14?sort=8')
pages.append('https://www.tokopedia.com/lbagstore/page/15?sort=8')

conn = sqlite3.connect('../data/scrap.lbagstore.db')
for page in pages:
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome('chromedriver',options=chrome_options)
    driver.implicitly_wait(30)
    driver.maximize_window()
    driver.get(page)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    data = []
    elems = driver.find_elements_by_xpath("//a")
    for elem in elems:

        data_test = elem.get_attribute("data-testid")
        if data_test == "lnkProductContainer":
            href = elem.get_attribute("href")
            product_name = elem.text
            product_name = product_name.replace('Produk Unggulan\n','')
            product_name = product_name.replace('Stok Kosong\n','')
            product_name = product_name.replace('\nGrosir','')
            products = product_name.split('\n')
            products.append(href)

            # full info
            if len(products) == 6:
                rows = products
            # no ratings with discount
            if len(products) == 5:
                rows = [products[0],products[1],products[2],products[3],None,products[4]]
            # no discount with rating
            if len(products) == 4:
                rows = [products[0],None,None,products[1],products[2],products[3]]
            if len(products) == 2:
                rows = [products[0],None,None,products[1],None,products[3]]
                                        
            data.append(rows)
            # break;
            
    # print(data)
    driver.quit()
    df = pd.DataFrame(data,columns=['name','disc_percent','price_bef_disc','price_sell','rating','href'])
    df.to_sql('LBAGSTORE_MASTER', conn, if_exists='append', index = True)
    # df.head(n=20)
    data.clear()
    time.sleep(2)

