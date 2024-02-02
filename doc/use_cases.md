**Bob**
- Upload Resume 
    - User: upload resume 
    - System: Analyze skills  
    - System: Check if authenticated 
        - If yes 
            - Add skills to profile 
            - Extract working experience and add to profile  
            - Display visualization 
        - If no 
            - Only display stat visualization 
- View Application 
    - User: access profile page 
    - System: display application stage information 
- View Job Posting 
    - User: view a job post, keywords 
    - System: Show job post 
        - Implicit user usage 
            - Check how much resume fits to the targeted job position 
            - Check job posting trending – how many jobs posted recently 
    - System: Display stat visualization  
    - System: Ask if user applied to the job 
    - User: Select ‘yes’ or ‘no’ 
    - System: 
        - If yes, add the job to user’s job list & change status to ‘Applied’ 
        - If no, do nothing 
- Provide feedback 
    - User: Information on whether they got the job 
    - System: Provide job match statistics 

**Alice**
- Access Recruiter Landing Page 
    - User: Access authentication page  
    - System: Enter authentication code (receive it when they authenticate it using company email) 
    - User: enter authentication code 
    - System: (if correct) shows their job posting status page 
- Create Job Posting 
    - User: access recruiter landing page 
    - System: display “create job posting” button 
    - User: click “create job posting” button 
    - System: display job posting creation page/pop-up 
    - User: enter or upload job details 
    - System: validate job details (has all necessary components like job title, experience level, job type, skills, etc.) 
        - If valid: allow creation of posting 
        - If not valid: prompt user to make changes 
    - System: redirect back to landing page and display created job posting 

**Jane** 
- Access Model Accuracy and user statistics 
    - User: Access statistics page  
    - System: Display the statistics page 
    - User: Select what info they want to check 
    - System: 
        - Display the recommendation model accuracy 
        - Display the user statistics 
        - Display the bug log – involves command line 
- Review feedback 
    - User: Access feedback page 
    - System: Display feedback 

 

 