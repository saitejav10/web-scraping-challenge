from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

# Mars Dictionary
mars_info = {}

def mars_news():

        # Initialize browser 
        browser = init_browser()

        # Visit Nasa news url
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        time.sleep(1)

        # HTML Object
        html = browser.html
        soup = bs(html, "html.parser")

        # Retrieve news title and news_paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_paragraph = soup.find('div', class_='rollover_description_inner').text

        # Add to dictionary
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_paragraph

        browser.quit()

        return mars_info

# Mars Image
def mars_image():

        # Initialize browser 
        browser = init_browser()

        # Visit Mars Space Images
        image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url)

        # HTML Object 
        html_image = browser.html
        soup = bs(html_image, 'html.parser')

        # Retrieve background-image url
        background_url  = soup.find('article')['style']
        start = background_url.find("url('")
        end = background_url.find("');")
        url = background_url[start+len("url('"):end]

        # Concatenate
        featured_image_url = 'https://www.jpl.nasa.gov' + url

        # Add to dictionary
        mars_info['featured_image_url'] = featured_image_url 

        browser.quit()

        return mars_info

# Mars Weather 
def mars_weather():

        # Initialize browser 
        browser = init_browser()

        # Visit Mars Weather Twitter
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        # HTML Object 
        html_weather = browser.html
        soup = bs(html_weather, 'html.parser')

        # For loop all the tweets and display the first index
        mars_weathers=[]                                            
        for info in soup.find_all('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'):
            mars_weathers.append(info.text)  
        mars_weather = mars_weathers[0]

        # Add to dictionary
        mars_info['weather_tweet'] = mars_weather

        browser.quit()

        return mars_info

# Mars Facts
def mars_facts():

    # Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

    # Read Html and find the mars data
    mars_df = pd.read_html(facts_url)[0]

    # Assign the columns
    mars_df.columns = ['Description','Value']

    # Save html code
    final_data = mars_df.to_html()

    # Add to dictionary
    mars_info['mars_facts'] = final_data

    return mars_info

# Mars hemisphere
def mars_hemispheres():

    # Initialize browser 
    browser = init_browser()

    # Visit hemispheres website
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    # HTML Object
    html_hemispheres = browser.html
    soup = bs(html_hemispheres, 'html.parser')

    # Retreive mars hemispheres information
    all_items = soup.find_all('div', class_='item')
   
    hemispheres = []

    # For Loop
    for item in all_items: 
        
        # title
        title = item.find('h3').text

        # Image link
        link_url = item.find('a', class_='itemLink product-item')['href']
        browser.visit('https://astrogeology.usgs.gov'   + link_url)
            
        # HTML object once again to parse the link
        link_url_html = browser.html
        soup = bs(link_url_html, 'html.parser')
            
        # Full image source 
        final_image_url = 'https://astrogeology.usgs.gov'   + soup.find('img', class_='wide-image')['src']
            
        # Append
        hemispheres.append({"title" : title, 
                            "final_image_url" : final_image_url})

    # Add to dictionary
    mars_info['hemispheres'] = hemispheres

    browser.quit()

    return mars_info