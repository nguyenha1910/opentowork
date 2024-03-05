"""
Module initializes job scraping process and writes out results to csv file.
Depends on indeed_jobs and linkedin_jobs.
"""
import csv
import os
from datetime import datetime
from .indeed_jobs import indeed_job_listings
from .linkedin_jobs import linkedin_job_listings

def write_to_csv(data, job_title_input, pages):
    """
    Function writes inputted data to csv file with job titles, number of pages,
    and scraped time in file name.
    Args:
        data (list): list of job information to write out
        job_title_input (list): job titles used in scraping
        pages (int): number of pages scraped
    Returns:
        None
    """
    scrape_dt = datetime.now().strftime("%Y%m%d_%H%M%S")
    directory = "csvs"
    if not os.path.exists(directory):
        os.makedirs(directory)

    job_title_str = '_'.join(job_title_input).replace(' ', '_')

    filename = f"job_listings_{job_title_str}_{pages}_pages_scraped_{scrape_dt}.csv"
    csv_file = os.path.join(directory, filename)
    colnames = ["title", "company", "location", "posted date",
                "link", "description", "scraped date"]

    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=colnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    """
    Main function to initialize indeed and linkedin job scraping processes.
    Takes the scraping output lists and writes to one csv file.
    """
    job_title_input = ['data analyst']#, 'data scientist', 'data engineer'] !!testing
    pages = 1

    scraped_data = []

    for job_title in job_title_input:
        scraped_data.extend(indeed_job_listings(job_title, pages))
        scraped_data.extend(linkedin_job_listings(job_title, pages))

    write_to_csv(scraped_data, job_title_input, pages)

if __name__ == "__main__":
    main()
