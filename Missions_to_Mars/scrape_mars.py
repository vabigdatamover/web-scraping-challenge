# -*- coding: utf-8 -*-
"""
Created on 2019
Author: GB
"""

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import pymongo

# Setup connection to mongodb
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Select database and collection to use
db = client.mars_data
collection = db.mars_data

def scrape():
    
    return_dict = {}
    
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    """
    NASA Mars News
    """

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title =  soup.find('div', class_='content_title').a.text
    news_p = soup.find('div', class_='article_teaser_body').text

    mars_news_dict = {"news_title":news_title, "news_p":news_p}
    
    return_dict.update(mars_news_dict)
    
    """
    JPL Mars Space Images - Featured Image
    """
    
    url1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url1)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    carousel_item =  soup.find('article', class_='carousel_item')
    style = carousel_item["style"]
    split_text = style.split("'")
    featured_image_url = 'https://www.jpl.nasa.gov' + split_text[1]
    
    featured_image_dict = {"featured_image_url":featured_image_url}
    
    return_dict.update(featured_image_dict)
    
    """
    Mars Weather
    """
    url2 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url2)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    tweet_text_container = soup.find('div', class_='js-tweet-text-container')
    mars_weather = tweet_text_container.p.text 
    
    mars_weather_dict = {"mars_weather":mars_weather}
    
    return_dict.update(mars_weather_dict)
    
    """
    Mars Fact
    """
    url3 = 'http://space-facts.com/mars/'
    browser.visit(url3)
    time.sleep(1)

    tables = pd.read_html(url3)
    df = tables[0]
    df.columns = ["description", "value"]
    df.set_index('description', inplace=True)
    
    mars_fact_dict = {"mars_fact":df.to_html()}
    return_dict.update(mars_fact_dict)
    
    """
    Mars Hemispheres
    """
  

    browser.quit()
    
    return return_dict
