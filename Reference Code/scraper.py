#TODO: TOR, FIND A WAY TO GET ALL WEBSITES? KEYWORDS? KEY TAGS? AND MAX MONEY

from fake_useragent import UserAgent
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import time
from bs4 import BeautifulSoup as bs

agent = UserAgent()

opts = Options()

opts.add_argument("user-agent=" + agent.random)
#doesn't open chrome, headless
opts.add_argument("--headless")

driver = webdriver.Chrome(options=opts)

keep = True

website = []

urls = {}

inputbool = True
#get cards from user
while inputbool:
    name = input("Enter another website name or type E if you are finished: \n").lower()

    if name == 'e':
        inputbool = False
        break
    elif  name == "newegg" or name == "bestbuy":
        website.append(name)

        gpu = input("Enter GPU Name: \n")

        url = input("Enter URL: \n")

        urls[gpu] = url
    else:
        print("Not Valid in Current Code, edit Source?")


#convert the keys to a list in order for ease of checking both website and url from a range
keys_list = list(urls.keys())

chrome = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

rangevar = len(website)

print("Started")
if rangevar == 0:
    print("and.... Finished :p")
    sys.exit()

while keep:
    for i in range(rangevar):
        print(f"Currently Searching For: {keys_list[i]}")

        driver.get(urls[keys_list[i]])

        html = driver.page_source

        doc = bs(html, "html.parser")

        if website[i] == "bestbuy":
            soldout_tag = doc.find(string="Sold Out")

            soldout = soldout_tag.text if soldout_tag else None
        else:
            soldout_tag = doc.find(string="OUT OF STOCK ")

            soldout = soldout_tag.text if soldout_tag else None
        #check to see if CAPTCHA
        title_tag = doc.find('title')

        title = title_tag.text.lower() if title_tag else None

        title_split = title.split()

        if "captcha" in title_split:
            print("EEK CAPTCHA! CAUGHT! EXITING!! MAYDAY MAYDAY!!!")
            sys.exit()

        if not soldout:
            print(f"FOUND GPU: {keys_list[i]} at {urls[keys_list[i]]}")

            webbrowser.get(chrome).open(urls[keys_list[i]])

            stop = input(f"DID YOU GET IT? Press T in order to Terminate, or Continue going by pressing any other key\n")

            if stop == 'T':
                sys.exit()

        else:
            print("OUT OF STOCK")

    time.sleep(10)