# pylint: disable=import-error
# pylint runs from a different place than deployed app
# pylint: disable=broad-exception-caught
"""
This module represents the home page of the app.
"""
import os
from pathlib import Path
import yaml
import streamlit as st
from streamlit_tags import st_tags
import pandas as pd
import fitz
from opentowork.skill_extraction import get_resume_skills
from opentowork.scraper import job_listing_scraper
from opentowork.pages.job_recommendation import get_latest_csv_file
from opentowork.pages.job_recommendation import app as job_recommendation_app

# Load config file
with open("config.yml", "r", encoding='UTF-8') as config_file:
    config = yaml.safe_load(config_file)

for key, value in config.items():
    if isinstance(value, str):
        config[key] = Path(value)
        if 'dir' in key:
            config[key].mkdir(parents=True, exist_ok=True)

def app():
    """
    This function represents the home page of the app.
    """

    # Set page title and icon
    st.set_page_config(
        page_title="OpenToWork",
        page_icon="🟢",
        initial_sidebar_state="collapsed"
    )
    st.title("Open To Work")

    uploaded_file = st.file_uploader(label="Upload your resume", type="pdf")

    if uploaded_file:
        save_path = Path(config['pdf_dir'], uploaded_file.name)
        if save_path.exists():
            base_name, extension = os.path.splitext(save_path)
            counter = 1
            while True:
                new_file_path = f"{base_name} ({counter}){extension}"
                if not os.path.exists(new_file_path):
                    os.rename(save_path, new_file_path)
                    break
                counter += 1
            save_path = new_file_path
        with open(save_path, mode='wb') as resume_file:
            resume_file.write(uploaded_file.getvalue())
        try:
            skills_resume, resume_content = get_resume_skills(save_path)
        except fitz.EmptyFileError:
            st.error("Please upload non-empty PDF file.")

        st_tags_component = st_tags(
            label='### Skills:',
            text='Press enter to add more',
            value=skills_resume,
            key='skills_resume'
        )
        skills_resume = st_tags_component # to change resume skill list dynamically

        update_job_button = st.button('Update Job Posting Data')
        if update_job_button:
            try:
                job_listing_scraper.main()
                st.session_state.pop('job_loaded')
            except Exception as exception:
                st.error(f"An unexpected error occurred: {str(exception)}")

        _, last_scraped_dt = get_latest_csv_file()
        st.write(f"Job postings last updated: {last_scraped_dt}")

        with st.expander("See Applied Jobs"):
            if 'status' in st.session_state and st.session_state['status']:
                status_df = pd.read_csv(config['status_csv_path'])
                status_df = status_df.drop_duplicates(
                    ['Company Name', 'Position Title','Location', 'Status'])
            else:
                status_df = pd.DataFrame(
                        columns= ['Company Name', 'Position Title','Location', 'Status', 'Date'])
                status_df.to_csv(config['status_csv_path'], header=True, index=False)
            st.dataframe(status_df)

        if 'job_loaded' in st.session_state and st.session_state['job_loaded']:
            st.success("Job list has been loaded and sorted by match score.")
        job_recommendation_app(skills_resume, resume_content)

app()
