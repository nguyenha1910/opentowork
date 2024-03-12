## Web Scraping Scripts
The opentowork application uses job listings scraped from LinkedIn and Indeed. This document goes over how to run and maintain the scraping scripts found [here](../opentowork/scraper/).

### Requirements
The web scraper uses Selenium and BeautifulSoup4. Both are included in the environment.yml file. Selenium additionally requires both Google Chrome and Chromedriver - installation instructions can be found [here](../README.md#data)

### How it Works
The scripts access LinkedIn/Indeed job searches for a job title and scrape details for a specified number of jobs by looking for certain tags on each site. It then exports the job listings to a csv file, stored in data/csv.

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
By default,

### Future Updates
Due to the unstable nature of web scraping, we plan to add functionality allowing users to input specific job links and/or job descriptions for comparison with resumes. This will allow users to enjoy the main functionality of opentowork regardless of scraper performance.