"""
This module represents the home page of the app.
"""
from pathlib import Path
import subprocess
import yaml
import streamlit as st
from streamlit_tags import st_tags
from pages import job_recommendation
from opentowork import skill_extraction_resume

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
    )
    st.title("Open To Work")

    uploaded_file = st.file_uploader(label="Upload your resume", type="pdf")
    if uploaded_file:
        save_path = Path(config['pdf_dir'], uploaded_file.name)
        with open(save_path, mode='wb') as resume_file:
            resume_file.write(uploaded_file.getvalue())
        skills_resume = skill_extraction_resume(save_path)

        st_tags(
            label='### Skills:',
            text='Press enter to add more',
            value=skills_resume,
        )

        if st.button('Update Job Posting Data'):
            subprocess.run(["python", "-m", "opentowork.scraper.job_listing_scraper"],check=True)
            #subprocess.run(["python", "opentowork/scraper/job_listing_scraper.py"],check=True)

        job_recommendation.app(skills_resume)

app()
