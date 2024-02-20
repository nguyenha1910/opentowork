import streamlit as st
import pandas as pd
import numpy as np
import yaml

config = yaml.safe_load(open("config.yml"))

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

def job_item(data):
    score = np.random.randint(0, 100)
    container = st.container(border=True)
    c1, c2 = container.columns([5, 1])
    c1.subheader(data['title'])
    c1.write(data['company'])
    c1.caption(data['location'])
    c2.link_button("Apply", data['link'])
    c2.progress(score, text=f"{score}%")
    return container

def app():
    data = load_data(config['data_path'])

    for id, row in data.iterrows():
        job_item(row)
