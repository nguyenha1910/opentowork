import PyPDF4
import fitz  # PyMuPDF library
from sentence_transformers import (SentenceTransformer, util)
import numpy as np
from numpy.linalg import norm
from statistics import mean
import spacy
import pandas as pd
import sys
import os
from datetime import datetime

nlp = spacy.load("en_core_web_lg") # python -m spacy download en_core_web_lg

# get this once the user upload their resume using streamlit button
# can make upload button and probably will be able to get the path from that
path = "./JaniceKim_Resume_DSPositions.pdf"

# read the pdf file - PyPDF4
#with open(path, 'rb') as pdfFileObj:
#    pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
    # print("Number of pages:", pdfReader.numPages)

#    extracted_resume_content_PyPDF4 = ""
#    for i in range(pdfReader.numPages):
#        pageObj = pdfReader.getPage(i)
#        extracted_resume_content_PyPDF4 += pageObj.extractText()


# read the pdf file - PyMuPDF, our final choice
with fitz.open(path) as pdf_resume:
    extracted_resume_content_PyMuPDF = ""
    for page_number in range(pdf_resume.page_count):
        page = pdf_resume[page_number]
        extracted_resume_content_PyMuPDF += page.get_text()

# print statement that checks the content
#print("extracted_resume_content_PyPDF4:", extracted_resume_content_PyMuPDF)


# needs to have this file downloaded
skills = "jz_skill_patterns.jsonl" 
# https://medium.com/@vikrantptl06/resume-parsing-using-spacy-af24376ec008
# https://github.com/kingabzpro/jobzilla_ai/blob/main/jz_skill_patterns.jsonl

ruler = nlp.add_pipe("entity_ruler", before = "ner")
ruler.from_disk(skills)
doc = nlp(extracted_resume_content_PyMuPDF)

skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"]

dict = {}
skills = []

for ent in doc.ents:
    #print(ent.label_)
    if "SKILL" in ent.label_:
        skills.append(ent.text)

# remove duplicates (capitalization)
lowercase_skills = [s.lower() for s in skills]
unique_skills = list(set(lowercase_skills))

# List of skills
#print("Extracted Skills:", unique_skills)






# find all scraped job posting csv files
csv_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
csv_files = [file for file in os.listdir(csv_dir) if file.startswith('job_listings') and file.endswith('.csv')]
csv_files_paths = [os.path.join(csv_dir, file) for file in csv_files]

# find latest scraped csv file
latest_csv_file = max(csv_files_paths, key=os.path.getmtime)
print("latest_csv_file:", latest_csv_file)

latest_scraped_dt = datetime.fromtimestamp(os.path.getmtime(latest_csv_file))
print("latest_scraped_dt:", latest_scraped_dt)




model = SentenceTransformer("sentence-transformers/all-MiniLM-L12-v2") # LLM model used for embedding calculation

# we can only include job description or make a new column including job title and other info or extract keyword from job description
job_desc = job_posting['description']
job_posting['embedding'] = job_desc.apply(lambda x: model.encode(x, convert_to_tensor=True).numpy()) # vecter embedding for job description 
np.set_printoptions(threshold=sys.maxsize) #print all embedding

skill_embedding = model.encode(unique_skills) # vector embedding for skill set

# use torch to calculate the similarity score
similarity_torch = job_posting['embedding'].apply(lambda x: util.pytorch_cos_sim(skill_embedding, x).tolist()[0][0])

# This one manually calculates the score, but it seems like it calculates each skill with job descriptions -- have a list whose length is a skill set length
# So I averaged them to calculate the similarity score in this case - but saved the whole list as well
sim_score = []
sim_score_total = []
for i in range(len(job_posting['embedding'])):
    each_job = job_posting['embedding'][i] #shape(384,)   
    similarity_score = np.dot(each_job, skill_embedding.transpose())/(norm(each_job)*norm(skill_embedding.transpose())) #transpose shape (384, 19)
    sim_score_total.append(similarity_score) 
    sim_score.append(mean(similarity_score))

job_posting['sim_manual'] = sim_score #averaged manually calculated score
job_posting['sim_manual_list'] = sim_score_total #list of similariy score for each skill
job_posting['sim_torch'] = similarity_torch #torch calculated similairy score

# output generation as csv
#job_posting.to_csv("job_posting_with_similarity.csv")

# To see if torch calculates it alright, I just used the whole job description and one job description to check similarity score
sanity_check = job_posting['embedding'].apply(lambda x: util.pytorch_cos_sim(job_posting['embedding'][3], x).tolist()[0][0])
#print(sanity_check) #provides similairty score of 1 for itself, so it works properly
sanity_check = pd.DataFrame(sanity_check)
#sanity_check.to_csv("job_posting_check.csv")