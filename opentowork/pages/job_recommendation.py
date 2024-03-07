import streamlit as st
import pandas as pd
import os
# from skill_extraction import get_job_description_skills
# from sim_score import get_sim_score


def get_latest_csv_file():
    csv_dir = os.path.join(os.path.dirname(__file__), '../..', 'csvs')
    print(f"csv_dir: {csv_dir}")
    csv_files = [file for file in os.listdir(csv_dir) if file.startswith('job_listings') and file.endswith('.csv')]
    csv_files_paths = [os.path.join(csv_dir, file) for file in csv_files]
    latest_csv_file = max(csv_files_paths, key=os.path.getmtime)
    return latest_csv_file

def job_item(data, skills_jd, skills_resume, jd_content, resume_content):
    score = get_sim_score(jd_content, resume_content)
    job_skills_set = set(skills_jd)
    resume_skills_set = set(skills_resume)
    intersection = job_skills_set.intersection(resume_skills_set)
    skills_present_in_resume = len(intersection)
    total_skills_required = len(job_skills_set)
    container = st.container(border=True)
    c1, c2 = container.columns([5, 1])
    c1.subheader(data['title'])
    c1.write(data['company'])
    c1.caption(data['location'])
    c2.link_button("Apply", data['link'])
    c2.progress(score, text=f"{int(score*100)}%")
    c2.write(f"{skills_present_in_resume} of {total_skills_required} skills are present in your resume.")
    return container

def app(skills_resume, resume_content):
    data_path = get_latest_csv_file()
    data = pd.read_csv(data_path)
    for _, row in data.iterrows():
        if not pd.isna(row['description']):
            skills_jd = get_job_description_skills(row['description'])
            jd_content = row['description']
            job_item(row, skills_jd, skills_resume, jd_content, resume_content)
        else:
            continue
