from sentence_transformers import (SentenceTransformer, util)
import numpy as np
from numpy.linalg import norm
from statistics import mean
import pandas as pd

def sim_calculator(job_posting, skill_set):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L12-v2")
    # we can only include job description or make a new column including job title and other info or extract keyword from job description
    job_desc = job_posting['description']
    print(f"job descrtipino {job_desc}")
    job_posting['embedding'] = model.encode([job_desc])
    #job_posting['embedding'] = job_desc.apply(lambda x: model.encode(x, convert_to_tensor=True).numpy()) # vecter embedding for job description 
    
    skill_embedding = model.encode(skill_set) 

    # use torch to calculate the similarity score
    similarity_torch = util.pytorch_cos_sim(skill_embedding, job_posting['embedding']).tolist()[0][0]
    
    return abs(similarity_torch)
