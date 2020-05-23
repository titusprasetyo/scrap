import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd

data = []

with open('data/analisa_fashion_pria.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    # chrome_options.add_argument('headless')
    driver = webdriver.Chrome('chromedriver',options=chrome_options)
    driver.implicitly_wait(30)
    driver.maximize_window()

    
    for row in csv_reader:

        print("Fetch {}".format(row['link']))
        driver.get(row['link'])
        elems = driver.find_elements_by_xpath('//div[@data-testid="lstCL2ProductList"]/div/a')
        for x in range(len(elems)):
            if x < 10 and x > 4:
                link = elems[x].get_attribute('href')
                link = re.sub(r'\?\S+','',link)
                rows = [row['link'], link, link.split("/")[3]]
                data.append(rows)



    driver.quit()

df = pd.DataFrame(data,columns=['link_category','link_product', 'store'])
df.to_csv("data/analisa_fashion_pria_result.csv", index=False)