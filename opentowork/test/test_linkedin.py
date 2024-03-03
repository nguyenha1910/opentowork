"""
This module contains unit tests for the linkedin_jobs module
in the opentowork/scraper module.
"""
import unittest
from opentowork.scraper.linkedin_jobs import linkedin_job_listings

class TestLinkedin(unittest.TestCase):
    """
    A class containing unit tests for the linkedin_jobs module.
    """
    def test_scrape_jobs_smoke(self):
        result = linkedin_job_listings('data analyst', 1)
        self.assertIsNotNone(result)

    def test_scrape_jobs_output(self):
        result = linkedin_job_listings('data scientist', 1)
        self.assertTrue(isinstance(result, list),
                        "linkedin_job_listings output is not a list")

    def test_scrape_jobs_job_title_type(self):
        with self.assertRaises(TypeError):
            linkedin_job_listings(4, 2)

    def test_scrape_jobs_pages_type(self):
        with self.assertRaises(TypeError):
            linkedin_job_listings('data engineer', 2.5)

if __name__ == '__main__':
    unittest.main()