from datetime import datetime
import time
import random
import math
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# enable headless mode
options = Options()
options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')

def clean_date(text):
    """
    Function cleans the date text retrieved from indeed.com. Adds space between
    first two words and removes repeated words.
    Args:
        text (string): posting date text scraped from indeed.com posting
    Returns:
        cleaned_text (string): posting date with clean formatting
    """
    if isinstance(text, str) is not True:
        raise TypeError("Date input is not a string")
    characters = []
    upper_count = 0
    # add a space after the first word
    for char in text:
        if char.isupper():
            upper_count += 1
            if upper_count == 2:
                characters.append(' '+char)
            else:
                characters.append(char)
        else:
            characters.append(char)
    joined_text = ''.join(characters)
    # check if the first and second words are the same
    words = joined_text.split()
    if words[0] == words[1] and len(words) >= 2:
        cleaned_text = ' '.join(words[1:])
    else:
        cleaned_text = ' '.join(words)
    return cleaned_text

def calculate_pages(target_job_count):
    """
    Function calculates the number of pages to scrape based off the target job count
    and specified number of listings per page.
    Args:
        target_job_count (int): number of jobs to scrape
    Returns:
        (pages, job_listings_per_page) (tuple): tuple with number of pages (int)
        and specified job_listings_per_page (int)
    Exceptions:
        TypeError if target_job_count is not int
    """
    if isinstance(target_job_count, int) is not True:
        raise TypeError("Target job count input is not an int")
    job_listings_per_page = 15
    pages = math.ceil(target_job_count/job_listings_per_page)
    return (pages, job_listings_per_page)