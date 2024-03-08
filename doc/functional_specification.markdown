Background: Make job searching easier! Allow users to see jobs that
match their skills.

User Profiles:

-   User 1: Bob

    -   Bob is a job seeker.

    -   Bob needs to analyze his resume, match currently open jobs with
        his experience, see recommendations, and track application
        status.

    -   Bob wants to be up-to-date and get notification on jobs that
        match his profile.

    -   Bob values accuracy.

    -   Bob prefers easy-to-understand visuals and a simple interface.

-   User 2: Jane

    -   Jane is the technician of the web application.

    -   Jane needs access to the back end.

    -   Jane wants to update the model, codebase, and test the app.

    -   Jane needs to monitor the app and ensure that all features work
        properly.

    -   Jane has high-tech skills, and Jane wants a fast and efficient
        interface.

Data Sources: The two main sources are the uploaded resumes and the
scraped job postings.

-   Resumes

    -   Uploaded in pdf format

    -   Extracted text is used to match with job postings

-   Job Postings

    -   Scraped from LinkedIn and Indeed to a csv

    -   Text from descriptions is used to match with resumes

Use Cases:

-   Apply to Matching Jobs (Bob)

    -   Objective: view jobs that match resume and apply on third-party
        site

    -   Expected Interactions:

        -   User: upload resume

        -   System: analyze skills

        -   System: displays list of jobs with match score

        -   Implicit user usage:

            -   Check how much resume fits to the targeted job position

            -   Check job posting trending -- how many jobs posted
                recently

        -   User: click link to job posting

        -   System: redirect user to job posting on third-party site

-   Access Model Accuracy (Jane)

    -   Objectives

    -   Interactions:

        -   User: Open log file

        -   System:

            -   Display the model accuracy

            -   Display the bug log -- involves command line
