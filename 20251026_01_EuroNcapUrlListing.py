# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# static_scraper.py
import requests, time
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

BASE = "https://quotes.toscrape.com"  # Use this demo site for practice
HEADERS = {"User-Agent":"MyScraperBot/0.1"}

def fetch(url):
    r = requests.get(url, headers = HEADERS, timeout = 15)
    r.raise_for_status()
    return r.text

def parse_quotes_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())
    items =[]
    for q in soup.select(".quote"):
        print("---------.quote identification: ------------------")
        print(q)
        text = q.select_one(".text").get_text(strip=True)
        print("*********.text identification: *******************")
        print(text)
        author = q.select_one(".author").get_text(strip=True)
        print("*********.author identification: *******************")
        print(author)
        tags= [t.get_text(strip = True) for t in q.select(".tags .tag")]
        items.append({"text": text, "author": author, "tags": ",".join(tags)})
    next_link = soup.select_one("li.next > a")
    return items, (urljoin(BASE, next_link["href"]) if next_link else None)

def scrape_all(start_url):
    url = start_url
    data = []
    while url:
        print("Fetching", url)
        html = fetch(url)
        items, url = parse_quotes_page(html)
        data.extend(items)
        time.sleep(1.2)  # Be polite
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = scrape_all(BASE)
    df.to_csv("quotes.csv", index = False)
    print ("Saved", len(df), "rows")