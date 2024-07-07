# pylint: disable=too-many-arguments
# disabled due to all arguments necessary (6/5)

"""
This module represents the job list of the app.
"""
import os
from pathlib import Path
from datetime import datetime
import streamlit as st
import pandas as pd
import yaml
from opentowork.skill_extraction import get_job_description_skills
from opentowork.model.sim_score import get_sim_score

with open("config.yml", "r", encoding='UTF-8') as config_file:
    config = yaml.safe_load(config_file)

def get_latest_csv_file():
    """
    Get the latest csv file from the csvs directory.

    Returns:
    latest_csv_file (str): The latest csv file.
    """
    parent_path = Path(__file__).resolve().parents[2]
    csv_dir = Path(parent_path, 'data', 'csvs')
    csv_files = [file for file in os.listdir(csv_dir) \
                 if file.startswith('job_listings') and file.endswith('.csv')
                 and not file.endswith('_temp.csv')]

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


def get_temp_path(data_path):
    """
    Function creates the temp path for sorting using the latest csv path
    Args:
        data_path (str): path of data csv file
    Returns:
        temp_data_path (str): path of temp data file
    """
    directory, filename = os.path.split(data_path)
    name, extension = os.path.splitext(filename)
    temp_name = f"{name}_temp{extension}"
    temp_data_path = os.path.join(directory, temp_name)
    return temp_data_path

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
    if 'job_loaded' in st.session_state and st.session_state['job_loaded']:
        score = data['score']
    else:
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
    col1.button('I applied!', on_click = status_update, args = (data,),key=key)
    col2.link_button("Apply", data['link'])
    col2.progress(score, text=f"{int(score*100)}%")
    col2.write(f"{skills_present_in_resume} of {total_skills_required}\
              skills are present in your resume.")
    return score

def status_update(data):
    """
    The main app that creates and updates job application
    Args:
        data (dataframe): job information

    Returns:
        dataframe: updated job application info
    """

    st.session_state['status'] = True
    st.toast("You Applied! Congrats")
    new_app = pd.DataFrame([{'Company Name': data['company'],
                'Position Title': data['title'],
                'Location': data['location'],
                'Status': 'Applied',
                'Date' : datetime.now()}])
    new_app.to_csv(
        config['status_csv_path'],
        index = None, mode='a', header=False
        )
    return new_app

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
    # Get temp data path
    temp_data_path = get_temp_path(data_path)

    if data_path is not None:
        data = pd.read_csv(data_path)

        if len(data.dropna()) <= 1:
            st.write("Oops, no jobs were found. Please try again. 🥺")

        if 'job_loaded' not in st.session_state or st.session_state['job_loaded'] is False:
            if os.path.exists(temp_data_path):
                os.remove(temp_data_path)
            scores = []
            progress_text = "Loading data"
            progress_bar = st.progress(0, text=progress_text)
            data_length = len(data.index)
            for idx, row in data.iterrows():
                if not pd.isna(row['description']):
                    progress_bar.progress(idx/data_length, text=progress_text)
                    skills_jd = get_job_description_skills(row['description'])
                    jd_content = row['description']
                    score = job_item(
                        row, skills_jd, skills_resume, jd_content, resume_content, idx
                        )
                    scores.append(score)
                else:
                    scores.append(0)

            #Save temporary data with the score
            data['score'] = scores
            sorted_data = data.sort_values(by='score', ascending=False)
            sorted_data.to_csv(temp_data_path)

            progress_bar.progress(1.0, text='Done loading data')
            st.session_state['job_loaded'] = True

        elif 'job_loaded' in st.session_state and st.session_state['job_loaded']:
            sorted_data = pd.read_csv(temp_data_path)
            for idx, row in sorted_data.iterrows():
                if not pd.isna(row['description']):
                    skills_jd = get_job_description_skills(row['description'])
                    jd_content = row['description']
                    score = job_item(
                        row, skills_jd, skills_resume, jd_content, resume_content, idx
                        )
            st.session_state['job_loaded'] = True

    else:
        st.write("Oops, no jobs were found. Please try again. 🥺")
