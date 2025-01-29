# This is mostly for REV, since we might be able to get the product names and serial numbers for GoBilda by mass-downloading the GoBuilda CAD files in Fusion and pasting their names
# into a spreadsheet. Then we could get the data from the spreadsheet (hopefully).

# Problem: not a single page can hold all the products, so for REV, will probably need to make a list of all possible URLS of all pages in the
# shop-all page cycling system, then loop through them

# So far this is experimentation and trying to apply it

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains


# Making functions to strip the result
#def remove_angle_brackets(str):
    # '''string str --> string newStr
    # Removes the angle brackets and the content enclosed in it from a string'''
    # newStr = ""
    # inBrackets = False
    # for i in range(len(str)):
    #     if str[i] != "<" and not inBrackets:
    #         newStr += str[i]
    #     elif str[i] == "<":   # if it has entered the brackets
    #         inBrackets = True
    #     elif str[i] == ">":   # if it has reached the closing brackets
    #         inBrackets = False
    #     else:                 # if it's just inside the brackets
    #         pass
    # return newStr               
#def strip_angle_brackets(strs):

# REV

def extract_content(things):
    '''HTML tag object list things --> string list newThings
    Extracts the text content of a list of HTML tag objects into a list of strings'''
    newThings = []
    for thing in things:
        newThings.append(thing.text.strip())     # .text gives the string content of the tag object; .strip() removes all the extra '\n' and whitespace in it
    return newThings
    # '''list of strings strs --> list of strings newStrs
    # Strips the things in angle brackets off the list of strings;
    # made for stripping serials out - may end up using for titles too'''
    # newStrs = []     # find_all gives a list of strings
    # for str in strs:
    #     newStrs.append(remove_angle_brackets(str))
    # return newStrs

def make_url_format(strs, stemURL):
    '''list of strings --> list of strings
    Reformats each string in the list into its URL format - used for get_GoBilda_products()'''
    newStrs = []
    for str in strs:
        strLow = str.lower()    # change to lowercase
        # change special characters to "-"
        if "&" in str:
            newStr = strLow.replace(" & ","-")
        elif " " in str:
            newStr = strLow.replace(" ","-")
        else:
            newStr = strLow
        newStr = stemURL + "/" + newStr    # add the STEM URL
        newStrs.append(newStr)
    return newStrs

def get_REV_products():
    '''nothing --> list titles, list serial numbers
    Returns a list of product names and a list of product serial numbers of all products from REV robotics'''
    
    # Set URL list
    urls = ['https://www.revrobotics.com/shop-all/?limit=100&mode=bo',
            'https://www.revrobotics.com/shop-all/?limit=100&page=2&mode=bo',
            'https://www.revrobotics.com/shop-all/?limit=100&page=3&mode=bo',
            'https://www.revrobotics.com/shop-all/?limit=100&page=4&mode=bo']

    # Now collect the data from REV
    titleList = []
    serialList = []

    for url in urls:
        # Making a GET request
        r = requests.get(url)     # later extend to loop through all page URLs

        # check status code for response received
        # success code - 200
        #print(r)

        # Parsing the HTML
        soup = BeautifulSoup(r.content, 'html.parser')

        # Get this info from inspecting the webpage
        page = soup.find('ul', class_='productGrid')          # ul class productGrid    
        #print(s)
        titles0 = page.find_all('h3', class_='card-title')       # h3 card-title
        serials0= page.find_all('div', class_="card-text card-text--sku")     # div card-text card-text--sku

        # Stripping out the serials
        serials = extract_content(serials0)
        serialList += serials

        # Stripping out the titles
        titles = extract_content(titles0)
        titleList += titles
        
    return titleList, serialList


# GoBilda

def get_next_GoBilda_URLs(currURL):
    '''String currURL --> list newURLs
    Returns a list of the URLs to the subcategories linked on the page'''
    newURLs = []
    
    r = requests.get(currURL)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # Get info from inspecting webpage
    grids = soup.find_all('ul', class_='productGrid')   # find all product grids
    for grid in grids:
        if get_grid_type(grid) != 'category':         # remove if it's not a category grid
            grids.remove(grid)
    
    # Get URL info
    for grid in grids:
        tags = grid.find_all('a')

        for tag in tags:
            newURLs.append(tag['href'])   # href attribute is where URLs are stored

    return newURLs

def get_grid_type(prodGrid):
    '''HTML object prodGrid --> String gridType
    Given an HTML object representing a product grid, returns the type
    of grid it is: either "category" or "product"'''
    sampleTag = prodGrid.find('a')   # only need to test this for 1 tag because categories and product are not in the same grid
    return sampleTag['data-card-type']
    
def get_GoBilda_prod_info(prodPageURL):
    '''String prodPageURL --> list productNames, list productSerials
    Given a page that may or may not contain products, returns a list of the
    names and serial numbers of the products on the page'''
    r = requests.get(prodPageURL)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    productNames = []
    productSerials = []
    
    # Case 1: product grid
    prodGrids = soup.find_all('ul', class_='productGrid')   # find the right section to comb through
    for prodGrid in prodGrids:
        if get_grid_type(prodGrid) == 'product':   # only do this if it is a grid of products
            tags1 = prodGrid.find_all('a')
            for tag in tags1:
                productNames.append(tag['title'])
                productSerials.append(tag['data-sku'])
            
    # Case 2: product table
    prodTables = soup.find_all('div', class_='tableParent')
    for prodTable in prodTables:
        tags2 = prodTable.find_all('a')
        for tag in tags2:
            productNames.append(tag['title'])
            sku = tag.text.strip()
            productSerials.append(sku)
    
    return productNames, productSerials

def next_GoBilda_URL(url):
    '''String url --> list productNames, list productSerials
    Runs a piece of a recursive function for extracting GoBilda data;
    For a certain url, retrieves product info for that URL and all corresponding 
    sub-URLs, then returns the information'''
    
    # Get product information
    productNames, productSerials = get_GoBilda_prod_info(url)
    
    # Get next URLs
    newURLs = get_next_GoBilda_URLs(url)
    
    # Check if there are no next URLs left on the page - if not then end recursion
    if len(newURLs) == 0:
        return productNames, productSerials
    
    # If there still are URLs to be run through
    for newURL in newURLs:
        # Get product information returned by this recursive function
        newProdNames, newProdSerials = next_GoBilda_URL(newURL)
        productNames += newProdNames
        productSerials += newProdSerials
    
    return productNames, productSerials

def get_GoBilda_products1():   # NOT DONE
    '''nothing --> list titles, list serial numbers
    Returns a list of product names and a list of product serial numbers of all products from GoBilda'''
    mainCategories = ["https://www.gobilda.com/structure",
                      "https://www.gobilda.com/motion",
                      "https://www.gobilda.com/electronics"
                      "https://www.gobilda.com/hardware"]
    #url = "https://www.gobilda.com/structure"           # the URL I'm using to run tests right now
    productNames = []                                   # list used to store the product names (including serial number)
    serials = []
    
    for url in mainCategories:
        newProdNames, newSerials = next_GoBilda_URL(url)
        productNames += newProdNames
        serials += newSerials
    
    print(productNames)
    print(serials)
    
    
def get_GoBilda_products2():
    '''nothing --> list titles, list serial numbers
    Returns a list of product names and a list of product serial numbers of all products from GoBilda'''
    
    # Initialize the driver using Service
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    # Set URLs
    categories = ["https://www.gobilda.com/structure",
                      "https://www.gobilda.com/motion",
                      "https://www.gobilda.com/electronics"
                      "https://www.gobilda.com/hardware",
                      "https://www.gobilda.com/kits",
                      "https://www.gobilda.com/merch"]
    url = "https://www.gobilda.com/structure"           # the URL I'm using to run tests right now
    driver.get(url)    # navigate to the  URL
    
    # Find subcategories
    subcats = driver.find_elements(By.CLASS_NAME, "product")
    
    # For each subcategory
    action = ActionChains(driver)
    action.click(on_element = subcats[0])  # navigate to a subcategory
    action.perform()
    
    # Find sub-subcategories
    sub2cats = driver.find_elements(By.CLASS_NAME, "product")
    #print(sub2cats)
    
    # For each sub-subcategory
    action2 = ActionChains(driver)
    action2.click(on_element = sub2cats[0])
    action2.perform()
    sub2URL = driver.current_url
    print(sub2URL)   # it's not navigating to the sub2cat, only stops at /channel
    
    driver.quit()

# Testing REV
revTitles, revSerials = get_REV_products()
#print(revTitles)
#print(revSerials)

# Testing GoBilda
# bildaTitles, bildaSerials = 
get_GoBilda_products1()
# print(bildaTitles)
# print(bildaSerials)