from datetime import datetime
import time
import random
from selenium import webdriver
from bs4 import BeautifulSoup

def clean_date(text):
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


def scrape_listings(job_listings, driver):
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

# pages: how many pages to scrape
# job_title_input: the job title you want to scrape
def indeed_job_listings(job_title_input, pages):
    jobs = [] # stores data listing data

    for i in range(pages):
        start_index = i * 15
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
            job_info = scrape_listings(job_listings, driver)
            # add data to the jobs list
            jobs = jobs + job_info
        # catch exception that occurs in the scraping process
        except Exception as exception:
            print(f"An error occurred while scraping jobs: {str(exception)}")

    # close the Selenium web driver
    driver.quit()

    return jobs
