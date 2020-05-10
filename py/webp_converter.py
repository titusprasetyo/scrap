from PIL import Image
import requests
from io import BytesIO
import sqlite3

def convert(img,name):
    response = requests.get(img)
    im = Image.open(BytesIO(response.content)).convert('RGB')
    im.save('/Users/titusadiprasetyo/Dropbox/Small Victories/wind up palm tree/{}{}'.format(name,'.jpg'),'jpeg')

conn = sqlite3.connect('scrap.slalukstore.db')
cur = conn.cursor()
cur.execute('select * from SLALUKSTORE_IMAGES')
reader = cur.fetchall()
for row in reader:
    if row[1] is not None:
        if row[1].startswith('data') == False:
            filename = row[1].split("/")
            convert(row[1], filename[len(filename)-1])

    if row[2] is not None:
        if row[2].startswith('data') == False:
            filename = row[2].split("/")
            convert(row[2], filename[len(filename)-1])

    if row[3] is not None:
        if row[3].startswith('data') == False:
            filename = row[3].split("/")
            convert(row[3], filename[len(filename)-1])

    if row[4] is not None:
        if row[4].startswith('data') == False:
            filename = row[4].split("/")
            convert(row[4], filename[len(filename)-1])

    if row[5] is not None:
        if row[5].startswith('data') == False:
            filename = row[5].split("/")
            convert(row[5], filename[len(filename)-1])
