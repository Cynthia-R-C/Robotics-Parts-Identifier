# This is mostly for REV, since we might be able to get the product names and serial numbers for GoBilda by mass-downloading the GoBuilda CAD files in Fusion and pasting their names
# into a spreadsheet. Then we could get the data from the spreadsheet (hopefully).

# Problem: not a single page can hold all the products, so for REV, will probably need to make a list of all possible URLS of all pages in the
# shop-all page cycling system, then loop through them

# So far this is experimentation and trying to apply it

import requests
from bs4 import BeautifulSoup


# Making a GET request
r = requests.get('https://www.revrobotics.com/shop-all/')     # later extend to loop through all page URLs

# check status code for response received
# success code - 200
print(r)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')

s = soup.find('div', class_='entry-content')
content = soup.find_all('REV-21-2099')                          # test if a product from page 2 can be detected through HTML taken from page 1: answer = no

print(content)