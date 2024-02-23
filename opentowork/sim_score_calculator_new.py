from sentence_transformers import (SentenceTransformer, util)
import numpy as np
from numpy.linalg import norm
from statistics import mean
import pandas as pd

# does not work when I did Data Scientist.csv?????????????????????????
job_posting= pd.read_csv("job_listings_data analyst_10_pages.csv")
skill = ['python', 'tableau', 'excel'] # placeholder Idont know if I should call extraction.. and how to!

def sim_calculator(job_posting, skill_set):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L12-v2")
    # we can only include job description or make a new column including job title and other info or extract keyword from job description
    job_desc = job_posting['description']
    job_posting['embedding'] = job_desc.apply(lambda x: model.encode(x, convert_to_tensor=True).numpy()) # vecter embedding for job description 
    skill_embedding = model.encode(skill_set) 

    # use torch to calculate the similarity score
    similarity_torch = job_posting['embedding'].apply(lambda x: util.pytorch_cos_sim(skill_embedding, x).tolist()[0][0])
    print('done')
    return similarity_torch

sim_score_test = sim_calculator(job_posting, skill)
"""
When we generate an output as csv
"""
# output generation as csv
#job_posting['sim_torch'] = similarity_torch #torch calculated similairy score
#job_posting.to_csv("job_posting_with_similarity.csv")

"""
Sanity Check - run the similarity score on the same data set (job desc)
"""
# To see if torch calculates it alright, I just used the whole job description and one job description to check similarity score
# sanity_check = job_posting['embedding'].apply(lambda x: util.pytorch_cos_sim(job_posting['embedding'][3], x).tolist()[0][0])
#print(sanity_check) #provides similairty score of 1 for itself, so it works properly
#sanity_check = pd.DataFrame(sanity_check)
#sanity_check.to_csv("job_posting_check.csv")

"""
Calculate the similarity score manually
"""
# This one manually calculates the score, but it seems like it calculates each skill with job descriptions -- have a list whose length is a skill set length
# So I averaged them to calculate the similarity score in this case - but saved the whole list as well
# sim_score = []
# sim_score_total = []
#for i in range(len(job_posting['embedding'])):
#    each_job = job_posting['embedding'][i] #shape(384,)   
#    similarity_score = np.dot(each_job, skill_embedding.transpose())/(norm(each_job)*norm(skill_embedding.transpose())) #transpose shape (384, 19)
#    sim_score_total.append(similarity_score) 
#    sim_score.append(mean(similarity_score))

#job_posting['sim_manual'] = sim_score #averaged manually calculated score
#job_posting['sim_manual_list'] = sim_score_total #list of similariy score for each skill