# pylint: disable=W0221
# disabling due to use of setup function in 2 different test files
# pylint: disable=protected-access
# disabling bc we need _value (attribute name of the object)
# pylint: disable=too-few-public-methods
# disabled because using class as mock file uploader

"""
This module contains the ui tests for the app and job_recommendation modules.
"""
import unittest
import os
import sys
from unittest import mock
import yaml
from streamlit.testing.v1 import AppTest
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

    def test_get_latest_csv_file_oneshot(self):
        """
        One-shot test for get_latest_csv_file function
        """
        latest_csv_file, last_scraped_dt = get_latest_csv_file()
        self.assertTrue(('job_listings_data_analyst_data_scientist'
                        '_data_engineer_30_jobs_scraped_20240312_'
                        '183404.csv') in latest_csv_file)
        self.assertTrue('2024' in last_scraped_dt)

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

class TestStreamlit(unittest.TestCase):
    """
    A class containing ui tests for the job_recommendation and app modules.
    """
    @mock.patch('streamlit.file_uploader')
    def setUp(self, mock_file_uploader):
        """
        The unittest framework automatically runs this `setUp` function before
        each test. By refactoring the creation of the AppTest into a common
        function, we reduce the total amount of code in the file.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.abspath(os.path.join(current_dir, '..'))
        sys.path.append(project_dir)

        self.at = AppTest.from_file('../app.py')

        class MockFileUploader():
            """
            Mock file uploader class for testing purposes.
            """
            def __init__(self):
                self.name = 'resume.pdf'

            def getvalue(self):
                """
                Get the content of the uploaded file.
                Returns: The raw content of the uploaded file.
                """
                path = "data/pdfs/sample_resume.pdf"
                # open a test pdf file, read in
                with open(path, mode='rb') as real_pdf:
                    return real_pdf.read() # just raw content of pdf

        mock_file_uploader.return_value = MockFileUploader()
        self.at.run(timeout=120)

    def test_title(self):
        """ Test title """
        self.assertEqual(self.at.title[0].value, "Open To Work")

    def test_update_data_button_label(self):
        """ Test the label of the 'Update Job Posting Data' button """
        self.assertEqual(self.at.button[0].label, "Update Job Posting Data")

    def test_update_data_button(self):
        """ Test the update data button """
        update_button = self.at.button[0]
        self.assertTrue(update_button.click()._value)

    def test_applied_button(self):
        """ Test the applied button """
        if len(self.at.button) > 1:
            first_applied_button = self.at.button[1]
            self.assertTrue(first_applied_button.click()._value)
            self.assertEqual(first_applied_button.click().label, "I applied!")
            self.assertTrue( self.at.session_state['job_loaded'])
            self.assertTrue(os.path.exists(config['status_csv_path']))

    def test_expander_exists(self):
        """ Test that the expander exists """
        self.assertTrue(self.at[0][5].type in ['expandable', 'expander'])

    def test_dataframe_cols(self):
        """ Test that columns in the dataframe are as expected"""
        df_columns = self.at.dataframe[0].value.columns
        expected_columns = ['Company Name', 'Position Title', 'Location', 'Status', 'Date']
        self.assertCountEqual(df_columns, expected_columns)

    def test_job_description(self):
        """ Test that the job description is not empty"""
        description = self.at.markdown[2].value
        self.assertIsInstance(description, str)
        self.assertNotEqual(description, "")

if __name__ == '__main__':
    unittest.main()
