# pylint: disable=import-error
# pylint runs from a different place than deployed app
# pylint: disable=broad-exception-caught
"""
This module represents the home page of the app.
"""
import os
from pathlib import Path
# import subprocess
import yaml
import streamlit as st
from streamlit_tags import st_tags
import skill_extraction
from scraper import job_listing_scraper
# from opentowork import skill_extraction
# from opentowork.pages import job_recommendation
from pages import job_recommendation

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
        skills_resume, resume_content = skill_extraction.get_resume_skills(save_path)

        st_tags(
            label='### Skills:',
            text='Press enter to add more',
            value=skills_resume,
        )

        if st.button('Update Job Posting Data'):
            try:
                job_listing_scraper.main()
                # subprocess.run(["python", "-m", "scraper.job_listing_scraper"], check=True)
            # except subprocess.CalledProcessError as e:
            #     st.error("Error occurred:")
            #     st.error(f"Subprocess error output: {e.output}")
            #     st.error(f"Subprocess return code: {e.returncode}")
            except Exception as exception:
                st.error(f"An unexpected error occurred: {str(exception)}")
        job_recommendation.app(skills_resume, resume_content)

app()
