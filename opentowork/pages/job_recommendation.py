# pylint: disable=import-error
"""
This module represents the job list of the app.
"""
import os
from pathlib import Path
import streamlit as st
import pandas as pd
from skill_extraction import get_job_description_skills
from sim_score import get_sim_score

def get_latest_csv_file():
    """
    Get the latest csv file from the csvs directory.

    Returns:
    latest_csv_file (str): The latest csv file.
    """
    parent_path = Path(__file__).resolve().parents[2]
    csv_dir = Path(parent_path, 'csvs')
    csv_files = [file for file in os.listdir(csv_dir) \
                 if file.startswith('job_listings') and file.endswith('.csv')]
    csv_files_paths = [os.path.join(csv_dir, file) for file in csv_files]
    latest_csv_file = max(csv_files_paths, key=os.path.getmtime)
    return latest_csv_file

def job_item(data, skills_jd, skills_resume, jd_content, resume_content):
    """
    Create a job item using streamlit container.

    Args:
        data (dict): The job data.
        skills_jd (list): The skills required for the job.
        skills_resume (list): The skills present in the resume.
        jd_content (str): The job description.
        resume_content (str): The resume content.
    
    Returns:
        container (streamlit.container): 
            The container containing the job item.
    """
    score = get_sim_score(jd_content, resume_content)
    job_skills_set = set(skills_jd)
    resume_skills_set = set(skills_resume)
    intersection = job_skills_set.intersection(resume_skills_set)
    skills_present_in_resume = len(intersection)
    total_skills_required = len(job_skills_set)
    container = st.container(border=True)
    col1, col2 = container.columns([5, 1])
    col1.subheader(data['title'])
    col1.write(data['company'])
    col1.caption(data['location'])
    col2.link_button("Apply", data['link'])
    col2.progress(score, text=f"{int(score*100)}%")
    col2.write(f"{skills_present_in_resume} of {total_skills_required}\
              skills are present in your resume.")
    return container

def app(skills_resume, resume_content):
    """
    The main app function of the job recommendation list.
    Args:
        skills_resume (list): The skills present in the resume.
        resume_content (str): The resume content.

    Returns:
        None
    """
    data_path = get_latest_csv_file()
    data = pd.read_csv(data_path)
    for _, row in data.iterrows():
        if not pd.isna(row['description']):
            skills_jd = get_job_description_skills(row['description'])
            jd_content = row['description']
            job_item(row, skills_jd, skills_resume, jd_content, resume_content)
        else:
            continue
