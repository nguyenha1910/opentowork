from pathlib import Path
import subprocess
import yaml
import streamlit as st
from streamlit_tags import st_tags
from pages import job_recommendation
import pandas as pd
from opentowork import skill_extraction_resume
from opentowork import sim_calculator


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
        skills_resume = skill_extraction_resume(save_path)

        if skills_resume:
            keywords = st_tags(
                            label='### Skills:',
                            text='Press enter to add more',
                            value=skills_resume,
                            )
        else:
            keywords = st_tags(
                            label='### Skills:',
                            text='Press enter to add more',
                            value=[],
                            )

        if st.button('Update Job Posting Data'):
            subprocess.run(["python", "data/job_listing_scraper.py"])

        job_recommendation.app(skills_resume)

app()
