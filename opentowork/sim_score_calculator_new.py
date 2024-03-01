"""
Sentence transfomer module that class the LLM model and
utilizes pytorch for cosine similairty calculation.
"""
from sentence_transformers import (SentenceTransformer, util)


def sim_calculator(job_posting, skill_set):
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
    
    # we can only include job description or make a new column including job title
    # and other info or extract keyword from job description
    job_desc = job_posting['description']
    print(f"job descrtipino {job_desc}")
    job_posting['embedding'] = model.encode([job_desc])
    #job_posting['embedding'] = job_desc.apply(lambda x: model.encode(x, convert_to_tensor=True).numpy())
    
    skill_embedding = model.encode(skill_set) 
    similarity_torch = util.pytorch_cos_sim(skill_embedding, job_posting['embedding']).tolist()[0][0]
    
    return abs(similarity_torch)
