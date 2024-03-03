from selenium import webdriver
from bs4 import BeautifulSoup
import random
import time
from datetime import datetime

# pages: how many pages to scrape
# job_title_input: the job title you want to scrape
def scrape_linkedin_job_listings(job_title_input, pages):
	job_listings_per_page = 25
	jobs = [] # stores data listing data

	for i in range(pages):
		start_index = i * job_listings_per_page
		url = f"https://www.linkedin.com/jobs/search/?keywords={job_title_input}&location=United%20States&start={start_index}"
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
		job_listings = soup.find_all("div", class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card")

		try:
			for job in job_listings:
				job_title = job.find("h3", class_="base-search-card__title").text.strip()
				job_company = job.find("h4", class_="base-search-card__subtitle").text.strip()
				job_location = job.find("span", class_="job-search-card__location").text.strip()
				posted_date = job.find("time", class_=lambda x: x and x.startswith("job-search-card__listdate")).text.strip()
				apply_link = job.find("a", class_="base-card__full-link")["href"]

				# navigate to the job posting page to scrape job description
				driver.get(apply_link)
	
				# sleeping randomly
				time.sleep(random.choice(list(range(5, 11))))
	
				try:
					description_soup = BeautifulSoup(driver.page_source, "html.parser")
					job_description = description_soup.find("div", class_="description__text description__text--rich").text.strip()

				# handle the AttributeError exception that may occur if the element is not found
				except AttributeError:
					job_description = None # job_description is None if not found
					print("AttributeError occurred while retrieving job description.")

				# add data to the jobs list
				jobs.append({"title": job_title,
							"company": job_company,
							"location": job_location,
							"posted date": posted_date,
				            "link": apply_link,
							"description": job_description,
							"scraped date": str(datetime.now())})

		# catch exception that occurs in the scrapping process
		except Exception as e:
			print(f"An error occurred while scraping jobs: {str(e)}")

	# close the Selenium web driver
	driver.quit()

	return jobs