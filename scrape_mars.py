#Dependencies
from bs4 import BeautifulSoup as bs
from lxml import html
import requests
import pandas as pd
from splinter import Browser
from selenium import webdriver
import time

url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

# Retrieve page with the requests module
response = requests.get(url)

soup = bs(response.text, 'html.parser')

# TitleTag = bs.find_all('div', class_="content_title")

results = soup.find('div', class_='features').text
#print(result)

# Print Title without tags
news_title=soup.title.text.strip()
news_title

# Extract all paragraph elements
soup.body.find_all('p')

# Print paragraph and remove tags
news_p=soup.p.text.strip()
news_p

# create path to find image
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

mars_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA19964_ip.jpg'
browser.visit(mars_image_url)

mars_image_html = browser.html
mars_image_soup = bs(mars_image_html, 'lxml')

# JPL Mars Space Image
# 'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA19964_ip.jpg
featured = mars_image_soup.find('div', class_='default floating_text_area ms-layer') 
featured_image = featured.find('footer')
featured_image_url = 'https://www.jpl.nasa.gov'+ featured_image.find('a')['button fancybox']
# browser.visit(featured_image_url)
featured_image_url

# Scrape Mars Twitter account for latest info on the weather in Mars
mars_twitter_url = 'https://twitter.com/marswxreport?lang=en'

mars_twitter_response = requests.get(mars_twitter_url)

mars_twitter_soup = bs(mars_twitter_response.text, 'html.parser')

mars_twitter_result = mars_twitter_soup.find('div', class_='js-tweet-text-container')
print(mars_twitter_result)

# Visit the Mars Facts webpage

mars_twitter_result = mars_twitter_soup.find('div', class_='tweet-js-stream-tweet')
tweet_container = mars_twitter_soup.find('ol', class_='stream-items js-navigable-stream')
tweet_container.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

# for tweet in soup.find_all('li'):
#     print(tweet)

mars_weather = mars_twitter_result.find_all('span', class_="username u-dir u-textTruncate")
# mars_twitter_url.format(row['prefix_1'], year, row['prefix_2'])

# Scrape facts about Mars (Diameter, etc.)
mars_facts_url = 'https://space-facts.com/mars/'
facts = pd.read_html(mars_facts_url)
facts

# Create Pandas DataFrame
facts_df = facts[0]
facts_df.columns = ['Diameter Description', 'Value']
facts_df.head()


#Scrape DataFrame to HTML table string
mars_facts = facts_df.to_html()
mars_facts.replace("\n", '')
facts_df.to_html('Mars_Facts.html')

#Use Dependencies to visit the astrogeology website
Astrogeology_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(Astrogeology_url)

# Set up scraping of astrogeology site using beautiful soup
Astrogeology_html = browser.html
Astrogeology_soup = bs(Astrogeology_html, 'lxml')
base_url = 'https://astrogeology.usgs.gov'


hemisphere_images = Astrogeology_soup.find_all('div', class_='downloads')

hemisphere_image_urls = []

for image in hemisphere_images:
    hemisphere_data = {}
    
    href = image.find('a', class_='itemLink product-item')
    link = base_url + href['href']
    browser.visit(link)
    
    time.sleep(1)
    
    Astrogeology_html2 = broswer.html
    Astrogeology_soup2 = bs(Astrogeology_html2, 'lxml')
    
    img_url = Astrogeology_soup2.find('div', class_='downloads').find('a')['href']
    Astrogeology_data['url_img'] = img_url
    
    img_title = Astrogeology_soup2.find('div', class_='content').find('h2', class_='title').text
    Astrogeology_data['title'] = img_title


    # Append dictionary to list
    hemisphere_image_urls.append(Astrogeology_data)
    
hemisphere_image_urls