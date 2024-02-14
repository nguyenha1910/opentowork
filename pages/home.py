import streamlit as st
from pages import job_recommendation

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

    uploaded_file = st.file_uploader("Upload your resume", type="pdf")
    if uploaded_file is not None:
        pass

app()
