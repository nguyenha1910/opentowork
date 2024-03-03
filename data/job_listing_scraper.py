import csv
import os
from datetime import datetime
from indeed_jobs import indeed_job_listings
from linkedin_jobs import linkedin_job_listings

def write_to_csv(data, job_title_input, pages):
    scrape_dt = str(datetime.now())
    directory = "csvs"
    if not os.path.exists(directory):
        os.makedirs(directory)
    csv_file = os.path.join(directory, f"job_listings_{job_title_input}_{pages}_pages_scraped_{scrape_dt}.csv")
    colnames = ["title", "company", "location", "posted date", 
                "link", "description", "scraped date"]

    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=colnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    job_title_input = ['data analyst', 'data scientist', 'data engineer']
    pages = 1

    scraped_data = []

    for job_title in job_title_input:
        #scraped_data = scraped_data 
        #+ scrape_indeed_job_listings(job_title, pages) 
        #+ scrape_linkedin_job_listings(job_title, pages)
        scraped_data.extend(indeed_job_listings(job_title, pages))
        scraped_data.extend(linkedin_job_listings(job_title, pages))

    write_to_csv(scraped_data, job_title_input, pages)

if __name__ == "__main__":
    main()