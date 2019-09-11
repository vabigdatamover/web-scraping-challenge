"""
Created 2019
Author: GB
"""

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time




def init_browser():
   # @NOTE: Path to my chromedriver in the homework folder
   executable_path = {"executable_path": 'chromedriver.exe'}
   return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser=init_browser()
     
    """
    NASA Mars News
    """
    #Mars News URL
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
    # Featured Space Image URL
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
    #Weather Tweets, includes loops to find tweets with weather info
    url2 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url2)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    tweet_text_container = soup.find_all('div', class_='js-tweet-text-container')
     
    print(tweet_text_container)
    # Loop through latest tweets and find the tweet that has weather information
    for tweet in tweet_text_container: 
        mars_weather = tweet.find('p').text
        if 'sol' and 'pressure' in mars_weather:
            #print(mars_weather)
            break
        else: 
            pass
    
    """
    Mars Fact Alternate
    """
    #Mars facts URL with Earth and Mars comparison
    #url3 = 'http://space-facts.com/mars/'
    #browser.visit(url3)
    #time.sleep(1)

    #tables = pd.read_html(url3)
    #df = tables[0]
    #df.columns = ["Parameter", "Mars", "Earth"]
    #df.set_index('Parameter', inplace=True)
    
    
    #mars_fact_dict = df.to_html()
    


    """
    Mars Fact
    """
    # Mars Facts URL
    url = r"https://space-facts.com/mars/"
    browser.visit(url)
    tables = pd.read_html(url)
    df = tables[1]
    df.columns = ['Fact', 'Value']
    df.set_index("Fact", inplace=True)
   
    html_table = df.to_html(table_id='scrape_table')
    
   
    """
    Mars Hemispheres
    """
    #Mars Hemispheres URL
    url = "https://astrogeology.usgs.gov/maps/mars-viking-hemisphere-point-perspectives"    
    browser.visit(url)
    time.sleep(2)    
    
    
    img_url_list = []
    title_list = []
    hemi=2
    count=1
    x=0
    

#    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    url = "https://astrogeology.usgs.gov/maps/mars-viking-hemisphere-point-perspectives"    
#    xpath = ('//*[@id="product-section"]/div[2]/div[' + str(hemi) +']/div/a/h3')
   #X Path into the Four Hemisphere Images
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
       #News Title
       "news_title": news_title,
       #News Title
       "news_p": news_p,
       #Featured Image
       "featured_image_url": featured_image_url,
       #Mars Weather
       "mars_weather": mars_weather,
       #Mars Facts
       "html_table":html_table,
       #Mars Four Hemispheres
       "hemisphere_image_urls":hemisphere_image_urls
   }

    browser.quit()
    
    return mars_data
