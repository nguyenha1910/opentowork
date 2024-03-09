"""test_streamlit.py"""
import unittest
import os
import sys
import pdb # delete later
from unittest import mock
import streamlit as st
from streamlit.testing.v1 import AppTest
from opentowork.pages.job_recommendation import status_update
from opentowork.app import app
from opentowork.skill_extraction import get_resume_skills
from opentowork.skill_extraction import get_job_description_skills


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

        self.at = AppTest.from_file('../app.py')#.run()
        #self.at = AppTest.from_file('../pages/job_recommendation.py').run()

        class MockFileUploader(object):
            def __init__(self):
                self.name = 'resume.pdf'

            def getvalue(self):
                path = "pdfs/random_ds_resume.pdf"
                # open a test pdf file, read in
                with open(path, mode='rb') as real_pdf:
                    return real_pdf.read() # just raw content of pdf

        mock_file_uploader.return_value = MockFileUploader() 

        self.at.run(timeout=20)

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
        if self.at.button[1]:
            first_applied_button = self.at.button[1]
            self.assertTrue(first_applied_button.click()._value)