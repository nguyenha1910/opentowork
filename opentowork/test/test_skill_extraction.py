"""
This module contains unit tests for the 
skill_extraction function in the opentowork module.
"""

import unittest
from opentowork.skill_extraction import skill_extraction

class TestSkillExtraction(unittest.TestCase):
    """
    A class containing unit tests for the skill_extraction function.
    """
    def test_valid_pdf(self):
        """
        Test the skill_extraction function with a valid PDF file.
        """
        path = "pdf/random_ds_resume.pdf"
        skills = skill_extraction(path)
        expected = ['neo4j', 'sqlite', 'engineering', 'finance', 
                    'monitoring', 'design', 'python', 'algorithms', 
                    'google', 'multivariate analysis', 'tensorflow', 
                    'tableau', 'r', 'd3.js', 'machine learning', 
                    'big data', 'mysql', 'data visualization', 'storm', 
                    'variables', 'motion detection', 'time series', 
                    'opencv', 'api', 'visualization', 'logistic regression', 
                    'smoothing', 'mobile', 'data analysis', 'business', 
                    'bash', 'anomaly detection', 'data mining', 
                    'gradient descent', 'hadoop', 'sql', 'data science', 
                    'git']
        self.assertIsInstance(skills, list)
        self.assertGreater(len(skills), 0)
        self.assertCountEqual (skills, expected)
        
if __name__ == "__main__":
    unittest.main()
