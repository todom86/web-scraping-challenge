import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Get newest title and paragraph
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'lxml')

    news_title = soup.select('div.content_title a')[0].text
    news_p = soup.select('div.article_teaser_body')[0].text

    # Get featured image
    url = 'https://www.jpl.nasa.gov'
    scrape_url = '/spaceimages/?search=&category=Mars'
    browser.visit(url + scrape_url)

    html = browser.html
    soup = bs(html, 'lxml')

    featured_title = soup.select('h1.media_feature_title')[0].text

    browser.links.find_by_partial_text('FULL IMAGE').click()

    html = browser.html
    soup = bs(browser.html, 'lxml')

    try:
        featured_image = soup.select('div img.fancybox-image')[0]['src']
        featured_image_url = url + featured_image
        
    except:
        
        browser.visit(url + scrape_url)

        html = browser.html
        soup = bs(html, 'lxml')

        featured_title = soup.select('h1.media_feature_title')[0].text

        browser.links.find_by_partial_text('FULL IMAGE').click()

        html = browser.html
        soup = bs(browser.html, 'lxml')
        
        featured_image = soup.select('div img.fancybox-image')[0]['src']
        featured_image_url = url + featured_image

    # Get Mars information
    mars_facts = pd.read_html('https://space-facts.com/mars/')[0].to_html(header=False,index=False)

    # Get hemisphere images
    url = "https://astrogeology.usgs.gov"
    scrape_url = "/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(url + scrape_url)

    links = browser.find_by_css("div.description a.itemLink")

    len(links)

    hemisphere_urls = []

    for x in range(len(links)):
        
        dict = {}
        
        browser.visit(url + scrape_url)
        browser.find_by_css("div.description a.itemLink")[x].click()
        
        html = browser.html
        soup = bs(html, 'lxml')
        
        dict['title'] = soup.select('h2.title')[0].text
        
        
        img = soup.select('div img.wide-image')[0]['src']
        dict['img_url'] = url + img
        
        hemisphere_urls.append(dict)

    mars_data = {
        "news_title" : news_title,
        "news_p" : news_p,
        "featured_image_url" : featured_image_url,
        "mars_facts" : mars_facts,
        "hemisphere_urls" : hemisphere_urls
    }
        
    browser.quit()

    return mars_data

    


