"""
This module contains unit tests for the linkedin_jobs module
in the opentowork/scraper module.
Classes:
    TestLinkedin - unit tests for linkedin_jobs module
Functions:
    test_scrape_jobs_smoke - smoke test for linkedin_job_listings
    test_scrape_jobs_output - checks linkedin_job_listings output type
    test_scrape_jobs_job_title_type - edge test for job title input type
    test_scrape_jobs_pages_type - edge test for page number input type
"""
import unittest
from opentowork.scraper.linkedin_jobs import linkedin_job_listings

class TestLinkedin(unittest.TestCase):
    """
    A class containing unit tests for the linkedin_jobs module.
    """
    def test_scrape_jobs_smoke(self):
        """
        Test linkedin_job_listings runs and returns something.
        """
        result = linkedin_job_listings('data analyst', 2)
        self.assertIsNotNone(result)

    def test_scrape_jobs_output(self):
        """
        Test linkedin_job_listings returns a list.
        """
        result = linkedin_job_listings('data scientist', 2)
        self.assertTrue(isinstance(result, list),
                        "linkedin_job_listings output is not a list")

    def test_scrape_jobs_job_title_type(self):
        """
        Edge test linkedin_job_listings returns TypeError for job title input.
        """
        with self.assertRaises(TypeError):
            linkedin_job_listings(4, 2)

    def test_scrape_jobs_pages_type(self):
        """
        Edge test linkedin_job_listings returns TypeError for page number input.
        """
        with self.assertRaises(TypeError):
            linkedin_job_listings('data engineer', 2.5)

if __name__ == '__main__':
    unittest.main()
