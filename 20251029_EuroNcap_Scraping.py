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

def getCarInfo(html, nameList):
    # Create soup object
    soup = BeautifulSoup(html, "html.parser")
    # Extract links and Mod time
    item = {}
    for name in nameList:
        print(name, '---------', soup.select_one(name))
        text = soup.select_one(name).get_text(strip = True)
        item[name] = text
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
    nameList = ["year", "stars", "car-name"]
    carInfo = getCarInfo(html, nameList)