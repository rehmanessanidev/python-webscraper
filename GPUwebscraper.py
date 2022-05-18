#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 14 09:12:09 2022

@author: abdulrehmanessani

GPU Web Scraper 
"""

from bs4 import BeautifulSoup
import requests
import re

search_term = input("What GPU would you like to search for? ")

url = f"https://www.newegg.com/p/pl?d={search_term}&N=8000%204131"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

page_text = doc.find(class_="list-tool-pagination-text").strong
pages = int(str(page_text).split('/')[-2].split('>')[-1][:-1])

items_found = {}


for page in range(1, pages+1):
    url = f"https://www.newegg.com/p/pl?d={search_term}&N=8000%204131&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    
    
    
    items = div.find_all(text = re.compile(search_term))
    for item in items:
        parent = item.parent
        if parent.name != 'a':
            continue
            
        link = parent['href']
        next_parent = item.find_parent(class_='item-container')
        try:
            price = next_parent.find(class_="price-current").find('strong').string
            items_found[item]={'price': int(price.replace(',', '')), 'link': link}
        except:
            pass
        



sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])

for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])
    print("--------------------")
        
        