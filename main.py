from bs4 import BeautifulSoup
import requests
import time

print("Where is your desired Location?")
user_location = input(">> ").capitalize()
print(f'filtering out all results not in {user_location}\n')

def find_jobs():
    html_text = requests.get('https://www.indeed.co.uk/jobs?q=python&sort=date').text # Asigns all html text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('div', class_='jobsearch-SerpJobCard')
    for index, job in enumerate(jobs):
        published_date = job.find('span', class_='new').text
        if 'new' in published_date: 
            company_name = job.find('span', class_='company').text # used to return just the company name
            skills = job.find('div', class_='jobCardReqList')

            # Section below used to get url
            more_info = job.a['href']
            job_role = job.h2.a.text
            job_url = 'https://www.indeed.co.uk/viewjob?' + more_info[8:] 

            # Section below used to get job location and filter by it
            job_location = job.find('span', class_='location accessible-contrast-color-location').text
            if user_location in job_location:
                with open(f'posts/{index}.txt', 'w') as f:
        
                    if skills == None:
                        f.write(f'Company Name: {company_name.strip()}\n')
                        f.write(f'Role: {job_role.strip()}\n')
                        f.write(f'Required Skills: None specified\n')
                        f.write(f'More Info: {job_url}\n')

                    else:
                        f.write(f'Company Name: {company_name.strip()}\n')
                        f.write(f'Required Skills: {skills.strip()}\n')
                        f.write(f'More Info: {job_url}\n')
                        f.write(f'Role Name: {job_role.strip()}\n')
                print(f"File saved: {index}\n")

if __name__ == "__main__":
    while True:
        find_jobs()
        time_wait = 10
        print(f"Waiting {time_wait} minutes...")
        time.sleep(time_wait * 60)