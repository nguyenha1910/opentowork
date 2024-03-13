# pylint: disable=redundant-unittest-assert
# needed for smoke test assertTrue
"""
Test the get_sim_score function in the opentowork module.
"""
import unittest
import pandas as pd
from opentowork.skill_extraction import get_resume_skills
from opentowork.sim_score import get_sim_score

class TestSimScore(unittest.TestCase):
    """
    A class containing unit tests for the sim_score module.
    """
    def test_smoke(self):
        """
        A smoke test to ensure that the test suite is working.
        """
        get_sim_score("", "")
        self.assertTrue(True)

    def test_get_sim_score(self):
        """
        Test the get_sim_score function with a valid job description and resume.
        """
        scraped_data_path = (
            'data/csvs/job_listings_data_analyst_data_scientist_data_engineer_'
            '30_jobs_scraped_20240312_183404.csv'
        )
        resume_path = "data/pdfs/sample_resume.pdf"
        job_posting = pd.read_csv(scraped_data_path).iloc[0]
        description = job_posting['description']
        _, resume_content = get_resume_skills(resume_path)
        expected_score = 0.13
        actual_score = get_sim_score(description, resume_content)
        self.assertGreaterEqual(actual_score, 0.0)
        self.assertLessEqual(actual_score, 1.0)
        self.assertAlmostEqual(actual_score, expected_score, places=2)

if __name__ == '__main__':
    unittest.main()
