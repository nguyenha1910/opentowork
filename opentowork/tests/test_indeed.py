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

    def test_scrape_jobs_smoke(self):
        """
        Test indeed_job_listings runs and returns something.
        """
        result = indeed_job_listings('data analyst', 1)
        self.assertIsNotNone(result)

    def test_scrape_jobs_output(self):
        """
        Test indeed_job_listings returns a list.
        """
        result = indeed_job_listings('data scientist', 1)
        self.assertTrue(isinstance(result, list),
                        "indeed_job_listings output is not a list")

    def test_scrape_jobs_job_title_type(self):
        """
        Edge test indeed_job_listings returns TypeError for job title input.
        """
        with self.assertRaises(TypeError):
            indeed_job_listings(4, 2)

    def test_scrape_jobs_pages_type(self):
        """
        Edge test indeed_job_listings returns TypeError for page number input.
        """
        with self.assertRaises(TypeError):
            indeed_job_listings('data engineer', 2.5)

if __name__ == '__main__':
    unittest.main()
