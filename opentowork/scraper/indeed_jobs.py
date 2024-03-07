# pylint: disable=broad-exception-caught
# disabled due to variability in scraping exceptions, no specific expected exception
"""
Module retrieves job information from indeed.com using Selenium and BeautifulSoup.
Returns a list of job information stores as dictionaries.
Functions:
    calculate_pages - calculates the number of pages needed for specific number of jobs
    clean_date - cleans scraped date
    scrape_indeed_listings - gathers job details from input generated with BeautifulSoup
    indeed_job_listings - searches inputted job title on indeed.com and calls scrape_indeed_listings
"""
from datetime import datetime
import time
import random
import math
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# enable headless mode
options = Options()
# options.add_argument("--headless")

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

def scrape_indeed_listings(job_listings, driver, valid_job_count, last_page, target_job_count):
    """
    Function takes soup from BeautifulSoup and strips out the job title, company
    location, posted date, and link. It then gets the job description from the link.
    Inputs in .find() are specific to indeed.com
    Args:
        job_listings (beautifulsoup): generated from soup.find_all() looking for a
        specific class
        driver (Chrome webdriver): Chrome webdriver from selenium
        valid_job_count (int): number of jobs with no None values
        last_page (boolean): indicator for last page
        target_job_count (int): targetted number of jobs to scrape
    Returns:
    in a tuple:
        listings (list): list of job info, each job is its own dictionary with the
        job attribute as a key and scraped detail as value
        valid_job_count (int): count of valid jobs scraped
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
        job_data = [job_title, job_company, job_location, posted_date, apply_link, job_description]
        if all(job_detail is not None for job_detail in job_data):
            listings.append({"title": job_title,
                        "company": job_company,
                        "location": job_location,
                        "posted date": posted_date,
                        "link": apply_link,
                        "description": job_description,
                        "scraped date": str(datetime.now())})
            valid_job_count += 1
        if last_page is True and valid_job_count >= target_job_count:
            break
    return (listings, valid_job_count)

def indeed_job_listings(job_title_input, target_job_count):
    """
    Function initializes the scraping process by going to the indeed.com search for the
    inputed job title and number of pages. It calls the scrape_indeed_listings function
    for the number of pages inputted and returns one list with all the job listings.
    Uses selenium and BeautifulSoup.
    Args:
        job_title_input (string): job title to search for
        target_job_count (int): number of jobs to get
    Returns:
        jobs (list): list of job details, each job is its own dictionary, generated
        from scrape_indeed_listings
    Exceptions:
        TypeError for inputs (if job_title_input is not string, if target_job_count is not int)
    """
    if isinstance(job_title_input, str) is not True:
        raise TypeError("Job title input is not a string")
    if isinstance(target_job_count, int) is not True:
        raise TypeError("Target job count input is not an int")

    pages = calculate_pages(target_job_count)
    jobs = []
    valid_job_count = 0
    last_page = False

    for i in range(pages[0]):
        if i == pages[0]-1:
            last_page = True
        start_index = i * pages[1]
        url = f"https://www.indeed.com/jobs?q={job_title_input}&l=United+States&start={start_index}"
        print(f"Scraping from this url: {url}")

        driver = webdriver.Chrome(options=options)
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
            results = scrape_indeed_listings(job_listings, driver, valid_job_count,
                                             last_page, target_job_count)
            # add data to the jobs list
            jobs = jobs + results[0]
            valid_job_count = results[1]
        # catch exception that occurs in the scraping process
        except Exception as exception:
            print(f"An error occurred while scraping jobs from Indeed: {str(exception)}")

    # close the Selenium web driver
    driver.quit()

    return jobs
