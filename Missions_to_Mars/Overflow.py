    """
    Mars Hemispheres
    """
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    hemisphere_image_urls = []
    
    hemis_titles = soup.find_all('h3')
    
    for i in range(len(hemis_titles)):
        
        hemis_title = hemis_titles[i].text
        
        hemis_images = browser.find_by_tag('h3')
        hemis_images[i].click()
        time.sleep(1)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        img_url = soup.find('img', class_='wide-image')['src']
        img_url = "https://astrogeology.usgs.gov" + img_url
        
        hemis_dict = {"title": hemis_title, "img_url":img_url}
        hemisphere_image_urls.append(hemis_dict)
                        
        browser.back()
    
    mars_hemispheres_dict = {"mars_hemispheres_dict":hemisphere_image_urls}
    
    return_dict.update(mars_hemispheres_dict)




        ##https://astrogeology.usgs.gov/maps/mars-viking-hemisphere-point-perspectives

    url4 = 'https://astrogeology.usgs.gov/maps/mars-viking-hemisphere-point-perspectives'
    browser.visit(url4)
    time.sleep(1)

    xpath=(//*[@id="publish"]/div[1]/div[1]/div[4]/div/a[2]/div/h3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    hemisphere_image_urls = []
    
    hemis_titles = soup.find_all('h3')
    
    for i in range(len(hemis_titles)):
        
        hemis_title = hemis_titles[i].text
        
        hemis_images = browser.find_by_tag('h3')
        hemis_images[i].click()
        time.sleep(1)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        img_url = soup.find('img', class_='wide-image')['src']
        img_url = "https://astrogeology.usgs.gov" + img_url
        
        hemis_dict = {"title": hemis_title, "img_url":img_url}
        hemisphere_image_urls.append(hemis_dict)
                        
        browser.back()
    
    mars_hemispheres_dict = {"mars_hemispheres_dict":hemisphere_image_urls}
    
    mars_dict.update(mars_hemispheres_dict)