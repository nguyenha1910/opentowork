import os
import unittest
import csv
from opentowork.scraper import job_listing_scraper

def count_csv_rows(file_path):
        with open(file_path, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            row_count = sum(1 for row in csv_reader)
        return row_count

class TestScraper(unittest.TestCase):

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
        job_listing_scraper.main()

    def test_scraper_check_csv_not_empty(self):
        job_listing_scraper.main()
        final_files = set(os.listdir('csvs/'))
        new_file = (final_files - self.initial_files).pop()
        self.assertTrue(new_file.endswith('.csv'))
        self.assertGreater(count_csv_rows('csvs/'+new_file), 1, "Generated file is empty")

if __name__ == '__main__':
    unittest.main()
