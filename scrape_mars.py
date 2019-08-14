from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    
    url = 'https://mars.nasa.gov/news/'

    # browser.visit(url)
    time.sleep(1)

    # Retrieve page with the requests module
    news_response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    news_soup = bs(news_response.text, 'lxml')

    # Retrieve the parent divs for all news headlines
    news_results = news_soup.find_all('div', class_='slide')

    #create empty list to hold dictionary objects
    nasa_headlines=[]
    
    # Loop through results to retrieve headline and paragraph
    for result in news_results:
        news_title = result.find('div', class_='content_title').text.replace('\n','')

        news_p = result.find('div', class_='rollover_description_inner').text.replace('\n','')
        
        
        # create dictionaries and append to list
        post = {
            'news_title': news_title,
            'news_p': news_p
        }
        
        nasa_headlines.append(post)
    
    #assign nasa headline data to dictionary
    mars_data = nasa_headlines[0]
    
    # image url for featured image
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA00063-1920x1200.jpg'
    image_dict = {'featured_image': featured_image_url}

    # assign image into mars_data dictionary
    mars_data.update(image_dict)

    # scrape mars weather from twitter
    # URL of page to be scraped
    weather_url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    weather_response = requests.get(weather_url)
    # Create BeautifulSoup object; parse with 'lxml parser'
    weather_soup = bs(weather_response.text, 'lxml')

    weather_results = weather_soup.find_all('div',class_='js-tweet-text-container')

    #declare empty list to hold weather tweets
    mars_weather_tweets = []
    for result in weather_results:
        tweet = result.text.replace('\n','')
        mars_weather_tweets.append(tweet)
    
    
    mars_weather = {'mars_weather':mars_weather_tweets[0]}

    # append mars_weather to end of mars_data dictionary
    mars_data.update(mars_weather)

    
    # scrape mars facts 
    facts_url = 'https://space-facts.com/mars/'

    tables = pd.read_html(facts_url)
    factDF = tables[0]
    html_table = factDF.to_html()
    mars_facts = {'mars_facts':html_table}

    # pass html table into mars_data
    mars_data.update(mars_facts)

    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
    {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
    ]

    # # append hemisphere images to mars_data dictionary
    # mars_data.update(hemisphere_image_urls[0])
    # mars_data.update(hemisphere_image_urls[1])
    # mars_data.update(hemisphere_image_urls[2])
    # mars_data.update(hemisphere_image_urls[3])
    mars_data.update({'hemisphere':hemisphere_image_urls})

    

    # Return results
    return mars_data