# pylint: disable=broad-exception-caught
# disabled due to variability in scraping exceptions, no specific expected exception
# pylint: disable=too-many-arguments
# disabled due to all arguments necessary (6/5)
# pylint: disable=possibly-used-before-assignment

"""
Module retrieves job information from LinkedIn and Indeed using Selenium and BeautifulSoup.
Returns a list of job information stores as dictionaries.
Functions:
    clean_date - cleans scraped date for indeed job listings
    calculate_pages - calculates the number of pages needed for specific number of jobs
    get_url - creates url to scrape from
    find_listings - uses BeautifulSoup to find job listings on search page
    get_details - gathers job details from input generated with BeautifulSoup
    get_description - retrieves job description from job link
    scrape_listings - gathers job details for each job in search
    scrape_search - initializes scraping and creates list of jobs
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

def get_url(source, job_title_input, start_index):
    """
    Function creates url to start scraping jobs from depending on job source.
    Args:
        source (string): either "LinkedIn" or "Indeed"
        job_title_input (string): job title to search for
        start_index (int): start index for search page, used to paginate
    Returns:
        url (string): search url to scrape from
    """
    if source == "LinkedIn":
        base_url = "https://www.linkedin.com/jobs/search/?keywords="
        url = base_url + f"{job_title_input}&location=UnitedStates&start={start_index}"
    elif source == "Indeed":
        url = f"https://www.indeed.com/jobs?q={job_title_input}&l=United+States&start={start_index}"
    return url

def get_details(job, source):
    """
    Function finds details of each job listing from job passed in from scrape_listings.
    Uses BeautifulSoup to identify specific details.
    Args:
        job (Tag): contains details for a job in HTML
        source (string): either "LinkedIn" or "Indeed"
    Returns:
        [job_title, job_company, job_location, posted_date, apply_link] (list):
        list of job details
    """
    if source == "LinkedIn":
        job_title = job.find("h3", class_="base-search-card__title").text.strip()
        job_company = job.find("h4", class_="base-search-card__subtitle").text.strip()
        job_location = job.find("span", class_="job-search-card__location").text.strip()
        posted_date = job.find("time", class_=lambda x: x and
                                x.startswith("job-search-card__listdate")).text.strip()
        apply_link = job.find("a", class_="base-card__full-link")["href"]
    elif source == "Indeed":
        job_title = job.find("span", id=lambda x: x and
                            x.startswith('jobTitle')).text.strip()
        job_company = job.find(attrs={'data-testid':'company-name'}).text.strip()
        job_location = job.find(attrs={'data-testid':'text-location'}).text.strip()
        posted_date = clean_date(job.find(attrs={'data-testid':
                                                    'myJobsStateDate'}).text.strip())
        apply_link = 'https://indeed.com' + job.find("a", class_=lambda x: x
                                                and x.startswith('jcs-JobTitle'))["href"]
    return [job_title, job_company, job_location, posted_date, apply_link]

def get_description(description_soup, source):
    """
    Function gets job description from job posting page using BeautifulSoup.
    Args:
        description_soup (BeautifulSoup): generated in scrape_listings function
        source (string): either "LinkedIn" or "Indeed"
    Returns:
        job_description (string): job description retrieved from job posting
    """
    if source == "LinkedIn":
        description = description_soup.find("div", class_=("description__text "
                                                            "description__text--"
                                                                "rich")).text
        job_description = description.strip().replace('\n', '')
    if source == "Indeed":
        description = description_soup.find("div", id='jobDescriptionText').text
    job_description = description.strip().replace('\n', '')
    return job_description

def find_listings(soup, source):
    """
    Function takes BeautifulSoup input and finds job listings using specified class.
    Args:
        soup (BeautifulSoup): generated from scrape_search function
        source (string): either "LinkedIn" or "Indeed"
    Returns:
        job_listings (ResultSet): contains div tags matching specified class
    """
    if source == "LinkedIn":
        job_listings = soup.find_all("div", class_=("base-card relative w-full hover:no-underline "
                                                        "focus:no-underline "
                                                        "base-card--link base-search-card "
                                                        "base-search-card--link job-search-card"))
    if source == "Indeed":
        job_listings = soup.find_all("div", class_=lambda x: x and
                                    x.startswith('cardOutline tapItem dd-privacy-allow result job'))
    return job_listings

def scrape_listings(job_listings, driver, valid_job_count, last_page, target_job_count, source):
    """
    Function takes soup from BeautifulSoup and calls get_details, get_description
    to generate job details. Iterates through each job in job_listings and stores
    job details in a list of dictionaries.
    Args:
        job_listings (BeautifulSoup): generated from soup.find_all() looking for a
        specific class
        driver (Chrome webdriver): Chrome webdriver from selenium
        valid_job_count (int): number of jobs with no None values
        last_page (boolean): indicator for last page
        target_job_count (int): targeted number of jobs to scrape
        source (string): either "LinkedIn" or "Indeed"
    Returns:
    in a tuple:
        listings (list): list of job info, each job is its own dictionary with the
        job attribute as a key and scraped detail as value
        valid_job_count (int): count of valid jobs scraped
    """
    listings = []
    for job in job_listings:
        job_data = get_details(job, source)
        # navigate to the job posting page to scrape job description
        driver.get(job_data[4])
        # sleeping randomly
        time.sleep(random.choice(list(range(5, 11))))
        try:
            description_soup = BeautifulSoup(driver.page_source, "html.parser")
            job_description = get_description(description_soup, source)
        # handle the AttributeError exception that may occur if the element is not found
        except AttributeError:
            job_description = None # job_description is None if not found
            print("AttributeError occurred while retrieving job description.")
        job_data.append(job_description)
        if all(detail is not None for detail in job_data):
            listings.append({"title": job_data[0],
                        "company": job_data[1],
                        "location": job_data[2],
                        "posted date": job_data[3],
                        "link": job_data[4],
                        "description": job_data[5],
                        "scraped date": str(datetime.now())})
            valid_job_count += 1
        if last_page is True and valid_job_count >= target_job_count:
            break

    return (listings, valid_job_count)

def scrape_search(job_title_input, target_job_count, source):
    """
    Function initializes the scraping process by getting search url for the
    inputed job title and number of pages. Calls calculate_pages, get_url, find_listings,
    and scrape_listings functions. Returns one list with all the job listings.
    Uses selenium and BeautifulSoup.
    Args:
        job_title_input (string): job title to search for
        target_job_count (int): number of jobs to get
        source (string): either "LinkedIn" or "Indeed"
    Returns:
        jobs (list): list of job details, each job is its own dictionary, generated
        from scrape_indeed_listings
    Exceptions:
        TypeError for job_title_input (should be string)
        TypeError for target_job_count (should be int)
        TypeError for source (should be string)
        ValueError for source (either "LinkedIn" or "Indeed")
    """
    if isinstance(job_title_input, str) is not True:
        raise TypeError("Job title input is not a string")
    if isinstance(target_job_count, int) is not True:
        raise TypeError("Target job count input is not an int")
    if isinstance(source, str) is not True:
        raise TypeError("Source is not a string")
    if source not in ["LinkedIn", "Indeed"]:
        raise ValueError("Source needs to be LinkedIn or Indeed")

    pages = calculate_pages(target_job_count)
    jobs = []
    valid_job_count = 0
    last_page = False

    for i in range(pages[0]):
        time.sleep(random.uniform(1, 3))
        if i == pages[0]-1:
            last_page = True
        start_index = i * pages[1]
        url = get_url(source, job_title_input, start_index)
        print(f"Scraping from this url: {url}")

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # scroll to the bottom of the page using JavaScript
        # print(f"Scrolling to bottom of page {i+1}")
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for a random amount of time before scrolling to the next page
        time.sleep(random.choice(list(range(3, 7))))
        # Scrape the job postings
        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_listings = find_listings(soup, source)
        try:
            results = scrape_listings(job_listings, driver, valid_job_count,
                                      last_page, target_job_count, source)
            # add data to the jobs list
            jobs = jobs + results[0]
            valid_job_count = results[1]
        # catch exception that occurs in the scraping process
        except Exception as exception:
            print(f"An error occurred while scraping jobs from LinkedIn: {str(exception)}")
    # close the Selenium web driver
    driver.quit()

    return jobs
