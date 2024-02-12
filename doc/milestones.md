**From the doc: Milestones**. A preliminary plan - a list of milestones,
each with a list of tasks in priority order.

1.  Resume Analyzer

    a.  Build web scraper for job listings

        i.  Success: scrapes job listing data with job description

    b.  Build skill keyword extractor

        i.  Success: extracts data science related skill keywords from
            resume (not including irrelevant keywords or missing out
            important keywords)

2.  Job Matching System

    a.  Generate Match Score: Calculate similarity score between
        extracted keyword from user and all job description from scraped
        data

        i.  Success: similarity score is generated for all job
            descriptions

3.  Create Web Interface for Job Application

    a.  Build resume PDF input interface

        i.  Success: PDF uploads as input to resume analyzer

    b.  Build matched jobs page

        i.  Success: display job postings with high matching score in
            descending order -- top 50 with pages, hyperlinks to
            third-party sites work

4.  Build Statistic Dashboard (nice to have)

    a.  Create user authentication

        i.  Success: allows secure user login with unique username and
            password

    b.  Create database for user data (including resume)

        i.  Success: able to add data to database with unique user token

    c.  Web interface for tracking job application status

        i.  Success: accurately reflects the application status data
            based on the user input

    d.  Web interface for data visualization

        i.  Success: create a chart and plots based on the accurate
            application status data & filters
