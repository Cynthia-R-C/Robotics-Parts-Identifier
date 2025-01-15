# This is mostly for REV, since we might be able to get the product names and serial numbers for GoBilda by mass-downloading the GoBuilda CAD files in Fusion and pasting their names
# into a spreadsheet. Then we could get the data from the spreadsheet (hopefully).

# Problem: not a single page can hold all the products, so for REV, will probably need to make a list of all possible URLS of all pages in the
# shop-all page cycling system, then loop through them

# So far this is experimentation and trying to apply it

import requests
from bs4 import BeautifulSoup
import selenium
import re


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

def make_url_format(strs):
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

def get_GoBilda_products():
    '''nothing --> list titles, list serial numbers
    Returns a list of product names and a list of product serial numbers of all products from GoBilda'''
    mainCategories = ["https://www.gobilda.com/structure",
                      "https://www.gobilda.com/motion",
                      "https://www.gobilda.com/electronics"
                      "https://www.gobilda.com/hardware",
                      "https://www.gobilda.com/kits",
                      "https://www.gobilda.com/merch"]
    url = "https://www.gobilda.com/structure"           # the URL I'm using to run tests right now
    
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
    subcategories = extract_content(page.find_all('li', class_='product'))       # Extracts list of strings of subcategory names in this category
    #print(subcategories)
    subcatSegments = make_url_format(subcategories)
    #print(subcatSegments)
    
    #for seg in subcatSegments:   # for each of the subcategory URL segments (get back to this later)
    exSubURL = "https://www.gobilda.com/channel"    # try to extract product name and serial number using this example first

# Testing REV
revTitles, revSerials = get_REV_products()
#print(revTitles)
#print(revSerials)

# Testing GoBilda
# bildaTitles, bildaSerials = 
get_GoBilda_products()
# print(bildaTitles)
# print(bildaSerials)