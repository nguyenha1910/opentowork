# pylint: disable=broad-exception-caught
# disabled due to variability in scraping exceptions, no specific expected exception
"""
Module retrieves job information from linkedin.com using Selenium and BeautifulSoup.
Returns a list of job information stores as dictionaries.
Functions:
    calculate_pages - calculates the number of pages needed for specific number of jobs
    scrape_linkedin_listings - gathers job details from input generated with BeautifulSoup
    linkedin_job_listings - searches job title on linkedin.com, calls scrape_indeed_listings
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
options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')

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

def scrape_linkedin_listings(job_listings, driver, valid_job_count, last_page, target_job_count):
    """
    Function takes soup from BeautifulSoup and strips out the job title, company
    location, posted date, and link. It then gets the job description from the link.
    Inputs in the .find() functions are specific to linkedin.com
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
        job_title = job.find("h3", class_="base-search-card__title").text.strip()
        job_company = job.find("h4", class_="base-search-card__subtitle").text.strip()
        job_location = job.find("span", class_="job-search-card__location").text.strip()
        posted_date = job.find("time", class_=lambda x: x and
                                x.startswith("job-search-card__listdate")).text.strip()
        apply_link = job.find("a", class_="base-card__full-link")["href"]
        # navigate to the job posting page to scrape job description
        driver.get(apply_link)
        # sleeping randomly
        time.sleep(random.choice(list(range(5, 11))))
        try:
            description_soup = BeautifulSoup(driver.page_source, "html.parser")
            job_description = description_soup.find("div", class_=("description__text "
                                                                   "description__text--"
                                                                   "rich")).text.strip()
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

def linkedin_job_listings(job_title_input, target_job_count):
    """
    Function initializes the scraping process by going to the linkedin.com search for the
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
        TypeError for job_title_input arg (if job_title_input is not string)
        TypeError for target_job_count arg (if target_job_count is not int)
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
        base_url = "https://www.linkedin.com/jobs/search/?keywords="
        url = base_url + f"{job_title_input}&start={start_index}"
        print(f"Scraping from this url: {url}")

        driver = webdriver.Chrome(options=options)
        driver.get(url)
        # scroll to the bottom of the page using JavaScript
        # print(f"Scrolling to bottom of page {i+1}")
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # testing!!!!!!!!
        # Wait for a random amount of time before scrolling to the next page
        time.sleep(random.choice(list(range(3, 7))))
        # Scrape the job postings
        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_listings = soup.find_all("div", class_=("base-card relative w-full hover:no-underline "
                                                    "focus:no-underline "
                                                    "base-card--link base-search-card "
                                                    "base-search-card--link job-search-card"))
        try:
            results = scrape_linkedin_listings(job_listings, driver, valid_job_count,
                                             last_page, target_job_count)
            # add data to the jobs list
            jobs = jobs + results[0]
            valid_job_count = results[1]
        # catch exception that occurs in the scraping process
        except Exception as exception:
            print(f"An error occurred while scraping jobs from LinkedIn: {str(exception)}")
    # close the Selenium web driver
    driver.quit()

    return jobs
