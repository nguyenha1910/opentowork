# pylint: disable=wrong-import-position
# disabled because pylint confused import order
"""
This module contains the ui tests for the app and job_recommendation modules.
"""
import sys
import os
import unittest
import yaml
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from opentowork.pages.job_recommendation import get_latest_csv_file
from opentowork.pages.job_recommendation import get_temp_path

# Load config file
with open("config.yml", "r", encoding='UTF-8') as config_file:
    config = yaml.safe_load(config_file)


class TestHelperFunctions(unittest.TestCase):
    """
    Class containing tests for the helper functions
    """
    def test_get_latest_csv_file_smoke(self):
        """
        Smoke test for get_latest_csv_file function
        """
        latest_csv_file, last_scraped_dt = get_latest_csv_file()
        self.assertIsNotNone(latest_csv_file)
        self.assertIsNotNone(last_scraped_dt)

    def test_get_latest_csv_file_output(self):
        """
        Check output types for get_latest_csv_file function
        """
        latest_csv_file, last_scraped_dt = get_latest_csv_file()
        self.assertTrue(isinstance(latest_csv_file, str))
        self.assertTrue(isinstance(last_scraped_dt, str))

    def test_get_temp_path_smoke(self):
        """
        Smoke test for get_temp_path function
        """
        data_path = ('job_listings_data_analyst_data_scientist'
                    '_data_engineer_30_jobs_scraped_20240312_'
                    '183404.csv')
        temp_path = get_temp_path(data_path)
        self.assertIsNotNone(temp_path)

    def test_get_temp_path_oneshot(self):
        """
        One-shot test for get_temp_path function
        """
        data_path = ('job_listings_data_analyst_data_scientist'
                    '_data_engineer_30_jobs_scraped_20240312_'
                    '183404.csv')
        expected_out = ('job_listings_data_analyst_data_scientist'
                        '_data_engineer_30_jobs_scraped_20240312_'
                        '183404_temp.csv')
        temp_path = get_temp_path(data_path)
        self.assertEqual(temp_path, expected_out)

    def test_get_temp_path_output(self):
        """
        Check output type for get_temp_path function
        """
        data_path = ('job_listings_data_analyst_data_scientist'
                    '_data_engineer_30_jobs_scraped_20240312_'
                    '183404.csv')
        temp_path = get_temp_path(data_path)
        self.assertTrue(isinstance(temp_path, str))
