"""
Module retrieves job information from indeed.com using Selenium and BeautifulSoup.
Returns a list of job information stores as dictionaries.
"""
from datetime import datetime
import time
import random
from selenium import webdriver
from bs4 import BeautifulSoup

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
    #add a space after the first word
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
    #check if the first and second words are the same
    words = joined_text.split()
    if words[0] == words[1] and len(words) >= 2:
        cleaned_text = ' '.join(words[1:])
    else:
        cleaned_text = ' '.join(words)
    return cleaned_text


def scrape_indeed_listings(job_listings, driver):
    """
    Function takes soup from BeautifulSoup and strips out the job title, company
    location, posted date, and link. It then gets the job description from the link.
    Inputs in the .find() functions are specific to indeed.com
    Args:
        job_listings (beautifulsoup): generated from soup.find_all() looking for a
        specific class
        driver (Chrome webdriver): Chrome webdriver from selenium
    Returns:
        listings (list): list of job info, each job is its own dictionary with the
        job attribute as a key and scraped detail as value
    """
    listings = []
    for job in job_listings:
        job_title = job.find("span", id=lambda x: x and
                                x.startswith('jobTitle')).text.strip()
        job_company = job.find(attrs={'data-testid':'company-name'}).text.strip()
        job_location = job.find(attrs={'data-testid':'text-location'}).text.strip()
        posted_date = clean_date(job.find(attrs={'data-testid':
                                                    'myJobsStateDate'}).text.strip())
        apply_link = 'https://indeed.com' + job.find("a", class_=lambda x: x
                                                and x.startswith('jcs-JobTitle'))["href"]
        # navigate to the job posting page to scrape job description
        driver.get(apply_link)
        # sleeping randomly
        time.sleep(random.choice(list(range(5, 11))))
        try:
            description_soup = BeautifulSoup(driver.page_source, "html.parser")
            job_description = description_soup.find("div", id='jobDescriptionText').text
            job_description = job_description.strip().replace('\n', '')
        # handle the AttributeError exception that may occur if the element is not found
        except AttributeError:
            job_description = None # job_description is None if not found
            print("AttributeError occurred while retrieving job description.")
        listings.append({"title": job_title,
                    "company": job_company,
                    "location": job_location,
                    "posted date": posted_date,
                    "link": apply_link,
                    "description": job_description,
                    "scraped date": str(datetime.now())})
    return listings

def indeed_job_listings(job_title_input, pages):
    """
    Function initializes the scraping process by going to the indeed.com search for the
    inputed job title and number of pages. It calls the scrape_indeed_listings function
    for the number of pages inputted and returns one list with all the job listings.
    Uses selenium and BeautifulSoup.
    Args:
        job_title_input (string): job title to search for
        pages (int): number of pages to scrape
    Returns:
        jobs (list): list of job details, each job is its own dictionary, generated
        from scrape_indeed_listings
    Exceptions:
        TypeError for inputs (if job_title_input is not string, if pages is not int)
    """
    if isinstance(job_title_input, str) is not True:
        raise TypeError("Job title input is not a string")
    if isinstance(pages, int) is not True:
        raise TypeError("Pages input is not an int")

    job_listings_per_page = 15
    jobs = []

    for i in range(pages):
        start_index = i * job_listings_per_page
        url = f"https://www.indeed.com/jobs?q={job_title_input}&l=United+States&start={start_index}"
        print(f"Scraping from this url: {url}")

        driver = webdriver.Chrome()
        driver.get(url)
        # scroll to the bottom of the page using JavaScript
        print(f"Scrolling to bottom of page {i+1}")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for a random amount of time before scrolling to the next page
        time.sleep(random.choice(list(range(3, 7))))
        # Scrape the job postings
        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_listings = soup.find_all("div", class_=lambda x: x and
                                    x.startswith('cardOutline tapItem dd-privacy-allow result job'))
        try:
            job_info = scrape_indeed_listings(job_listings, driver)
            # add data to the jobs list
            jobs = jobs + job_info
        # catch exception that occurs in the scraping process
        except Exception as exception:
            print(f"An error occurred while scraping jobs from Indeed: {str(exception)}")

    # close the Selenium web driver
    driver.quit()

    return jobs
