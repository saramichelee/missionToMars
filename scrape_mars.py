from bs4 import BeautifulSoup
import requests
import pymongo
import time

from splinter import Browser

import pandas as pd

def init_browser:
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():

    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    db = client.m2mars_db
    collection = db.mars_news

    news_url = 'https://mars.nasa.gov/news/'
    response = requests.get(news_url)
    soup = BeautifulSoup(response.text, 'lxml')

    title = soup.find('div', class_='content_title').find('a').text
    news_title = title.replace("\n","")

    paragraph = soup.find('div', class_='rollover_description_inner').text
    news_paragraph = paragraph.replace("\n","")

    browser = init_browser()

    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    browser.click_link_by_partial_text('FULL IMAGE')

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    full_image = soup.find('a', class_="button fancybox")['data-fancybox-href']
    featured_image_url = f'https://www.jpl.nasa.gov{full_image}'

    browser.quit()

    weather_url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(weather_url)
    soup = BeautifulSoup(response.text, 'lxml')

    tweets = soup.find_all('div', class_="js-tweet-text-container")

    notweather = []
    weathertweet = []

    for tweet in tweets:
        weather_tweet = tweet.find('p', class_="tweet-text").text
        check_tweet = weather_tweet.startswith('InSight')
        if check_tweet is False:
            notweather.append(weather_tweet)
        elif check_tweet is True:
            weathertweet.append(weather_tweet)
            break
    first_tweet = weathertweet[0]

    mars_weather = first_tweet.replace("\n"," ").replace("InSight sol","Sol")

    facts_url = 'https://space-facts.com/mars/'

    tables = pd.read_html(facts_url)

    facts_table = tables[1]

    fact_df = facts_table.rename(columns={0: "fact_type", 1: "information"})

    fact_dict = {}
    for x in range (0,9):
        into_dict = {fact_df['fact_type'][x]:fact_df['information'][x]}
        fact_dict.update(into_dict)

    html_table = fact_df.to_html()

    html_table = fact_df.to_html()

    updated_html = html_table.replace('\n', '')

    browser = init_browser()

    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemispheres = []

    desc = soup.find_all('div', class_="description")

    for x in desc:
        titles = x.find('a', class_="product-item").text
        hem_title = titles.replace(' Enhanced','')
        hemispheres.append(hem_title)
        
    hem_images = []

    for hemisphere in hemispheres:
        browser.visit(hem_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        browser.click_link_by_partial_text(hemisphere)
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        hem_img = soup.find('div', class_="downloads").find('a')['href']
        hem_images.append(hem_img)
        
    hemisphere_image_urls = []

    browser.quit()

    for x in range(0,4):
        dictn = {"title":hemispheres[x],"img_url":hem_images[x]}
        hemisphere_image_urls.append(dictn)

    mars_combined = {"news": {"title" : news_title, "paragraph": news_paragraph},
                    "featured_img": featured_image_url,
                    "current_weather": mars_weather,
                    "facts": fact_dict,
                    "hemispheres": hemisphere_image_urls}
    return mars_combined

# scrape()
