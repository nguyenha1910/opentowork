"""
This module contains unit tests for get_jobs
in the opentowork/scraper module.
Classes:
    TestGetJobsHelper - unit tests for helper functions in get_jobs module
    TestGetJobs - unit tests for get_jobs module
Functions:
    test_clean_date_smoke - smoke test for clean_date function
    test_clean_date_one_shot_posted - one-shot test for clean_date function
    test_clean_date_one_shot_employer - one-shot test for clean_date function
    test_clean_date_one_shot - one-shot test for clean_date function
    test_clean_date_output_type - tests output type for clean_date function
    test_clean_date_input_type_num - edge test for clean_date function input
    test_clean_date_input_type - edge test for clean_date function input
    test_calculate_pages_smoke - smoke test for calculate_pages function
    test_calculate_pages_one_shot - one-shot test for calculate_pages function
    test_calculate_pages_output - tests output type for calculate_pages function
    test_calculate_pages_target_job_count_type - edge test for calculate_pages input
    test_get_url_smoke - smoke test for get_url function
    test_get_url_output - tests output type for get_url function
    test_get_url_one_shot_linkedin - one-shot test for get_url, linkedin
    test_get_url_one_shot_indeed - one-shot test for get_url, indeed
    test_find_listings_smoke_linkedin - smoke test for find_listings, linkedin
    test_find_listings_smoke_indeed - smoke test for find_listings, indeed
    test_get_details_smoke_linkedin - smoke test for get_details, linkedin
    test_get_details_smoke_indeed - smoke test for get_details, indeed
    test_get_description_smoke_linkedin - smoke test for get_description, linkedin
    test_get_description_smoke_indeed - smoke test for get_description, indeed
    test_scrape_listings_smoke - smoke test for scrape_listings
    test_scrape_search_output - tests output for scrape_search function
    test_scrape_search_job_title_type - edge test for scrape_search function
    test_scrape_search_target_job_count_type - edge test for scrape_search function
    test_scrape_search_source_type - edge test for scrape_search function
    test_scrape_search_source_value - edge test for scrape_search function
"""
import unittest
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from opentowork.scraper.get_jobs import clean_date
from opentowork.scraper.get_jobs import calculate_pages
from opentowork.scraper.get_jobs import get_url
from opentowork.scraper.get_jobs import find_listings
from opentowork.scraper.get_jobs import get_details
from opentowork.scraper.get_jobs import get_description
from opentowork.scraper.get_jobs import scrape_listings
from opentowork.scraper.get_jobs import scrape_search

options = Options()
options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')

class TestGetJobsHelper(unittest.TestCase):
    """
    A class containing unit tests for helper functions in the get_jobs module.
    """
    def test_clean_date_smoke(self):
        """
        Test that clean_date runs and returns something.
        """
        result = clean_date("Posted 2 days ago")
        self.assertIsNotNone(result)

    def test_clean_date_one_shot_posted(self):
        """
        One-shot test for clean_date function, repetitive words.
        """
        self.assertEqual(clean_date("PostedPosted 2 days ago"), "Posted 2 days ago")

    def test_clean_date_one_shot_employer(self):
        """
        One-shot test for clean_date function, concatenated words.
        """
        self.assertEqual(clean_date("EmployerActive 2 days ago"), "Employer Active 2 days ago")

    def test_clean_date_one_shot(self):
        """
        One-shot test for clean_date function, no cleaning needed.
        """
        self.assertEqual(clean_date("Posted 2 days ago"), "Posted 2 days ago")

    def test_clean_date_output_type(self):
        """
        Tests that clean_date returns a string.
        """
        result = clean_date("Posted 2 days ago")
        self.assertTrue(isinstance(result, str),
                        "clean_date function output is not a String")

    def test_clean_date_input_type_num(self):
        """
        Edge test for clean_date input data type - needs to be String.
        """
        with self.assertRaises(TypeError):
            clean_date(200)

    def test_clean_date_input_type(self):
        """
        Edge test for clean_date input data type - needs to be String.
        """
        with self.assertRaises(TypeError):
            clean_date({'<span class="css-10pe3me eu4oa1w0">Employer</span>'})

    def test_calculate_pages_smoke(self):
        """
        Smoke test for calculate_pages function
        """
        result = calculate_pages(30)
        self.assertIsNotNone(result)

    def test_calculate_pages_one_shot(self):
        """
        One-shot test for calculate_pages function, expected output = (3, 15)
        """
        result = calculate_pages(35)
        self.assertEqual(result, (3, 15))

    def test_calculate_pages_output(self):
        """
        Test output of calculate_pages function, should be tuple
        """
        result = calculate_pages(10)
        self.assertTrue(isinstance(result, tuple), "calculate_pages output is not tuple")

    def test_calculate_pages_target_job_count_type(self):
        """
        Edge test calculate_pages should return TypeError for non-int input
        """
        with self.assertRaises(TypeError):
            calculate_pages(5.7)

    def test_get_url_smoke(self):
        """
        Test get_url runs and returns something.
        """
        result = get_url("LinkedIn", "abc", 0)
        self.assertIsNotNone(result)

    def test_get_url_output(self):
        """
        Test get_url returns a string.
        """
        result = get_url("LinkedIn", "abc", 0)
        self.assertTrue(isinstance(result, str), "get_url output is not string")

    def test_get_url_one_shot_linkedin(self):
        """
        One-shot test for get_url, LinkedIn
        """
        result = get_url("LinkedIn", "abc", 0)
        self.assertEqual(result, ("https://www.linkedin.com/jobs/search/?keywords="
                                  "abc&location=UnitedStates&start=0"))

    def test_get_url_one_shot_indeed(self):
        """
        One-shot test for get_url, Indeed
        """
        result = get_url("Indeed", "abc", 0)
        self.assertEqual(result, ("https://www.indeed.com/jobs?q=abc&"
                                  "l=United+States&start=0"))

class TestGetJobs(unittest.TestCase):
    """
    A class containing unit tests for the get_jobs module.
    """
    def test_find_listings_smoke_linkedin(self):
        """
        Smoke test for find_listings function, LinkedIn.
        """
        html = '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Sample Job Listings HTML</title>
            </head>
            <body>

            <div class="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card">
                <!-- First Job Listing -->
                <h3 class="base-search-card__title">Software Engineer</h3>
                <h4 class="base-search-card__subtitle">ABC Company</h4>
                <span class="job-search-card__location">New York, NY</span>
                <time class="job-search-card__listdate">Posted on January 15, 2023</time>
                <a class="base-card__full-link" href="https://example.com/apply123">Apply through company site</a>
            </div>

            <div class="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card">
                <!-- Second Job Listing -->
                <h3 class="base-search-card__title">Data Scientist</h3>
                <h4 class="base-search-card__subtitle">XYZ Corporation</h4>
                <span class="job-search-card__location">San Francisco, CA</span>
                <time class="job-search-card__listdate">Posted on January 20, 2023</time>
                <a class="base-card__full-link" href="https://example.com/apply456">Apply through company site</a>
            </div>

            </body>
            </html>
        '''
        soup = BeautifulSoup(html, "html.parser")
        results = find_listings(soup, "LinkedIn")
        self.assertIsNotNone(results)

    def test_find_listings_smoke_indeed(self):
        """
        Smoke test for find_listings function, Indeed.
        """
        html = '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Sample Job Listings HTML</title>
            </head>
            <body>

            <!-- First Job Listing -->
            <div class="cardOutline tapItem dd-privacy-allow result job">
                <h3 class="base-search-card__title">Software Engineer</h3>
                <h4 class="base-search-card__subtitle">ABC Company</h4>
                <span class="job-search-card__location">New York, NY</span>
                <time class="job-search-card__listdate">Posted 2 days ago</time>
                <a class="base-card__full-link" href="https://example.com/apply123">omg</a>
            </div>

            <!-- Second Job Listing -->
            <div class="cardOutline tapItem dd-privacy-allow result job">
                <h3 class="base-search-card__title">Data Scientist</h3>
                <h4 class="base-search-card__subtitle">XYZ Corporation</h4>
                <span class="job-search-card__location">San Francisco, CA</span>
                <time class="job-search-card__listdate">Posted yesterday</time>
                <a class="base-card__full-link" href="https://example.com/apply456">wa</a>
            </div>

            </body>
            </html>
        '''
        soup = BeautifulSoup(html, "html.parser")
        results = find_listings(soup, "LinkedIn")
        self.assertIsNotNone(results)

    def test_get_details_smoke_linkedin(self):
        """
        Smoke test for get_details function, LinkedIn.
        """
        html = '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Sample Job Card HTML</title>
            </head>
            <body>

            <div class="base-search-card">
                <h3 class="base-search-card__title">Software Engineer</h3>
                <h4 class="base-search-card__subtitle">ABC Company</h4>
                <span class="job-search-card__location">New York, NY</span>
                <time class="job-search-card__listdate">Posted on January 15, 2023</time>
                <a class="base-card__full-link" href="https://example.com/apply123">wa</a>
            </div>

            </body>
            </html>
        '''
        job = BeautifulSoup(html, 'html.parser')
        results = get_details(job, "LinkedIn")
        self.assertIsNotNone(results)

    def test_get_details_smoke_indeed(self):
        """
        Smoke test for get_details function, Indeed.
        """

        html = '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Sample Job Details HTML</title>
            </head>
            <body>

            <div class="job-details">
                <span id="jobTitle">Software Engineer</span>
                <div data-testid="company-name">ABC Company</div>
                <div data-testid="text-location">New York, NY</div>
                <div data-testid="myJobsStateDate">Posted on January 15, 2023</div>
                <a class="jcs-JobTitle" href="/apply123">Apply through company site</a>
            </div>

            </body>
            </html>
            '''
        job = BeautifulSoup(html, 'html.parser')
        results = get_details(job, "Indeed")
        self.assertIsNotNone(results)

    def test_get_description_smoke_linkedin(self):
        """
        Smoke test for get_description function, LinkedIn.
        """
        html = '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Sample Job Description HTML</title>
            </head>
            <body>

            <div class="job-description">
                <div class="description__text description__text--rich">
                    <p>This is a sample job description for a Software
                    Engineer position at ABC Company.</p>
                    <p>Key responsibilities include:</p>
                    <ul>
                        <li>Developing software applications</li>
                        <li>Collaborating with cross-functional teams</li>
                        <li>Testing and debugging code</li>
                    </ul>
                </div>
            </div>

            </body>
            </html>
        '''
        description_soup = BeautifulSoup(html, "html.parser")
        results = get_description(description_soup, "LinkedIn")
        self.assertIsNotNone(results)

    def test_get_description_smoke_indeed(self):
        """
        Smoke test for get_description function, Indeed.
        """
        html = '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Sample Job Description HTML</title>
            </head>
            <body>

            <div class="job-description">
                <div id="jobDescriptionText">
                    <p>This is a sample job description for a Software Engineer
                    position at ABC Company.</p>
                    <p>Key responsibilities include:</p>
                    <ul>
                        <li>Developing software applications</li>
                        <li>Collaborating with cross-functional teams</li>
                        <li>Testing and debugging code</li>
                    </ul>
                </div>
            </div>

            </body>
            </html>
        '''
        description_soup = BeautifulSoup(html, "html.parser")
        results = get_description(description_soup, "Indeed")
        self.assertIsNotNone(results)

    def test_scrape_listings_smoke(self):
        """
        Smoke test for scrape_listings function.
        """
        url = "https://www.indeed.com/jobs?q=job&l=United+States&start=0"
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_listings = find_listings(soup, "Indeed")
        results = scrape_listings(job_listings, driver, 2,
                                  True, 3, "Indeed")
        driver.quit()
        self.assertIsNotNone(results)

    def test_scrape_search_output(self):
        """
        Test scrape_search returns a list.
        """
        result = scrape_search('barista', 2, "Indeed")
        self.assertTrue(isinstance(result, list),
                        "indeed_job_listings output is not a list")

    def test_scrape_search_job_title_type(self):
        """
        Edge test scrape_search returns TypeError for job title input.
        """
        with self.assertRaises(TypeError):
            scrape_search(4, 2, "LinkedIn")

    def test_scrape_search_target_job_count_type(self):
        """
        Edge test scrape_search returns TypeError for target_job_count input.
        """
        with self.assertRaises(TypeError):
            scrape_search('technician', 2.5, "Indeed")

    def test_scrape_search_source_type(self):
        """
        Edge test scrape_search returns TypeError for source input.
        """
        with self.assertRaises(TypeError):
            scrape_search('magician', 3, 25)

    def test_scrape_search_source_value(self):
        """
        Edge test scrape_search returns ValueError for source input.
        """
        with self.assertRaises(ValueError):
            scrape_search('magician', 3, "Glassdoor")

if __name__ == '__main__':
    unittest.main()
