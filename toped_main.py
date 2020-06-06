from py import toped_scrap_main
import argparse



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=int)
    parser.add_argument("--module", type=str)

    args = parser.parse_args()

    db_file = "data/scrap.tokopedia.db"
    url = "https://www.tokopedia.com/{}"

    pages = args.pages
    table_name = args.module
    url = url.format(table_name)

    toped_scrap_main.scrap_main(url, pages, db_file, table_name)
    toped_scrap_main.scrap_detail(db_file, table_name)