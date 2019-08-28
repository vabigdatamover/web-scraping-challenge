from splinter import Browser
from bs4 import BeautifulSoup

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'c:\\Users\\EasyE\\Desktop\chromedriver'}
    
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    listings = {}
    #url = "https://washingtondc.craigslist.org/search/hhh?max_price=1500&availabilityMode=0"
    url="https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    listings["title"] = soup.find("a", class_="_self").get_text()
    listings["news"] = soup.find("span", class_="article_teaser_body").get_text()
    listings["hood"] = soup.find("span", class_="result-hood").get_text()
    # Close the browser after scraping
    browser.quit()
    
    return listings