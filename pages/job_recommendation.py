import streamlit as st
import pandas as pd
import os
from opentowork import skill_extraction_job_description
from opentowork import sim_calculator
from datetime import datetime
global app_status
app_status=pd.DataFrame(columns=['Company Name', 'Position Title', 'Location', 'Status', 'Date']) # link url in position title or can have sepearate 'url' column 
def get_latest_csv_file():
    csv_dir = os.path.join(os.path.dirname(__file__), '..', 'csvs')
    csv_files = [file for file in os.listdir(csv_dir) if file.startswith('job_listings') and file.endswith('.csv')]
    csv_files_paths = [os.path.join(csv_dir, file) for file in csv_files]
    latest_csv_file = max(csv_files_paths, key=os.path.getmtime)
    return latest_csv_file

def job_item(data, skills_jd, skills_resume, jd_content, resume_content, key):
    # score = data['score']
    #skills_resume = sorted(skills_resume)
    #skills_jd = sorted(skills_jd)
    score = sim_calculator(jd_content, resume_content)

    job_skills_set = set(skills_jd)
    resume_skills_set = set(skills_resume)
    intersection = job_skills_set.intersection(resume_skills_set)
    skills_present_in_resume = len(intersection)
    total_skills_required = len(job_skills_set)

    container = st.container(border=True)
    c1, c2 = container.columns([5, 1])
    c1.subheader(data['title'])
    c1.write(data['company'])
    c1.caption(data['location'])
    #if c2.link_button("Apply", data['link']):
    c2.button('applied?', on_click = status_update, args = (data,),key=key)
    c2.progress(score, text=f"{int(score*100)}%")
    c2.write(f"{skills_present_in_resume} of {total_skills_required} skills are present in your resume.")
    return container

def status_update(data): 
    global app_status

    st.toast("You Applied! Congrats")
    new_app = [{'Company Name': data['company'], 'Position Title': data['title'], 'Location': data['location'], 'Status': 'Applied', 'Date' : datetime.now()}]
    app_status = pd.concat([app_status, pd.DataFrame(new_app)], ignore_index=True)
    app_status = app_status.drop_duplicates(['Company Name', 'Position Title', 'Location', 'Status'])
    app_status.to_csv(r'C:\Users\user\Desktop\GitHub\opentowork\app_status.csv', index = None, header=True) 

    return app_status
#initiate data frame


    # alternative dropdown list for 'Status' cell but not sure if this works just proposing
    # https://docs.streamlit.io/library/api-reference/data/st.dataframe -- lots of options here!
    #    status = (‘Applied’, ‘Reject’, ‘Interview’, 'Offer')
    #    gb.configure_column('Status', editable=True, cellEditor=‘agSelectCellEditor’, cellEditorParams={‘values’: dropdownlst })
    
# in separate page, we can do this
# st.dataframe(app_status, hide_index= True)

        
def app(skills_resume, resume_content):
    data_path = get_latest_csv_file()
    data = pd.read_csv(data_path)
    for idx, row in data.iterrows():
        if not pd.isna(row['description']):
            skills_jd = skill_extraction_job_description(row['description'])
            jd_content = row['description']
            job_item(row, skills_jd, skills_resume, jd_content, resume_content,idx)
        else:
            continue


            