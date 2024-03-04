"""
Sentence transfomer module that class the LLM model and
utilizes pytorch for cosine similairty calculation.
"""
from sentence_transformers import (SentenceTransformer, util)
import numpy as np
from numpy.linalg import norm
from statistics import mean
import pandas as pd

def sim_calculator(job_posting_skills, resume_skills):
    """
    A function that calculates the similarity score between vector embedding of
    job description and skill set extracted from the user's resume based on the cosine similairty.
    The vector embedding is calculated by called Large Language Models.

    Args:
        job_posting (_string_): the text of job posting scraped
        skill_set (_list of string_): the list of skill set extracted from the resume

    Returns:
        float : absolute value of similarity score calculated between two inputs
    """
    
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L12-v2")
    job_embedding = model.encode([job_posting_skills])
    skill_embedding = model.encode(resume_skills)
    similarity_torch = util.pytorch_cos_sim(skill_embedding, job_embedding).tolist()[0][0]
    return abs(similarity_torch)
