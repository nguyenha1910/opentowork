from sentence_transformers import (SentenceTransformer, util)
import numpy as np
from numpy.linalg import norm
from statistics import mean
import pandas as pd

def sim_calculator(job_posting, skill_set):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L12-v2")
    job_embedding = model.encode([job_posting])
    skill_embedding = model.encode(skill_set)
    similarity_torch = util.pytorch_cos_sim(skill_embedding, job_embedding).tolist()[0][0]
    return abs(similarity_torch)