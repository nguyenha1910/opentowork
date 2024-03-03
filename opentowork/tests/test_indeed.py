"""
This module contains unit tests for the indeed_jobs module
in the opentowork/scraper module.
"""
import unittest
from opentowork.scraper.indeed_jobs import indeed_job_listings
from opentowork.scraper.indeed_jobs import clean_date

class TestIndeed(unittest.TestCase):
    """
    A class containing unit tests for the indeed_jobs module.
    """
    def test_clean_date_smoke(self):
        result = clean_date("Posted 2 days ago")
        self.assertIsNotNone(result)

    def test_clean_date_one_shot_posted(self):
        self.assertEqual(clean_date("PostedPosted 2 days ago"), "Posted 2 days ago")

    def test_clean_date_one_shot_employer(self):
        self.assertEqual(clean_date("EmployerActive 2 days ago"), "Employer Active 2 days ago")

    def test_clean_date_output_type(self):
        result = clean_date("Posted 2 days ago")
        self.assertTrue(isinstance(result, str),
                        "clean_date function output is not a String")

    def test_clean_date_input_type_num(self):
        with self.assertRaises(TypeError):
            clean_date(200)

    def test_clean_date_input_type(self):
        with self.assertRaises(TypeError):
            clean_date({'<span class="css-10pe3me eu4oa1w0">Employer</span>'})

    def test_scrape_jobs_smoke(self):
        result = indeed_job_listings('data analyst', 1)
        self.assertIsNotNone(result)

    def test_scrape_jobs_output(self):
        result = indeed_job_listings('data scientist', 1)
        self.assertTrue(isinstance(result, list),
                        "indeed_job_listings output is not a list")

    def test_scrape_jobs_job_title_type(self):
        with self.assertRaises(TypeError):
            indeed_job_listings(4, 2)

    def test_scrape_jobs_pages_type(self):
        with self.assertRaises(TypeError):
            indeed_job_listings('data engineer', 2.5)

if __name__ == '__main__':
    unittest.main()
