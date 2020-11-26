from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://www.indeed.co.uk/jobs?q=python&sort=date').text # Asigns all html text

soup = BeautifulSoup(html_text, 'lxml')
job = soup.find('div', class_='jobsearch-SerpJobCard')
company_name = job.find('span', class_='company').text # used to return just the comany name
skills = job.find('div', class_='jobCardReqList')
published_date = job.find('span', class_='date').text

if skills == None:
    print(f"""Company Name: {company_name}
Minimal requirements: None specified""")
else:
    print(f"""Company Name: {company_name} 
Minimal requirements: {skills.text}""")

print(published_date)

    
