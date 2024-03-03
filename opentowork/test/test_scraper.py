"""
This module contains unit tests for the job_listing_scraper module
in the opentowork/scraper module.
"""
import os
import unittest
import csv
from opentowork.scraper import job_listing_scraper

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

class TestScraper(unittest.TestCase):
    """
    A class containing unit tests for the job_listing_scraper module.
    """
    def setUp(self):
        print("setting up...")
        self.initial_files = set(os.listdir('csvs/'))

    def tearDown(self):
        final_files = set(os.listdir('csvs/'))
        new_files = final_files - self.initial_files
        print("tearing down...")
        self.assertGreater(len(new_files), 0, "No new file created")
        self.assertEqual(len(new_files), 1, "Too many files created")

    def test_scraper_smoke(self):
        """
        Test that a file is created upon calling the function.
        """
        job_listing_scraper.main()

    def test_scraper_check_csv_type(self):
        """
        Test that the created file is a csv file.
        """
        job_listing_scraper.main()
        final_files = set(os.listdir('csvs/'))
        new_file = (final_files - self.initial_files).pop()
        self.assertTrue(new_file.endswith('.csv'))

    def test_scraper_check_file_has_data(self):
        """
        Test that the created file is not empty.
        """
        job_listing_scraper.main()
        final_files = set(os.listdir('csvs/'))
        new_file = (final_files - self.initial_files).pop()
        self.assertGreater(count_csv_rows('csvs/'+new_file), 1, "Generated file is empty")

if __name__ == '__main__':
    unittest.main()
