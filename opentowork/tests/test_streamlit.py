"""test_streamlit.py"""
import unittest
import os
import sys
import streamlit as st
from streamlit.testing.v1 import AppTest
from opentowork.pages.job_recommendation import status_update


class TestStreamlit(unittest.TestCase):
    """
    A class containing ui tests for the job_recommendation and app modules.
    """
    def setUp(self):
        """
        The unittest framework automatically runs this `setUp` function before
        each test. By refactoring the creation of the AppTest into a common
        function, we reduce the total amount of code in the file.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.abspath(os.path.join(current_dir, '..'))
        sys.path.append(project_dir)
        print("project_dir:", project_dir)

        self.at = AppTest.from_file('../app.py').run()
        #self.at = AppTest.from_file('../pages/job_recommendation.py', default_timeout=10).run()

    def test_title(self):
        """ Test title """
        self.assertEqual(self.at.title[0].value, "Open To Work")


    def test_file_uploader(self):
        """TODO: test upload resume button"""
        pass


    def test_update_job_posting_data_button(self):
        pass


    def test_status_update_button(self):
        """ TODO: Test job application info update button """
        test_job_data = {
            'company': 'Test Company',
            'title': 'Test Job',
            'location': 'Test Location',
            'link': 'https://test.com'
        }





