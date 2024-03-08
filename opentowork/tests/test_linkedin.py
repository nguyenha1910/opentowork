"""
This module contains unit tests for the linkedin_jobs module
in the opentowork/scraper module.
Classes:
    TestLinkedin - unit tests for linkedin_jobs module
Functions:
    test_calculate_pages_smoke - smoke test for calculate_pages function
    test_calculate_pages_one_shot - one-shot test for calculate_pages function
    test_calculate_pages_output - tests output type for calculate_pages function
    test_calculate_pages_target_job_count_type - edge test for calculate_pages input
    test_scrape_jobs_smoke - smoke test for linkedin_job_listings
    test_scrape_jobs_output - checks linkedin_job_listings output type
    test_scrape_jobs_job_title_type - edge test for job title input type
    test_scrape_jobs_pages_type - edge test for page number input type
"""
import unittest
from opentowork.scraper.linkedin_jobs import calculate_pages
from opentowork.scraper.linkedin_jobs import linkedin_job_listings

class TestLinkedin(unittest.TestCase):
    """
    A class containing unit tests for the linkedin_jobs module.
    """
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

    def test_scrape_jobs_smoke(self):
        """
        Test linkedin_job_listings runs and returns something.
        """
        result = linkedin_job_listings('software', 2)
        self.assertIsNotNone(result)

    def test_scrape_jobs_output(self):
        """
        Test linkedin_job_listings returns a list.
        """
        result = linkedin_job_listings('electrical engineer', 2)
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
            linkedin_job_listings('artist', 2.5)

if __name__ == '__main__':
    unittest.main()
