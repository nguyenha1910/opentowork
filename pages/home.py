import streamlit as st
from streamlit_tags import st_tags
from pages import job_recommendation
from pathlib import Path
import os
import yaml

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
        skills = ['Python', 'SQL', 'Machine Learning', 'Data Analysis']

        if skills:
            keywords = st_tags(
                            label='### Skills:',
                            text='Press enter to add more',
                            value=skills,
                            )
            
        if st.button('See which jobs are a good fit for you'):
            job_recommendation.app()

        

app()
