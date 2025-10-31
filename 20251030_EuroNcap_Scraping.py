# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 22:03:08 2025

@author: homin

Scrape website Euroncap.com
"""

'''Step 1: get the list of pages from sitemap
'''

import requests, time
from bs4 import BeautifulSoup
import pandas as pd

def fetch(url):
    r = requests.get(url, headers = HEADERS, timeout = 15)
    r.raise_for_status()
    return r.text

def getListURL(html):
    """

    Parameters
    ----------
    html : html object from ferch function, which is the outout of a requests
        DESCRIPTION.

    Returns
    -------
    item : tuple of information extracted from the html site
        DESCRIPTION.

    """
    # Create soup object
    soup = BeautifulSoup(html, "html.parser")
    # Extract links and Mod time
    item = []
    for q in soup.select("url"):
        print("---------.URL identification: ------------------")
        print(q)
        text = q.select_one("loc").get_text(strip=True)
        modTime = q.select_one("lastmod").get_text(strip = True)
        item.append({"url": text, "modTime":modTime})
    return item

# =============================================================================
# def safe_select_attr(soup, selector, attr=None, strip_flag=True):
#     """
#     Safely extract an attribute or text from the first element matching a CSS selector.
# 
#     Args:
#         soup (BeautifulSoup): Parsed HTML soup.
#         selector (str): CSS selector string.
#         attr (str or None): Attribute name (e.g. 'href', 'data-src') or 'text' for element text.
#         strip (bool): Whether to strip whitespace from text (default: True).
# 
#     Returns:
#         str or None: The extracted value, or None if not found.
#     """
#     tag = soup.select_one(selector)
#     if not tag:
#         return None
# 
#     if attr is None or attr.lower() == 'text':
#         return tag.get_text(strip=strip_flag)
#     else:
#         return tag.get(attr)
# 
# =============================================================================

def safe_select_attr(soup, selector, attr=None):
    tag = soup.select_one(selector)
    if not tag:
        return None
    if attr:  # if attribute name provided
        return tag.get(attr)
    return tag.get_text(strip=True)

def getCarInfo(html, nameList):
    # Create soup object
    soup = BeautifulSoup(html, "html.parser")
    # Extract links and Mod time
    item = {}
# =============================================================================
#     
#     # Get releasedate
#     #item["releasedate"] = soup.select_one("#releasedate").get_text(strip = True)
#     item["releasedate"] = safe_select_attr(soup, 'div#releasedate')
# 
#     # Get stars
# # =============================================================================
# #     img_tag = soup.find('div', class_='stars').find('img')
# #     # Get the value of 'data-src'
# #     item["stars"] = img_tag['data-src']
# # =============================================================================
#     item["stars"] = safe_select_attr(soup, 'div.stars img', 'data-src')
#     
#     # Get car-name
#     #item["car-name"] = soup.select_one("h1", class_='car-name').get_text(strip = True)   
#     item["car-name"] = safe_select_attr(soup, 'h1.car-name')   
# 
#     # Get car-class
#     #item["car-class"] = soup.find('a', class_='car-class').get_text(strip = True)   
#     item["car-class"] = safe_select_attr(soup, 'a.car-class')
#     
# =============================================================================
    for name in nameList:
        item[name["name"]] = safe_select_attr(soup, name["selector"], name["attribute"])

    return item


if __name__ == "__main__":
    startTime = time.time()  # Start timer
    # Define website link
    BASE = "https://www.euroncap.com"
    SITEMAP = "/sitemap"
    HEADERS = {"User-Agent":"MyScraperBot/0.1"}
    fullLink = BASE+SITEMAP
    # Fetching the website
    '''20251028_Get the list of url
    print("Fetching", fullLink)
    html = fetch(fullLink)
    # Write fetched text into file
    text_file = open("fetch.txt", "w")
    text_file.write(html)
    text_file.close()
    # Extract links from the sitemap
    listURL = getListURL(html)
    # write down to csv file
    df = pd.DataFrame(listURL)
    csv_filename = "listURLs.csv"
    df.to_csv(csv_filename, index = False)
    print("List contains ", df.shape[0], " lines.")
    print("Process time: ", time.time() - startTime, ' s')'''
    '''20251029_Read the csv file and continue'''
    csv_filename = "listURLs.csv"
    df = pd.read_csv(csv_filename, delimiter = ',')
    df_results = df[df["url"].str.contains('/results/')]
    #for urlLink in df["url"]:
    urlLink = df_results["url"].iloc[0]
    print("===================Fetching the link ", urlLink)
    html = fetch(urlLink)
    #print(html)
    # List of information to scrape
    toScrapeList = [{"name":"releasedate", "selector":"#releasedate", "attribute":None},
                {"name":"stars", "selector":"div.stars img", "attribute":'data-src'},
                {"name":"car-name", "selector":"h1.car-name", "attribute":None},
                {"name":"car-class", "selector":"a.car-class", "attribute":None},
                {"name":"linkPDFreport", "selector":"div.download-report a", "attribute":"href"},
                ]
    
#    carInfo = getCarInfo(html, toScrapeList)