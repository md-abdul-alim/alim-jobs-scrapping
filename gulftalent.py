import requests
import csv
from datetime import datetime


save_csv_call_counter = 0
file_name = 'gulftalent_saudi_01_feb.csv'
keywords = [
    "Software+developer",
    "Software+engineer",
    "data+scientist",
    "python+developer",
    "javascript+developer"
]


def convert_timestamp_to_date(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S UTC').split(" ")[0]


def save_csv(data):
    global save_csv_call_counter

    header = ['job_title', 'company', 'company_website', 'location', 'date', 'job_desc']
    with open(file_name, 'a', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if save_csv_call_counter == 0:
            writer.writerow(header)
        writer.writerow(data)
    save_csv_call_counter += 1


def extract_jobs(jobs):
    for job in jobs:
        if job["country_id"] == "10111112000000":
            job_title = job["title"]
            job_date = convert_timestamp_to_date(job["posted_date_ts"])
            job_company = job["company_name"]
            job_location = job["location"]

            data = {
                "job_title": job_title,
                "company": job_company,
                "company_website": "",
                "location": job_location,
                "date": job_date,
                "job_desc": ""
            }

            print(data)
            save_csv(data.values())


def main():
    for keyword in keywords:
        url = f"https://www.gulftalent.com/api/jobs/search?condensed=false&config%5Bfilters%5D=ENABLED&config%5Bresults%5D=UNFILTERED&filters%5Bcountry%5D%5B0%5D=10111112000000&filters%5Bfetch_all%5D=true&include_scraped=1&limit=10000&search_keyword={keyword}&version=2"
        response = requests.get(url)

        if response.status_code == 200:
            response = response.json()
            total_jobs = response["results"]["data"]

            if len(total_jobs) >= 1:
                print("Total jobs: ", total_jobs)
                extract_jobs(total_jobs)
            else:
                print('No Jobs Found')
        else:
            print('Failed to retrieve the page. Status code:', response.status_code)

    print("-----------------Total Jobs-------------------")
    print("Total jobs: ", save_csv_call_counter)
    print("-----------------Total Jobs-------------------")


main()
