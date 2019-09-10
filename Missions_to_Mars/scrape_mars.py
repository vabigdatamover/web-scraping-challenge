# -*- coding: utf-8 -*-
"""
Created on 2019
Author: GB
"""

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
#import pymongo

# Setup connection to mongodb
#conn = "mongodb://localhost:27017"
#client = pymongo.MongoClient(conn)

# Select database and collection to use
#db = client.mars_data
#collection = db.mars_data

def init_browser():
   # @NOTE: Path to my chromedriver
   executable_path = {"executable_path": 'chromedriver.exe'}
   return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser=init_browser()
    mars_dict = {}
    
    #executable_path = {'executable_path': 'chromedriver.exe'}
    #browser = Browser('chrome', **executable_path, headless=False)
    
    """
    NASA Mars News
    """

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title =  soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
   
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

    # Loop through latest tweets and find the tweet that has weather information
    for tweet in tweet_text_container: 
        mars_weather = tweet.find('p').text
        if 'sol' and 'pressure' in mars_weather:
            #print(mars_weather)
            break
        else: 
            pass
    
    """
    Mars Fact
    """
    url3 = 'http://space-facts.com/mars/'
    browser.visit(url3)
    time.sleep(1)

    tables = pd.read_html(url3)
    df = tables[0]
    df.columns = ["Parameter", "Mars", "Earth"]
    df.set_index('Parameter', inplace=True)
    
    #mars_fact_dict = {"mars_fact":df.to_html()}
    mars_fact_dict = df.to_html()
    #mars_dict.update(mars_fact_dict)
    #mars_dict.update(mars_fact)=mars_fact_dict


    """
    Mars Fact
    """
    # Visit the following URL
    url = r"https://space-facts.com/mars/"
    browser.visit(url)
    tables = pd.read_html(url)
    df = tables[1]
    df.columns = ['Fact', 'Value']
    df.set_index("Fact", inplace=True)
   
    html_table = df.to_html(table_id='scrape_table')
    #html_table = str(html_table)
   
    """
    Mars Hemispheres
    """
    url = "https://astrogeology.usgs.gov/maps/mars-viking-hemisphere-point-perspectives"    
    browser.visit(url)
    time.sleep(2)    
    
    img_list =[]
    img_url_list = []
    title_list = []
    hemi=2
    count=1
    x=0
    kiki=[]

#    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    url = "https://astrogeology.usgs.gov/maps/mars-viking-hemisphere-point-perspectives"    
#    xpath = ('//*[@id="product-section"]/div[2]/div[' + str(hemi) +']/div/a/h3')
    xpath = ('//*[@id="publish"]/div[1]/div[1]/div[4]/div/a[' + str(hemi) +']/div/h3')    
#              //*[@id="publish"]/div[1]/div[1]/div[4]/div/a[4]/div/h3
#              //*[@id="publish"]/div[1]/div[1]/div[4]/div/a[6]/div/h3
#              //*[@id="publish"]/div[1]/div[1]/div[4]/div/a[8]/div/h3
    while count < 5:
        browser.visit(url)

        hemi_name = browser.find_by_xpath(xpath).text
        title_list.append(hemi_name)
        results = browser.find_by_xpath(xpath)

        img = results[0]
        img.click()
        time.sleep(2)

        # Scrape page into Soup
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        img_desc = soup.find('div', id="wide-image")
        img_src = img_desc.find('div',class_='downloads')
        image = img_src.find('a')
        if image.has_attr('href'):
            target_img = image.attrs['href']
        img_url_list.append(target_img)

        hemi+=2
#        xpath = ('//*[@id="product-section"]/div[2]/div[' + str(hemi) +']/div/a/h3')
        xpath = ('//*[@id="publish"]/div[1]/div[1]/div[4]/div/a[' + str(hemi) +']/div/h3')  
        count+=1
        x+=1
    
    hemisphere_image_urls = []
    h=0
    for items in title_list:
        if h < 4:
            dict = {"title": title_list[h], "img_url": img_url_list[h]}
            hemisphere_image_urls.append(dict)
            h+=1
    
    
  # Store data in a dictionary
    mars_data = {
       "news_title": news_title,
       "news_p": news_p,
       "featured_image_url": featured_image_url,
       "mars_weather": mars_weather,
       "mars_fact": mars_fact_dict,
       "html_table":html_table,
       "hemisphere_image_urls":hemisphere_image_urls
   }

    browser.quit()
    
    return mars_data
