"""
This module contains unit tests for the
skill_extraction function in the opentowork module.
"""
import os
import unittest
import yaml
from opentowork.skill_extraction import get_resume_skills
from opentowork.skill_extraction import get_job_description_skills

print(f"\nCurrent directory: {os.getcwd()}\n")

with open("config.yml", "r", encoding='UTF-8') as config_file:
    config = yaml.safe_load(config_file)

class TestSkillExtractionResume(unittest.TestCase):
    """
    A class containing unit tests for the skill_extraction module.
    """
    def test_invalid_resume(self):
        """
        Test the skill_extraction function with an invalid file.
        """
        path = "data/pdfs/random_ds_resume.docx"
        with self.assertRaises(ValueError):
            get_resume_skills(path)

    def test_one_shot(self):
        """
        Test the skill_extraction function with a valid PDF file.
        """
        path = "data/pdfs/random_ds_resume.pdf"
        skills = get_resume_skills(path)
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
        self.assertIsInstance(skills, tuple) # edited bc function returns tuple
        self.assertGreater(len(skills), 0)
        self.assertCountEqual (skills[0], expected)

    def test_pattern_path(self):
        """
        Test skill pattern file exists.
        """
        path = config["pattern_path"]
        self.assertTrue(os.path.isfile(path))
       

class TestSkillJobDescription(unittest.TestCase):
    """
    A class containing unit tests for the skill_extraction module.
    """

    def test_one_shot(self):
        """
        Test the skill_extraction_job_description function with a valid job description.
        """
        job_description = """This is a remote position.
    Junior Data Engineer (1 year experience, remote)
    Be part of our future! This job posting builds our talent pool
    for potential future openings. We'll compare your skills and experience
    against both current and future needs. If there's a match,
    we'll contact you directly. No guarantee of immediate placement,
    and we only consider applications from US/Canada residents
    during the application process.Hiring Type: Full-TimeBase
    Salary: $56K-$70K Per Annum.Position Summary
    Join the fast-paced, innovative, and collaborative environment
    focused on providing an AIOps platform that enhances the intelligence
    of the CVS Health infrastructure.
    Work closely with subject matter experts and colleagues to
    build and scale out machine learning and AI solutions that will detect,
    predict, and recommend solutions to correct issues before system impact and
    enhance the efficiency, reliability, and performance of CVS Health's IT operations.
    Key Responsibilities include:Data pipeline development:
    Designed, implemented, and managed data pipelines for extracting,
    transforming, and loading data from various sources into data lakes
    for processing, analytics, and correlation. Data modeling:
    Create and maintain data models ensuring data quality, scalability,
    and efficiency Develop and automate processes to clean, transform,
    and prepare data for analytics, ensuring data accuracy and consistency
    Data Integration: Integrate data from disparate sources, both structured
    and unstructured to provide a unified view of key infrastructure platform
    and application data Utilize big data technologies such as Kafka
    to process and analyze large volumes of data efficiently
    Implement data security measures to protect sensitive information
    and ensure compliance with data and privacy regulation
    Create/maintain documentation for data processes, data flows,
    and system configurations Performance Optimization-
    Monitor and optimize data pipelines and systems for performance,
    scalability and cost-effectiveness Characteristics of this role:
    Team Player: Willing to teach, share knowledge, and work with others
    to make the team successful. Communication: Exceptional verbal, written,
    organizational, presentation, and communication skills.
    Creativity: Ability to take written and verbal requirements and
    come up with other innovative ideas. Attention to detail:
    Systematically and accurately research future solutions and current problems.
    Strong work ethic: The innate drive to do work extremely well.
    Passion: A drive to deliver better products and services
    than expected to customers. Required Qualifications
    2+ years of programming experience in languages such as Python, Java,
    SQL 2+ years of experience with ETL tools and database management
    (relational, non-relational) 2+ years of experience in data modeling techniques
    and tools to design efficient scalable data structures
    Skills in data quality assessment, data cleansing, and data validation
    Preferred Qualifications: Knowledge of big data technologies and
    cloud platforms Experience with technologies like PySpark, Databricks,
    and Azure Synapse. EducationBachelor's degree in Computer Science,
    Information Technology, or related field, or equivalent working experience"""
        skills = get_job_description_skills(job_description)
        expected = ['big data', 'scalability', 'design', 'azure',
                    'data quality', 'kafka', 'data structures',
                    'machine learning', 'java', 'database',
                    'data validation', 'computer science', 'languages',
                    'python', 'ai', 'data integration', 'security',
                    'sql', 'data modeling', 'analytics',
                    'documentation']
        self.assertIsInstance(job_description, str)
        self.assertIsInstance(skills, list)
        self.assertGreater(len(skills), 0)
        self.assertCountEqual (skills, expected)

    def test_pattern_path(self):
        """
        Test skill pattern file exists.
        """
        path = config["pattern_path"]
        self.assertTrue(os.path.isfile(path))

if __name__ == "__main__":
    unittest.main()
