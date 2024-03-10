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

def get_details(job, source):
    if source == "LinkedIn":
        job_title = job.find("h3", class_="base-search-card__title").text.strip()
        job_company = job.find("h4", class_="base-search-card__subtitle").text.strip()
        job_location = job.find("span", class_="job-search-card__location").text.strip()
        posted_date = job.find("time", class_=lambda x: x and
                                x.startswith("job-search-card__listdate")).text.strip()
        apply_link = job.find("a", class_="base-card__full-link")["href"]
    if source == "Indeed":
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
    if source == "LinkedIn":
        description = description_soup.find("div", class_=("description__text "
                                                            "description__text--"
                                                                "rich")).text
        job_description = description.strip().replace('\n', '')
    if source == "Indeed":
        description = description_soup.find("div", id='jobDescriptionText').text
    job_description = description.strip().replace('\n', '')
    return job_description

def get_url(source, job_title_input, start_index):
    if source == "LinkedIn":
        base_url = "https://www.linkedin.com/jobs/search/?keywords="
        url = base_url + f"{job_title_input}&location=UnitedStates&start={start_index}"
    if source == "Indeed":
        url = f"https://www.indeed.com/jobs?q={job_title_input}&l=United+States&start={start_index}"
    return url

def find_listings(soup, source):
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
    listings = []
    for job in job_listings:
        details = get_details(job, source)
        # navigate to the job posting page to scrape job description
        driver.get(details[4])
        # sleeping randomly
        time.sleep(random.choice(list(range(5, 11))))
        try:
            description_soup = BeautifulSoup(driver.page_source, "html.parser")
            job_description = get_description(description_soup, source)
        # handle the AttributeError exception that may occur if the element is not found
        except AttributeError:
            job_description = None # job_description is None if not found
            print("AttributeError occurred while retrieving job description.")
        job_data = details.append(job_description)
        if all(job_detail is not None for job_detail in job_data):
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