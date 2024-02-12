import csv
from Indeed_Jobs import scrape_indeed_job_listings
from Linkedin_Jobs import scrape_linkedin_job_listings

def write_to_csv(data, job_title_input, pages):
	csv_file = f"job_listings_{job_title_input}_{pages}_pages.csv"
	colnames = ["title", "company", "location","posted date", "link", "description", "scraped date"]

	with open(csv_file, "w", newline="", encoding="utf-8") as file:
		writer = csv.DictWriter(file, fieldnames=colnames)
		writer.writeheader()
		writer.writerows(data)
	

def main(job_title_input, pages):
	scraped_data =  scrape_indeed_job_listings(job_title_input, pages) # + scrape_linkedin_job_listings(job_title_input, pages)
	write_to_csv(scraped_data, job_title_input, pages)


if __name__ == "__main__":
	job_title_input = input('What is the job title to scrape?')
	pages = int(input('How many pages to scrape?'))
	main(job_title_input, pages)
