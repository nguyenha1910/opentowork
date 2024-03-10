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
    def test_get_sim_score(self):
        """
        Test the get_sim_score function with a valid job description and resume.
        """
        scraped_data_path = 'data/csvs/job_listings_new.csv'
        resume_path = "data/pdfs/random_ds_resume.pdf"
        job_posting = pd.read_csv(scraped_data_path).iloc[0]
        description = job_posting['description']
        _, resume_content = get_resume_skills(resume_path)
        expected_score = 0.29
        actual_score = get_sim_score(description, resume_content)
        self.assertAlmostEqual(actual_score, expected_score, places=2)

if __name__ == '__main__':
    unittest.main()
