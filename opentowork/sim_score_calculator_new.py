"""
Sentence transfomer module that class the LLM model and
utilizes pytorch for cosine similairty calculation.
"""
from sentence_transformers import SentenceTransformer, util

def sim_calculator(job_posting, resume):
    """
    A function that calculates the similarity score between vector embedding of
    job description and skill set extracted from the user's resume based on the cosine similairty.
    The vector embedding is calculated by called Large Language Models.

    Args:
        job_posting (_string_): the text of job posting scraped
        resume (_string_): the text of resume content 
        #skill_set (_list of string_): the list of skill set extracted from the resume

    Returns:
        float : absolute value of similarity score calculated between two inputs
    """
    #print("job_posting:", job_posting)
    #print("resume", resume)
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L12-v2")
    job_embedding = model.encode([job_posting])
    resume_embedding = model.encode([resume])
    similarity_torch = util.pytorch_cos_sim(resume_embedding, job_embedding).tolist()[0][0]
    return abs(similarity_torch)
