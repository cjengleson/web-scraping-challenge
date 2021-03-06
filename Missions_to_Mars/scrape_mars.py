#!/usr/bin/env python
# coding: utf-8

# In[14]:


# import dependencies
import os
import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pymongo
import time
from pprint import pprint
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    #######################################
    # NASA Mars News
    #######################################

    # Scrape the Mars News Site and collect the latest News Title and Paragraph Text.

    # Assign the text to variables that you can reference later.

    # In[15]:

    # setup splinter and connect to site
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    url = "https://redplanetscience.com"
    browser.visit(url)
    html = browser.html

    # In[16]:

    # create bs object and parse html
    soup = bs(html, "html.parser")

    # In[17]:

    # scrape first news title & paragraph
    title = soup.find_all("div", class_="content_title")
    title = title[0].text

    paragraph = soup.find_all("div", class_="article_teaser_body")
    paragraph = paragraph[0].text

    print(title)
    print("--------------------------------------------")
    print(paragraph)

    browser.quit()

    #######################################
    # JPL Mars Space Images - Featured Image
    #######################################

    # Visit the url for the Featured Space Image site at https://spaceimages-mars.com/.

    # Use splinter to navigate the site and find the image url for the current
    # Featured Mars Image and assign the url string to a variable called featured_image_url.

    # Make sure to find the image url to the full size .jpg image.

    # Make sure to save a complete url string for this image.

    # In[18]:

    # setup splinter and connect to site
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    jpl_url = "https://spaceimages-mars.com/"
    browser.visit(jpl_url)
    jpl_html = browser.html

    # In[19]:

    # create bs object and parse html
    jpl_soup = bs(jpl_html, "html.parser")

    # In[20]:

    # find image url and assign to variable
    images = jpl_soup.find_all("img", class_="headerimage fade-in")
    for image in images:
        featured_image_url = (image["src"])

    featured_image_url = "https://spaceimages-mars.com/" + featured_image_url
    print(featured_image_url)

    browser.quit()

    #######################################
    # Mars Facts
    #######################################

    # Visit the Mars Facts webpage at https://galaxyfacts-mars.com/ and use
    # Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

    # Use Pandas to convert the data to a HTML table string.

    # In[21]:

    # set url
    facts_url = "https://galaxyfacts-mars.com/"

    # read tables
    tables = pd.read_html(facts_url)

    # convert table to df
    table_df = pd.DataFrame(tables[1])
    table_df.columns = ["Characteristic", "Value"]
    table_df

    # In[22]:

    # convert df to html table string
    html_table = table_df.to_html()
    html_table

    #######################################
    # Mars Hemispheres
    #######################################

    # Visit the astrogeology site at https://marshemispheres.com/ to obtain
    # high resolution images for each of Mar's hemispheres.

    # You will need to click each of the links to the hemispheres
    # in order to find the image url to the full resolution image.

    # Save both the image url string for the full resolution hemisphere image,
    # and the Hemisphere title containing the hemisphere name.

    # Use a Python dictionary to store the data using the keys img_url and title.

    # Append the dictionary with the image url string and the hemisphere title to a list.
    # This list will contain one dictionary for each hemisphere.

    # In[23]:

    # setup splinter and connect to site
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    url = "https://marshemispheres.com/"
    browser.visit(url)

    # In[24]:

    # set up lists
    hemispheres = ["Cerberus", "Schiaparelli",
                   "Syrtis Major", "Valles Marineris"]
    hemisphere_entries = []

    for hemi in hemispheres:

        # click into individual link
        browser.links.find_by_partial_text(
            hemi + " Hemisphere Enhanced").click()

        # create bs object
        html = browser.html
        soup = bs(html, "html.parser")

        # find image url
        li = soup.find_all("li")
        a = li[0].find("a")
        image_url = url+a["href"]

        # add image url to dictionary
        hemisphere_entries.append(
            {"title": hemi + " Hemisphere Enhanced", "img_url": image_url})

        # click back button
        browser.links.find_by_partial_text("Back").click()

    browser.quit()

    # In[25]:

    # view scraped hemisphere entries
    hemisphere_entries

    # In[26]:

    hemisphere_image_urls = hemisphere_entries
    hemisphere_image_urls

    # In[27]:

    mars_dictionary = {
        "article_title": title,
        "article_paragraph": paragraph,
        "featured_image_url": featured_image_url,
        "fact_table": html_table,
        "cerberus_title": hemisphere_image_urls[0]["title"],
        "cerberus_image": hemisphere_image_urls[0]["img_url"],
        "schiaparelli_title": hemisphere_image_urls[1]["title"],
        "schiaparelli_image": hemisphere_image_urls[1]["img_url"],
        "syrtis_major_title": hemisphere_image_urls[2]["title"],
        "syrtis_major_image": hemisphere_image_urls[2]["img_url"],
        "valles_marineris_title": hemisphere_image_urls[3]["title"],
        "valles_marineris_image": hemisphere_image_urls[3]["img_url"]
    }

    # In[28]:

    return(mars_dictionary)

    # In[ ]:

# %%
