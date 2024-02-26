import streamlit as st
import pandas as pd
import numpy as np
import yaml
from opentowork import sim_calculator
from opentowork import skill_extraction

config = yaml.safe_load(open("config.yml"))
# Need to check with different file like job_listings_Data Scientist.csv
job_posting= pd.read_csv("job_listings_data analyst_10_pages.csv")

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

def job_item(data, skills):
    score = sim_calculator(data, skills)
    container = st.container(border=True)
    c1, c2 = container.columns([5, 1])
    c1.subheader(data['title'])
    c1.write(data['company'])
    c1.caption(data['location'])
    c2.link_button("Apply", data['link'])
    c2.progress(score, text=f"{score}%")
    return container

def app(skills):
    data = load_data(config['data_path'])

    for id, row in data.iterrows():
        job_item(row, skills)
