from py import toped_scrap_main


db_file = "data/scrap.tokopedia.db"

pages = 7
table_name = "laris88_main"
url = "https://www.tokopedia.com/laris88"

# pages = 15
# table_name = "lbagstore_main"
# url = "https://www.tokopedia.com/lbagstore"

# pages = 5
# table_name = "heylookofficial_main"
# url = "https://www.tokopedia.com/heylookofficial"

# toped_scrap_main.scrap_main(url, pages, db_file, table_name)
toped_scrap_main.scrap_detail(db_file, table_name)