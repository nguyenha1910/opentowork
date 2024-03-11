# opentowork
[![build_test](https://github.com/nguyenha1910/opentowork/actions/workflows/build_test.yml/badge.svg)](https://github.com/nguyenha1910/opentowork/actions/workflows/build_test.yml)
[![Coverage Status](https://coveralls.io/repos/github/nguyenha1910/opentowork/badge.svg?branch=main)](https://coveralls.io/github/nguyenha1910/opentowork?branch=main)


### Introduction
This repository hosts a comprehensive tool that helps job seekers in streamlining their job search process. The tool comprises a web application and data loader designed to provide job posting recommendations based on resume analysis, similarity scoring, and application status tracking.


| Team Member  | GitHub                                   |
|------------------|--------------------------------------|
| Nguyen Ha         | [nguyenha1910](https://github.com/nguyenha1910)    |
| Kelly Wang       | [kellyzwang](https://github.com/kellyzwang)  |
| Elaine Zhang     | [ezhang17](https://github.com/ezhang17)|
| Janice Kim      | [ymkim814](https://github.com/ymkim814)|

### Key Features
* Web Scraper​: collects data science related job posting data from LinkedIn and Indeed.

* Resume/Job Description Skill Analyzer​: leverages spaCy's Named Entity Recognition (NER) and Entity Ruler, combined with a JSON file containing data-related skills, to extract skill keywords from resumes and job descriptions.

* Match Score Generator​: calculates a similarity score between each job posting and the user's resume using sentence embeddings generated by the SentenceTransformer library.

* Web App Interface: enables users to upload resumes, add or delete skills, and view job listings with match percentages and the presence of skills. Users can trigger the web scraper for updates and track application status.

### Directory Summary
**data**: All data used is accessible from the data folder. The job_listing_scraper.py writes out job posting data from LinkedIn and Indeed to a CSV file in the csvs folder. The pdfs folder stores resume PDFs uploaded by the user.

**doc**: Documentation for the project is found in this folder. This includes the files such as technology review presentation, component design, functional specification, and user stories.

**examples**: This folder contains documentation for the process of setting up, scraping data, and running the web app. A tutorial and a demo are also included.

**opentowork**: All python modules used in the project directory are found in this folder. Unit tests are also included for testable modules.

### Directory Structure
```
.
├── .github/workflows
|   └── build_test.yml
├── data
|   └── csvs
|       └── ...
|   └── pdfs
|       └── random_ds_resume.docx
|       └── random_ds_resume.pdf
|   └── jz_skill_patterns.jsonl
├── doc
|   └── DATA515 Technology Reviews.pptx
|   └── component_design.md
|   └── functional_specification.markdown
|   └── interaction_diagram.png
|   └── milestones.md
|   └── user_stories.md
├── examples
|   └── README.md
├── opentowork
|   └── pages
|       └── __init__.py
|       └── job_recommendation.py
|   └── scraper
|       └── __init__.py
|       └── get_jobs.py
|       └── job_listing_scraper.py
|   └── tests
|       └── __init__.py
|       └── test_get_jobs.py
|       └── test_scraper.py
|       └── test_sim_score.py
|       └── test_skill_extraction.py
|       └── test_streamlit.py
|   └── __init__.py
|   └── app.py
|   └── sim_score.py
|   └── skill_extraction.py
├── .coveragerc
├── .gitignore
├── LICENSE
├── README.md
├── config.yml
├── environment.yml
├── pyproject.toml
└── requirements.txt
```
