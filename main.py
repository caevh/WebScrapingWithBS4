from bs4 import BeautifulSoup

with open('index.html', 'r') as html_file:
    content = html_file.read()

    soup = BeautifulSoup(content, 'lxml') 
    courses_htlm_tags = soup.find_all('h5')
    
    for course in courses_htlm_tags:
        print(course.text)