import streamlit as st
import pandas as pd
import os
from opentowork import sim_calculator

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

    data_path = "csvs/job_listings_['data analyst', 'data scientist', 'data engineer']_1_pages.csv"
    data = pd.read_csv(data_path)

    for _, row in data.iterrows():
        if not pd.isna(row['description']):
            job_item(row, skills)
        else:
            continue
            