import streamlit as st
from streamlit_tags import st_tags
from pages import job_recommendation
from pathlib import Path
import yaml
import pandas as pd
from opentowork import skill_extraction
from opentowork import sim_calculator
import subprocess


config = yaml.safe_load(open("config.yml"))

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

    uploaded_file = st.file_uploader(label="Upload your resume", type="pdf")

    if uploaded_file:
        save_path = Path(config['pdf_dir'], uploaded_file.name)
        with open(save_path, mode='wb') as w:
            w.write(uploaded_file.getvalue())

        # TODO: Analyze the PDF to extract skills
        skills = skill_extraction(save_path)
        skills = sorted(skills)

        if skills:
            keywords = st_tags(
                            label='### Skills:',
                            text='Press enter to add more',
                            value=skills,
                            )
        else:
            keywords = st_tags(
                            label='### Skills:',
                            text='Press enter to add more',
                            value=[],
                            )

        if st.button('Update Job Posting Data'):
            subprocess.run(["python", "data/Job_Listing_Scraper.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        job_recommendation.app(skills)

app()