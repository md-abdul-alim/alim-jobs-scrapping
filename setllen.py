import csv
import requests
from bs4 import BeautifulSoup

save_csv_call_counter = 0
file_name = 'setllen_market_de_25_jan.csv'
keywords = [
    "Software+developer",
    "Software+engineer",
    "data+scientist",
    "python+developer",
    "javascript+developer"
]


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
    if len(jobs) >= 1:
        for job in jobs:
            job_title = job.find(class_='jwtpl-hili-itemTitel').text.strip()
            job_date = job.find(class_='jwtpl-hili-itemDate').text.strip()
            job_company = job.find(class_='jwtpl-hili-itemCompany').text.strip()
            job_location = job.find(class_='jwtpl-hili-itemLocation').text.strip()

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


def paginated_jobs(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        all_jobs = soup.find_all(class_='jwtpl-hili-col2')
        extract_jobs(all_jobs)
    else:
        pass


def get_urls(soup, total_pages):
    for page in range(1, total_pages + 1):
        next_page_url = soup.find('a', class_='jwtpl-hilipage-nextBt jwtpl-hilipage-nextBtActive1').get('href') if soup.find('a', class_='jwtpl-hilipage-nextBt jwtpl-hilipage-nextBtActive1') else print("End of the page. No Job anymore.")
        base_url = next_page_url.split("jssc")[0]
        new_int_value = f'jssc={page*20}'
        updated_url = base_url + str(new_int_value)

        paginated_jobs(updated_url)


def main():
    for keyword in keywords:
        url = f"https://stellenmarkt.sueddeutsche.de/suchergebnis?jsjn={keyword}&jsjnid=&jsjo=&jsjoid=&jsjr=#"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            all_jobs = soup.find_all(class_='jwtpl-hili-col2')

            if len(all_jobs) >= 1:
                extract_jobs(all_jobs)

                total_jobs = int(soup.find(class_='jwtpl-seco1-contentSpecial').text.strip().split(" ")[0])
                total_pages = total_jobs // 20

                print("------------------------------------")
                print("Jobs for: ", keyword, "Total jobs: ", total_jobs, "Total Pages: ", total_pages)
                print("------------------------------------")

                if total_pages > 1:
                    get_urls(soup=soup, total_pages=total_pages)
            else:
                print('Element with class jwtpl-hili-col2 not found.(No Jobs Found)')
        else:
            print('Failed to retrieve the page. Status code:', response.status_code)

    print("-----------------Total Jobs-------------------")
    print("Total jobs: ", save_csv_call_counter)
    print("-----------------Total Jobs-------------------")


main()
