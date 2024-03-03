import csv
from datetime import datetime
from data.indeed_jobs import indeed_job_listings
from data.linkedin_jobs import linkedin_job_listings

def write_to_csv(data, job_title_input, pages):
    scrape_dt = str(datetime.now())
    csv_file = f"job_listings_{job_title_input}_{pages}_pages_scraped_{scrape_dt}.csv"
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
        try:
            indeed = indeed_job_listings(job_title, pages)
        except:
            print("Error occurred with Indeed scraping")
            indeed = []
        try:
            linkedin = linkedin_job_listings(job_title, pages)
        except:
            print("Error occurred with LinkedIn scraping")
            linkedin = []
        scraped_data = scraped_data + indeed + linkedin
    write_to_csv(scraped_data, job_title_input, pages)

if __name__ == "__main__":
    main()
