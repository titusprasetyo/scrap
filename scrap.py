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
from bs4 import BeautifulSoup


# %%
r = requests.get('http://detik.com/')
arr = []


# %%
#print(r.text)
soup = BeautifulSoup(r.text, 'lxml')


# %%

for link in soup.find_all('a'):
    try:
        #print(link.get('href'))
        re = requests.get(link.get('href'))
        #soup = BeautifulSoup(re.text, 'lxml')
        arr.add(link.get('href'))
    except:
        print("ERROR")


# %%



# %%


