# pylint: disable=duplicate-code
# disabling for now
"""
This module contains unit tests for the indeed_jobs module
in the opentowork/scraper module.
Classes:
    TestIndeed - unit tests for indeed_jobs module
Functions:
    test_clean_date_smoke - smoke test for clean_date function
    test_clean_date_one_shot_posted - one-shot test for clean_date function
    test_clean_date_one_shot_employer - one-shot test for clean_date function
    test_clean_date_output_type - tests output type for clean_date function
    test_clean_date_input_type_num - edge test for clean_date function input
    test_clean_date_input_type - edge test for clean_date function input
    test_calculate_pages_smoke - smoke test for calculate_pages function
    test_calculate_pages_one_shot - one-shot test for calculate_pages function
    test_calculate_pages_output - tests output type for calculate_pages function
    test_calculate_pages_target_job_count_type - edge test for calculate_pages input
    test_scrape_jobs_smoke - smoke test for linkedin_job_listings
    test_scrape_jobs_output - checks linkedin_job_listings output type
    test_scrape_jobs_job_title_type - edge test for job title input type
    test_scrape_jobs_target_job_count_type - edge test for target_job_count type
"""
import unittest
from opentowork.scraper.indeed_jobs import clean_date
from opentowork.scraper.indeed_jobs import calculate_pages
from opentowork.scraper.indeed_jobs import indeed_job_listings


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
        Test indeed_job_listings runs and returns something.
        """
        result = indeed_job_listings('nail art', 2)
        self.assertIsNotNone(result)

    def test_scrape_jobs_output(self):
        """
        Test indeed_job_listings returns a list.
        """
        result = indeed_job_listings('barista', 2)
        self.assertTrue(isinstance(result, list),
                        "indeed_job_listings output is not a list")

    def test_scrape_jobs_job_title_type(self):
        """
        Edge test indeed_job_listings returns TypeError for job title input.
        """
        with self.assertRaises(TypeError):
            indeed_job_listings(4, 2)

    def test_scrape_jobs_target_job_count_type(self):
        """
        Edge test indeed_job_listings returns TypeError for target_job_count input.
        """
        with self.assertRaises(TypeError):
            indeed_job_listings('technician', 2.5)

if __name__ == '__main__':
    unittest.main()
