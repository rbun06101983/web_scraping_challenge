#Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser=init_browser()
    mars_dictionary={}

    #Scarping the Mars Nasa News Page
    #url of webpage that is going to be scraped
    url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    #pulling the data
    html=browser.html
    #creating BeautifulSoup object  parse with 'lxml'
    news_soup=BeautifulSoup(html, "html.parser")
    #Scraping for the latest news title and assigning to a variable news_title
    news_title=news_soup.find("li", class_="slide").find("div", class_="content_title").text
    #Scraping for the latest paragraph text and assigning to a variable news_p
    news_p=news_soup.find("li", class_="slide").find("div", class_="article_teaser_body").text

    #Scraping JPL Mars Space Images - Featured Image
    #url of webpage that is going to be scraped
    jpl_nasa_url="https://www.jpl.nasa.gov"
    images_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(images_url)
    #pulling the data
    html=browser.html
    #creating BeautifulSoup object  parse with 'lxml'
    images_soup=BeautifulSoup(html, "html.parser")
    #Retrieving the the featured image link
    relative_image_path=images_soup.find_all('img')[3]['src']
    featured_image_url=jpl_nasa_url + relative_image_path
    
    #Scraping Mars Fact
    #url of webpage that is going to be scraped
    facts_url="https://space-facts.com/mars/"
    browser.visit(facts_url)
    #scraping table containing facts
    table=pd.read_html(facts_url)
    #converting table to dataframe
    mars_facts_df=table[2]
    mars_facts_df.columns=["Description", "Value"]
    #Converting dataframe to html
    mars_html_table=mars_facts_df.to_html()
    #Replacing all the \n values'
    mars_html_table.replace("/n", "")

    #Scraping Mars Hemisphere
    #url of webpage that is going to be scraped
    usgs_url="https://astrogeology.usgs.gov"
    hemispheres_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    #pulling the data
    html=browser.html
    #creating BeautifulSoup object  parse with 'lxml'
    hemispheres_soup=BeautifulSoup(html, "html.parser")
    #Getting the Mars hemispheres product data
    all_mars=hemispheres_soup.find('div', class_='collapsible results')
    mars_hemispheres=all_mars.find_all('div', class_='item')

    hemispheres_image_urls=[]

    #iterate through each hemisphere
    for i in mars_hemispheres:
        #collect title
        hemisphere=i.find('div', class_='description')
        title=hemisphere.h3.text
        #collect image link by browsing hemisphere page
        hemisphere_link=hemisphere.a['href']
        browser.visit(usgs_url + hemisphere_link)
        image_html=browser.html
        image_soup=BeautifulSoup(image_html, "html.parser")
        image_link=image_soup.find('div', class_='downloads')
        image_url=image_link.find('li').a['href']
        #create dictionary to store title and url info
        image_dict={}
        image_dict['title']=title
        image_dict['img_url']=image_url
        hemispheres_image_urls.append(image_dict)
    
    #Mars
    mars_dictionary={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "fact_table":str(mars_html_table),
        "hemisphere_images":hemispheres_image_urls
    }   

    return mars_dictionary

