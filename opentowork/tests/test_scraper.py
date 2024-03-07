"""
This module contains unit tests for the job_listing_scraper module
in the opentowork/scraper module.
Classes:
    TestHelperFunctions - unit tests for helper functions in job_listing_scraper module
    TestScraper - unit tests for job_listing_scraper module
Functions:
    count_csv_rows - helper function for counting rows in csv
    test_jobs_per_title_smoke - smoke test for jobs_per_title function
    test_jobs_per_title_one_shot - one-shot test for jobs_per_title function
    test_jobs_per_title_job_titles_type - edge test for jobs_per_title function
    test_jobs_per_title_total_job_count_type - edge test for jobs_per_title function
    setUp - helper function for logging initial files before scraping
    tearDown - helper function for logging added files and cleaning up directory
    test_scraper_smoke - smoke test for job_listing_scraper
    test_scraper_check_csv_type - checks output is csv for job_listing_scraper
"""
import os
import unittest
import csv
from opentowork.scraper import job_listing_scraper
from opentowork.scraper.job_listing_scraper import jobs_per_title

directory = 'csvs/'

def count_csv_rows(file_path):
    """
    A function for counting the rows in a csv file.
    input: csv file path
    output: integer count of rows
    """
    with open(file_path, 'r', newline='', encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)
        row_count = sum(1 for row in csv_reader)
    return row_count

class TestHelperFunctions(unittest.TestCase):
    """
    A class containing unit tests for the helper functions in job_listing_scraper.
    """
    def test_jobs_per_title_smoke(self):
        """
        Smoke test for jobs_per_title function
        """
        result = jobs_per_title(['data analyst', 'data scientist'], 20)
        self.assertIsNotNone(result)

    def test_jobs_per_title_one_shot(self):
        """
        One-shot test for jobs_per_title function, expected output = 10
        """
        self.assertEqual(jobs_per_title(['data analyst', 'data scientist'], 20), 10)

    def test_jobs_per_title_job_titles_type(self):
        """
        Edge test for jobs_per_title function, job_titles type
        """
        with self.assertRaises(TypeError):
            jobs_per_title('data analyst', 20)

    def test_jobs_per_title_total_job_count_type(self):
        """
        Edge test for jobs_per_title function, total_job_count type
        """
        with self.assertRaises(TypeError):
            jobs_per_title(['data analyst'], 20.5)


class TestScraper(unittest.TestCase):
    """
    A class containing unit tests for the job_listing_scraper module's main function.
    """
    def setUp(self):
        print("setting up...")
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.initial_files = set(os.listdir(directory))

    def tearDown(self):
        final_files = set(os.listdir(directory))
        new_files = final_files - self.initial_files
        print("tearing down...")
        #clean up files/directories made during testing
        for file in new_files:
            os.remove(directory + file)
        if len(self.initial_files) == 0:
            os.rmdir(directory)
        else:
            pass
        self.assertGreater(len(new_files), 0, "No new file created")
        self.assertEqual(len(new_files), 1, "Too many files created")

    def test_scraper_smoke(self):
        """
        Test that a file is created upon calling the function.
        """
        job_listing_scraper.main(total_job_count = 6)

    def test_scraper_check_csv_type(self):
        """
        Test that the created file is a csv file.
        """
        job_listing_scraper.main(total_job_count = 6)
        final_files = set(os.listdir(directory))
        new_file = (final_files - self.initial_files).pop()
        self.assertTrue(new_file.endswith('.csv'))

    # commented out to allow for empty files -> if empty then tell user on frontend
    # def test_scraper_check_file_has_data(self):
    #     """
    #     Test that the created file is not empty.
    #     """
    #     job_listing_scraper.main()
    #     final_files = set(os.listdir(directory))
    #     new_file = (final_files - self.initial_files).pop()
    #     self.assertGreater(count_csv_rows(directory+new_file), 1, "Generated file is empty")

if __name__ == '__main__':
    unittest.main()
