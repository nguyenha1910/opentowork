"""
Module initializes job scraping process and writes out results to csv file.
Depends on indeed_jobs and linkedin_jobs.
Functions:
    write_to_csv - writes out data to csv file
    main - initializes the scraping process and calls write_to_csv
"""
import csv
import os
import subprocess
import yaml
import math
from datetime import datetime
from .get_jobs import scrape_search

with open("config.yml", "r", encoding='UTF-8') as config_file:
    config = yaml.safe_load(config_file)

def write_to_csv(data, job_titles, total_job_count):
    """
    Function writes inputted data to csv file with job titles, number of jobs,
    and scraped time in file name.
    Args:
        data (list): list of job information to write out
        job_titles (list): job titles used in scraping
        total_job_count (int): target total number of jobs scraped
    Returns:
        None
    Exceptions:
        TypeError for data arg (if data is not a list)
        TypeError for job_titles arg (if job_titles is not list)
        TypeError for total_job_count arg (if total_job_count is not int)
        ValueError for data arg (if not all items in list are dict)
        ValueError for job_titles arg (if not all items in list are string)
    """
    if isinstance(data, list) is not True:
        raise TypeError("Data input is not a list")
    if isinstance(job_titles, list) is not True:
        raise TypeError("Job titles input is not a list")
    if isinstance(total_job_count, int) is not True:
        raise TypeError("Total job count needs to be int")
    if len(data) > 0 and any(not isinstance(job, dict) for job in data):
        raise ValueError("All data need to be in dict")
    if any(not isinstance(job, str) for job in job_titles):
        raise ValueError("All job titles need to be strings")

    scrape_dt = datetime.now().strftime("%Y%m%d_%H%M%S")
    directory = "data/csvs"
    if not os.path.exists(directory):
        os.makedirs(directory)

    job_title_str = '_'.join(job_titles).replace(' ', '_')

    filename = f"job_listings_{job_title_str}_{total_job_count}_jobs_scraped_{scrape_dt}.csv"
    csv_file = os.path.join(directory, filename)
    colnames = ["title", "company", "location", "posted date",
                "link", "description", "scraped date"]

    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=colnames)
        writer.writeheader()
        writer.writerows(data)

def jobs_per_title(job_titles, total_job_count):
    """
    Function calculates target number of jobs to scrape per job title.
    Args:
        job_titles (list): list of job titles to scrape
        total_job_count (int): total number of job listings to scrape
    Returns:
        job_count (int): number of job listings to scrape per job title
    Exceptions:
        TypeError for job_titles arg (if not a list)
        TypeError for total_job_count (if not int)
    """
    if isinstance(job_titles, list) is not True:
        raise TypeError("Job titles input is not a list")
    if isinstance(total_job_count, int) is not True:
        raise TypeError("Total job count needs to be int")

    job_count = math.ceil(total_job_count/len(job_titles))
    return job_count

def scrape_jobs(job_titles, total_job_count):
    """
    Function gets the number of listings to scrape for each job title and loops through
    job titles to create job listings dataset. Tries LinkedIn twice before moving to Indeed
    if no jobs found, tries scraping 4 times total for each job title. Calls scrape_search
    from get_jobs module.
    Args:
        job_titles (list): list of job titles to scrape
        total_job_count (int): target total number of jobs to scrape for all titles
    Returns:
        scraped_data (list): list of jobs (each in a dictionary)
    Exceptions:
        TypeError for job_title_input arg (if job_title_input is not list)
        TypeError for total_job_count arg (if total_job_count is not int)
        ValueError for job_titles arg (if not all items in list are string)
    """
    if isinstance(job_titles, list) is not True:
        raise TypeError("Job titles input is not a list")
    if isinstance(total_job_count, int) is not True:
        raise TypeError("Total job count needs to be int")
    if any(not isinstance(job, str) for job in job_titles):
        raise ValueError("All job titles need to be strings")

    target_job_count = jobs_per_title(job_titles, total_job_count)
    scraped_data = []

    for job_title in job_titles:
        data = []
        total_tries = 0
        has_data = False
        while total_tries < 2 and has_data is False:
            total_tries += 1
            data = scrape_search(job_title, target_job_count, "LinkedIn")
            if len(data) > 0:
                has_data = True

        while 2 <= total_tries < 4 and has_data is False:
            total_tries += 1
            data = scrape_search(job_title, target_job_count, "Indeed")
            if len(data) > 0:
                has_data = True

        scraped_data.extend(data)

    return scraped_data

def check_chrome_driver():
    if 'CONDA_PREFIX' in os.environ:
        bin_path = os.path.join(os.environ['CONDA_PREFIX'], "bin")
    else:
        bin_path = os.path.join('/home',os.environ['SUDO_USER'],'.conda', "bin")
    if 'chromedriver' not in os.listdir(bin_path):
        driver_src_path = os.path.join( 'chromedriver',
                                        config['chrome_driver_version'], 
                                        "chromedriver")
        command = f"mv {driver_src_path} {bin_path}"
        subprocess.run(command, shell=True, check=True)
    if 'chromedriver' in os.listdir(bin_path):
        return True
    else:
        return False

def main(job_titles = None, total_job_count = 30):
    """
    Main function to initialize job scraping processes.
    Takes the scraping output lists and writes to one csv file.
    Args:
        job_titles (list) - list of job titles to search
        total_job_count (int) - number of total jobs to scrape
    """
    if not check_chrome_driver():
        os.write("Could not find chromedriver")
        raise Exception("Could not find chromedriver")
    else:
        os.write("Found chromedriver")
    if job_titles is None:
        job_titles = ['data analyst', 'data scientist', 'data engineer']
    scraped_data = scrape_jobs(job_titles, total_job_count)
    write_to_csv(scraped_data, job_titles, total_job_count)

    if len(scraped_data) == 0:
        print("Oops! There was an error getting jobs. Please try again.")

if __name__ == "__main__":
    main()
