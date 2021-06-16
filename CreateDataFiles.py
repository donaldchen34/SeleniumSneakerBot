import csv
import os.path
import json
import FilePaths

SITES_FILE = "files/sites.json"
ITEMS_FILE = "files/items.csv" #(Name,amount to buy)
STATS_FILE = "files/stats.csv"

SITES_FIELDS = ["site","link"]
ITEM_FIELDS = ["name","amount_to_buy"]
STAT_FIELDS = ["name","cost","amount","total_spent","date_purchased"]

#Create more files:
#accounts.json
#proxy.json
#task.json
#Log.csv

def createFiles():
    if not os.path.isfile(FilePaths.ITEMS_FILE):
        with open(FilePaths.ITEMS_FILE, 'w', newline='') as outfile:
            csv.writer(outfile).writerow(ITEM_FIELDS)
            outfile.close()

    if not os.path.isfile(FilePaths.STATS_FILE):
        with open(FilePaths.STATS_FILE, 'w', newline='') as outfile:
            csv.writer(outfile).writerow(STAT_FIELDS)
            outfile.close()

    #Don't need will be given in github
    if not os.path.isfile(FilePaths.SITES_FILE):
        with open(FilePaths.SITES_FILE, 'w', newline='') as outfile:
            sites = {
                    }
            """
            "footsites": {},
             "shopify" : {},
             "supreme" : "",
             "yeezysupply": "",
             "adidas" : "",
             "nike" : ""
             """
            json.dump(sites, outfile, indent=4)
            outfile.close()

    if not os.path.isfile(FilePaths.ACCOUNTS_FILE):
        with open(FilePaths.ACCOUNTS_FILE, 'w', newline = '') as outfile:
            json.dump('{}',outfile,indent = 4)
            outfile.close()


#Move to ReadData.py/ Will manually add sites
def addWebiste(website,link):
    with open(SITES_FILE,'r') as file:
        json_data = json.load(file)
        json_data[website] = link
        file.close()

    with open(SITES_FILE,'w') as file:
        json.dump(json_data,file,indent=4)

if __name__ == '__main__':
    createFiles()
    print("Files created")
    #<product_num>
    #site = "eastbay"
    #link = "https://www.eastbay.com/product/~/<product_num>.html"
    #addWebiste(site,link)