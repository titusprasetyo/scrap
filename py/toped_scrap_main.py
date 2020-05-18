
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time
import sqlite3
import re


def scrap_main(url, pages, db_file, table_name):

    data = []

    conn = sqlite3.connect(db_file)
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome('chromedriver',options=chrome_options)
    driver.implicitly_wait(30)
    driver.maximize_window()
    data = []
    for page in range(1, pages+1):
        full_url = url+"/page/{}?sort=8".format(page)
        print("Fetch {}".format(full_url))
        driver.get(full_url)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        
        elems = driver.find_elements_by_xpath('//a[@data-testid="lnkProductContainer"]')
        for elem in elems:

            href = elem.get_attribute("href")
            product_name = elem.text
            option = ""
            if "Produk Unggulan" in product_name:
                option = "Produk Unggulan"
                if page != 1:
                    continue
            elif "Stok Kosong" in product_name:
                option = "Stok Kosong"
            elif "Grosir" in product_name:
                option = "Grosir"
            elif "Preorder" in product_name:
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
    df.to_sql(table_name, conn, if_exists='replace', index = True, index_label="ID")
    # df.head(n=20)
    data.clear()
    time.sleep(2)
    driver.quit()

def scrap_detail(db_file, table_name):

    #grab detail
    SQLMODE = "replace"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("select a.href, a.name from {} a where a.option not in ('Stok Kosong','Preorder') order by a.ID".format(table_name))
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
        elems = driver.find_elements_by_xpath('//ol[@data-testid="lnkPDPDetailBreadcrumb"]/li')
        product_cat = ""
        for elem in range(len(elems)):
            if elem != len(elems)-1:
                product_cat = product_cat + "#" + elems[elem].text
        product_cat = product_cat + "#"
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
        product_desc = re.sub(r'http\S+', '', product_desc)
        print(product_desc)
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
