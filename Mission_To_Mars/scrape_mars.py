from attr import Attribute
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def mars_news(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=2)

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    try:
        slide_element = news_soup.select_one('div.list_text')
        slide_element.find('div', class_='content_title')

        news_title = slide_element.find('div', class_='content_title').get_text()
        news_paragraph = slide_element.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    return news_title, news_paragraph


def featured_image(browser):
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    full_image_button = browser.find_by_tag('button')[1]
    full_image_button.click()

    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

    try:
        img_url = image_soup.find('img', class_='headerimage fade-in').get('src')

    except AttributeError:
        return None
    
    featured_img_url = f'https://spaceimages-mars.com/{img_url}'
    return featured_img_url

def Mars_df():
    try:
        Mars_df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None

    Mars_df.columns=["Properties", "Mars", "Earth"]
    Mars_df.set_index('Properties', inplace=True)

    return Mars_df.to_html

def hemisphere(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_img_url = []

    for item in range(4):
        browser.links.find_by_partial_text('Hemisphere')[item].click()
        html = browser.html
        h_soup = BeautifulSoup(html, 'html.parser')
        title = h_soup.find('h2', class_='title').text
        img_url = h_soup.find('li').a.get('href')
        hemisphere = {}
        hemisphere['title'] = title
        hemisphere['img_url'] = f'https://marshemispheres.com/{img_url}'
        hemisphere_img_url.append(hemisphere)
        browser.back()

    return hemisphere_img_url

def scrape():
    news_title, news_paragraph = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "mars_facts": Mars_df(),
        "hemisphere": hemisphere(browser),
        "timestamp": dt.datetime.now()
    }

    browser.quit()
    return data

if __name__ == "__main__":
    print(scrape())

