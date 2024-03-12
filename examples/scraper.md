## Web Scraping Scripts
The opentowork application uses job listings scraped from LinkedIn and Indeed. This document goes over how to run and maintain the scraping scripts found [here](../opentowork/scraper/).

### Requirements
The web scraper uses Selenium and BeautifulSoup4. Both are included in the environment.yml file. Selenium additionally requires both Google Chrome and Chromedriver - installation instructions can be found [here](../README.md#data)

### How it Works
The scripts access LinkedIn/Indeed job searches for a job title and scrape details for a specified number of jobs by looking for certain HTML tags on each site. It then exports the job listings to a csv file, stored in data/csv.

**Note that if the site changes its layout, the scraping script will need to be updated to accurately find job details. We cannot guarantee that the script works all the time and will continue to work in the future.

### How to Run It
The web scraping process can be triggered through the app's "Update Job Posting Data" button or by running a command locally:

```bash
conda activate opentowork
python -m opentowork.scraper.job_listing_scraper
```
The scraping process can take anywhere from 10-30 minutes once triggered.

If the web scraper is unable to scrape any job data, a message will appear on the app and the terminal.

### How to Customize It
The default job titles included when scraping for jobs are data analyst, data scientist, and data engineer. The default total number of jobs scraped is set to 30 job listings. These options can be customized either in [opentowork/app.py](../opentowork/app.py) or [opentowork/scraper/job_listing_scraper.py](../opentowork/scraper/job_listing_scraper.py). Code snippets are shown below.

In [opentowork/app.py](../opentowork/app.py):
Specify a list of job titles (as strings) to scrape for when calling job_listing_scraper.main(). Input specified total number as integer.
```python
# in app.py
if update_job_button:
    try:
        job_listing_scraper.main(job_titles = ['cat', 'dog', 'rabbit'], total_job_count = 20)
```
In [opentowork/scraper/job_listing_scraper.py](../opentowork/scraper/job_listing_scraper.py):
Change the defaults in the main() function. Job title input is in the body of the function, total job count is in the function definition. Job titles need to be a list of strings and total job count needs to be an integer.
```python
# in the main() function
def main(job_titles = None, total_job_count = 30):
    if job_titles is None:
        job_titles = ['data analyst', 'data scientist', 'data engineer']
```
### Future Updates
Due to the unstable nature of web scraping, we plan to add functionality allowing users to input specific job links and/or job descriptions for comparison with resumes in the future. This will allow users to enjoy the main functionality of opentowork regardless of scraper performance.