from pathlib import Path
import yaml
import pandas as pd

import streamlit as st
from streamlit_tags import st_tags
from pages import job_recommendation
from opentowork import skill_extraction

config = yaml.safe_load(open("config.yml"))
job_posting= pd.read_csv("job_listings_data analyst_10_pages.csv")

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

        skills = skill_extraction(save_path)
        if skills:
            keywords = st_tags(
                            label='### Skills:',
                            text='Press enter to add more',
                            value=skills,
                            )
            
            job_recommendation.app(skills)
app()
