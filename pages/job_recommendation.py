import streamlit as st
import pandas as pd
import os
from opentowork import sim_calculator

def get_latest_csv_file():
    csv_dir = os.path.join(os.path.dirname(__file__), '..', 'csvs')
    csv_files = [file for file in os.listdir(csv_dir) if file.startswith('job_listings') and file.endswith('.csv')]
    csv_files_paths = [os.path.join(csv_dir, file) for file in csv_files]
    latest_csv_file = max(csv_files_paths, key=os.path.getmtime)
    return latest_csv_file

def job_item(data, skills):
    # score = data['score']
    score = sim_calculator(data['description'], skills)
    container = st.container(border=True)
    c1, c2 = container.columns([5, 1])
    c1.subheader(data['title'])
    c1.write(data['company'])
    c1.caption(data['location'])
    c2.link_button("Apply", data['link'])
    c2.progress(score, text=f"{int(score*100)}%")
    return container

def app(skills):
    data_path = get_latest_csv_file()
    data = pd.read_csv(data_path)

    for _, row in data.iterrows():
        if not pd.isna(row['description']):
            job_item(row, skills)
        else:
            continue
            