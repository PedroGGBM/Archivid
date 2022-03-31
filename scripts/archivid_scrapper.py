"""
https://www.tutorialspoint.com/python_web_scraping/python_web_scraping_dynamic_websites.htm
https://scrapingant.com/blog/scrape-dynamic-website-with-python
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import random as rd
import re
import requests
from utils import str_encode_img_web

def configure_chromedriver(cat):

    # Instantiate options
    opts = Options()
    
    # opts.add_argument(" — headless") # Uncomment if the headless version needed
    opts.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

    # Set the location of the webdriver
    chrome_driver = "C:\\bin\\chromedriver.exe"

    # Instantiate a webdriver
    driver = webdriver.Chrome(options= opts, executable_path= chrome_driver)

    # Load the HTML page
    driver.get(f"https://www.archilovers.com/projects?keywords={cat}")

    # Parse processed webpage with BeautifulSoup
    soup = BeautifulSoup(driver.page_source,'html.parser')
    return soup

def get_images_by_cat(category):
    soup = configure_chromedriver(category)
    img_tags = soup.find_all('img')

    urls = [img['src'] for img in img_tags if ".jpg" in img['src']]

    str_images=[]

    rd.shuffle(urls)

    for i, url in enumerate(urls):
                
        image_path = f'./tmp_downloads/scrapped_archivid_{i}.jpg'
        with open(image_path, 'wb') as f:
            #if 'http' not in url:
                ## sometimes an image source can be relative 
                ## if it is provide the base url which also happens 
                ## to be the site variable atm. 
                #url = '{}{}'.format(site, url)
            response = requests.get(url)
            # print(url)
            f.write(response.content)
            img_str = str_encode_img_web(response.content)

            str_images.append(img_str)
    
    return str_images

#print(soup.find(id="src").get_text())
def parse_and_save(amount_of_images, string_activated):
    
    list_of_imgs = []
    
    for categ in string_activated:
        img_b64_cat = get_images_by_cat(categ.lower())
        rd.shuffle(img_b64_cat)
        list_of_imgs.extend(img_b64_cat)
    
    rd.shuffle(list_of_imgs) # randomize images
    
    return list_of_imgs[:amount_of_images]

"""
def test():
    results=parse_and_save(3,"spa")
    print(len(results))
"""