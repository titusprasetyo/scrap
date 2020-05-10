# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
# import os
# try:
# 	os.chdir(os.path.join(os.getcwd(), '../../../../var/folders/k8/2k6x2q_x2zv03nyl8n7spk700000gn/T'))
# 	print(os.getcwd())
# except:
# 	pass

# %%
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3


# %%
url = "https://www.detik.com"
response = requests.get(url)
conn = sqlite3.connect('scrap.news.db')


# %%
soup = BeautifulSoup(response.text, "lxml")
links = soup.find_all("a")
data = []


# %%
for link in links:
    data_label = link.get("data-label")
    data_text = link.text.replace("\n","")
    data_href = link.get("href")
    data_img = None
    if link.find("img") != None:
        data_img = link.find("img").get("title")
    if data_img == None:
        data_img = data_text
    row = [data_label,data_img,data_href]
    data.append(row)

df = pd.DataFrame(data,columns=['label','text','href'])
df.to_sql('DETIK', conn, if_exists='append', index = False)


# %%


