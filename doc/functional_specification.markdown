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

-   Update Job Titles to Scrape (Jane)

    -   Objective: update default job titles to use when updating job listing data

    -   Interactions:

        -   User: Refer to examples/scraper.md for instructions

        -   User: Navigate to opentowork/app.py or opentowork/scraper/job_listing_scraper.py to update job titles

        -   System: Saves updated defaults for use with update jobs button 

        -   User: Tests update button on frontend to make sure changes are reflected

        -   System: Runs job listing scraper script and outputs updated jobs to frontend

        -   User: Verifies that functions work as designed
