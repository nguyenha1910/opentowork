import streamlit as st
from streamlit_tags import st_tags
from pages import job_recommendation
from pathlib import Path
import os
import yaml
import PyPDF4
import fitz  # PyMuPDF library
#from sentence_transformers import (SentenceTransformer, util)
#import numpy as np
#from numpy.linalg import norm
#from statistics import mean
import spacy
import pandas as pd
import sys

config = yaml.safe_load(open("YOUR_CONFIG_FILE.yml"))
for key, value in config.items():
    if isinstance(value, str):
        config[key] = Path(value)
        if 'dir' in key:
            config[key].mkdir(parents=True, exist_ok=True)

def app():
    # Set page title and icon
    st.set_page_config(
        page_title="OpenToWork",
        page_icon="🟢",
    )
    st.title("Open To Work")    

    # Navigation bar
    nav_options = ['Home', 'Job Recommendation', 'Profile']
    selection = st.sidebar.radio("Navigation", nav_options)

    # Depending on the selection, display different content in the main area
    if selection == 'Job Recommendation':
        job_recommendation.app()

    uploaded_file = st.file_uploader(label="Upload your resume", type="pdf")
    if uploaded_file:
        save_path = Path(config['pdf_dir'], uploaded_file.name)
        with open(save_path, mode='wb') as w:
            w.write(uploaded_file.getvalue())

        # TODO: Analyze the PDF to extract skills
        skills = skill_extraction(save_path)

        if skills:
            keywords = st_tags(
                            label='### Skills:',
                            text='Press enter to add more',
                            value=skills,
                            )
            
        if st.button('See which jobs are a good fit for you'):
            job_recommendation.app()

def skill_extraction(path):
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
    return unique_skills

app()
