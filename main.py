from bs4 import BeautifulSoup
import requests

print("Where is your desired Location?")
user_location = input(">> ").capitalize()
print(f'filtering out all results not in {user_location}')


html_text = requests.get('https://www.indeed.co.uk/jobs?q=python&sort=date').text # Asigns all html text
soup = BeautifulSoup(html_text, 'lxml')
jobs = soup.find_all('div', class_='jobsearch-SerpJobCard')
for job in jobs:
    published_date = job.find('span', class_='date').text
    if 'Just' in published_date: 
        company_name = job.find('span', class_='company').text # used to return just the comany name
        skills = job.find('div', class_='jobCardReqList')
        # Section below used to get url
        more_info = job.a['href']
        job_role = job.h2.a.text
        job_url = 'https://www.indeed.co.uk/viewjob?' + more_info[8:] 
        # Section below used to get job location and filter by it
       job_location = job.find('span', class_='location accessible-contrast-color-location').text
        if user_location in job_location:
    
            if skills == None:
                print(f'Company Name: {company_name.strip()}')
                print(f'Role Name: {job_role.strip()}')
                print(f'Required Skills: None specified')
                print(f'More Info: {job_url}')

            else:
                print(f'Company Name: {company_name.strip()}')
                print(f'Required Skills: {skills.strip()}')
                print(f'More Info: {job_url}')
                print(f'Role Name: {job_role.strip()}')
            
        print(' ')
        

            

    
