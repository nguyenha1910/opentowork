# pylint: disable=import-error
# pylint: disable=too-many-arguments
# pylint runs from a different place than deployed app
"""
This module represents the job list of the app.
"""
import os
from pathlib import Path
from datetime import datetime
import streamlit as st
import pandas as pd
from opentowork.skill_extraction import get_job_description_skills
from opentowork.sim_score import get_sim_score

def get_latest_csv_file():
    """
    Get the latest csv file from the csvs directory.

    Returns:
    latest_csv_file (str): The latest csv file.
    """
    parent_path = Path(__file__).resolve().parents[2]
    csv_dir = Path(parent_path, 'data', 'csvs')
    csv_files = [file for file in os.listdir(csv_dir) \
                 if file.startswith('job_listings') and file.endswith('.csv')]

    if len(csv_files) != 0:
        csv_files_paths = [os.path.join(csv_dir, file) for file in csv_files]
        latest_csv_file = max(csv_files_paths, key=os.path.getmtime)

        last_modified_timestamp = os.path.getmtime(latest_csv_file)
        last_scraped_dt = datetime.fromtimestamp(last_modified_timestamp)
        last_scraped_dt = last_scraped_dt.strftime("%a %b %d %Y %H:%M:%S")
    else:
        latest_csv_file = None
        last_scraped_dt = "no csv found in csvs folder"

    return latest_csv_file, last_scraped_dt


def job_item(data, skills_jd, skills_resume, jd_content, resume_content, key):
    """
    Create a job item using streamlit container.

    Args:
        data (dict): The job data.
        skills_jd (list): The skills required for the job.
        skills_resume (list): The skills present in the resume.
        jd_content (str): The job description.
        resume_content (str): The resume content.
        key(integer): key to update job application status

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
    col1.markdown(f"[Apply through company site]({data['link']})")
    col2.button('Applied?', on_click = status_update, args = (data,),key=key)
    col2.progress(score, text=f"{int(score*100)}%")
    col2.write(f"{skills_present_in_resume} of {total_skills_required}\
              skills are present in your resume.")
    return container

app_status = pd.DataFrame(columns= ['Company Name', 'Position Title',
                                    'Location', 'Status', 'Date'])
def status_update(data):
    """
    The main app that creates and updates job application
    Args:
        data (dataframe): job information

    Returns:
        dataframe: updated job application info
    """
    st.toast("You Applied! Congrats")
    new_app = [{'Company Name': data['company'],
                'Position Title': data['title'], 
                'Location': data['location'], 
                'Status': 'Applied', 
                'Date' : datetime.now()}]
    global app_status
    app_status = pd.concat([app_status, pd.DataFrame(new_app)], ignore_index=True)
    app_status = app_status.drop_duplicates(
        ['Company Name', 'Position Title', 'Location', 'Status']
        )
    app_status.to_csv(
        r'data\csvs\app_status.csv', 
        index = None, header=True
        )
    return app_status

def app(skills_resume, resume_content):
    """
    The main app function of the job recommendation list.
    Args:
        skills_resume (list): The skills present in the resume.
        resume_content (str): The resume content.

    Returns:
        None
    """
    data_path, _ = get_latest_csv_file()

    if data_path is not None:
        data = pd.read_csv(data_path)

        if len(data.dropna()) <= 1:
            st.write("Oops, no jobs were found. Please try again. 🥺")

        for idx, row in data.iterrows():
            if not pd.isna(row['description']):
                skills_jd = get_job_description_skills(row['description'])
                jd_content = row['description']
                job_item(row, skills_jd, skills_resume, jd_content, resume_content, idx)
            else:
                continue
    else:
        st.write("Oops, no jobs were found. Please try again. 🥺")
