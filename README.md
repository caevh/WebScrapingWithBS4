**Part 1: Scraping from a local HTML file**

First import beautiful soup like;
`from bs4 import BeautifulSoup`

Next, because we are just scraping from a html file we will use the open method to read a file. 
```
with open('index.html', 'r') as html_file:
	content = html_file
	
	soup = BeautifulSoup(content, 'lxml')
	courses_html_tags = soup.find_all('h5')
	
	for course in courses_html_tags:
		print(course.text)
```

- so we open the file and define the `content` variable.
- We then create the `soup` object and use the `content` variable along with `lxml`. Lxml is the software used to parse the data. 
- Next we define the variable `courses_html_tags`. We then use `soup.find_all('h5')` to loop through the html file looking for all h5 tags. `courses_html_tags` will be of type list.
- We can now loop through the `courses_html_tags` list to print out just the text not the entire tag. To do this we use `course.text`

* * *

**Part 2**

To get the price we have to find all of the `div' tags as this is where the the card body elements are inside it. 

```
<div class="card" id="card-python-for-beginners">
<div class="card-header">
            Python
         </div>
<div class="card-body">
<h5 class="card-title">Python for beginners</h5>
<p class="card-text">If you are new to Python, this is the course that you should buy!</p>
<a class="btn btn-primary" href="#">Start for 20$</a>
</div>
</div>
```
the python code to do this looks like this;


```
from bs4 import BeautifulSoup

with open('index.html', 'r') as html_file:
    content = html_file.read()

    soup = BeautifulSoup(content, 'lxml') 
    course_cards = soup.find_all('div', class_='card')

    for course in course_cards:
        course_name = course.h5.text
        course_price = course.a.text.split()[-1]
        
        print(f'{course_name} costs {course_price[-3:]}')
```

- We use the same `soup` variable as before.
- We create the `course_cards` object which looks for all the `div` tags which are of class `card`. We do this so we only get the `div` tags we need.
	- **Note**: Make sure the class has an underline after (`class_='card'`) it otherwise it will think you are using the Python keyword class. 
- Next we use a for loop over the course_cards list to search for the `h5` tags first. This is where the course title is stored.
- Next, we use the for loop to get the `a` tags as this is where the price element is. 
- We use `.split()[-1]` to first split the string into a list, then access the price which is stored at the end of the list. 
- We then use print and f-string formatting, print;
```
Python for beginners costs 20$
Python Web Development costs 50$
Python Machine Learning costs 00$
```
* * *

**Part 3: Scraping from a real site**

We're now going to scrape from a real site. For the site, I chose https://www.indeed.co.uk the reason? Because my code eventually will look for jobs recently posted under a certain title, I chose "Python". 

First, I went to the site and typed Python in the search bar until a list of jobs were posted, from here I sorted by new. 

The first thing we need to make sure is the requests library is installed. Do this using pip, `pip install requests`. For me, I used a requirements.txt file with all my dependencies in and a virtual env. 

The finished code for this section will look like this;

```
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
```

- We import all the libraries we need.
- A `html_text` variable is created. We then use request and get to get all the HTML from the URL provided. 
	- `.text` is used so, the HTML will be assigned to the variable. Without the text, it will display something like `<Response [200]>`
- We then do the same as before and create the soup object
- Next, the job variable is created. This is used to see individual job cards. 
	- `soup.find' searches for the 'div' element, it then searched for the class `jobsearch-SerpJobCard` 
	- To find this out, I right-clicked on the card and clicked inspect and searched until I found an element and class that is associated with the job card. 
- I then create the variables `company_name` and inspect the HTML until I find the element and class associated. the same is done for `skills` and `published_date`
- An `if-else` statement is written as I found some jobs did not specify any requirements implicitly on the home page job card.  
	- The statement checks if `skills` is equal to `None` it assumes no requirements specified else, tells you the requirements. 
- The `published_date` will be used later on when checking the age of a posting. 

* * *

**Part 4**

Using `find_all` to find all matching jobs and filtering for a certain time posted.

The finished code:
```
from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://www.indeed.co.uk/jobs?q=python&sort=date').text # Asigns all html text

soup = BeautifulSoup(html_text, 'lxml')
jobs = soup.find_all('div', class_='jobsearch-SerpJobCard')
for job in jobs:
    published_date = job.find('span', class_='date').text
    if 'Just' in published_date: 
        company_name = job.find('span', class_='company').text # used to return just the comany name
        skills = job.find('div', class_='jobCardReqList')
    

        if skills == None:
            print(f"""Company Name:{company_name}

Minimal requirements: None specified
        """)
        else:
            print(f"""Company Name: {company_name} 
        Minimal requirements: {skills.text}""")

        

        print(' ')
```

Additions/edits to the code;
```
jobs = soup.find_all('div', class_='date').text class_='jobsearch-SerpJobCard')
for job in jobs:
    published_date = job.find('span', class_='date').text
    if 'Just' in published_date: 
        company_name = job.find('span', class_='company').text # used to return just the comany name
        skills = job.find('div', class_='jobCardReqList')
    

        if skills == None:
            print(f"""Company Name:{company_name}

Minimal requirements: None specified
        """)
        else:
            print(f"""Company Name: {company_name} 
        Minimal requirements: {skills.text}""")

        

        print(' ')
```

- First, `soup.find_all` is added to find all job posts that fall under our specified tags and class.
- next, we use a for loop to loop through the job posts. These are stored in an iterable list.
- In the for loop, we use the `published_date` variable to store the publish date of a post.
- next, we add an `if` statement to check if `just` is specified in the `publish_date` variable if it is, we print the job. 

* * *
**Part 5: Adding a URL**

In this section, we will add a URL. 

The finished code:
```
from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://www.indeed.co.uk/jobs?q=python&sort=date').text # Asigns all html text

soup = BeautifulSoup(html_text, 'lxml')
jobs = soup.find_all('div', class_='jobsearch-SerpJobCard')
for job in jobs:
    published_date = job.find('span', class_='date').text
    if 'Just' in published_date: 
        company_name = job.find('span', class_='company').text # used to return just the comany name
        skills = job.find('div', class_='jobCardReqList')
        more_info = job.a['href']
        job_url = 'https://www.indeed.co.uk/viewjob?' + more_info[8:] 
    

        if skills == None:
            print(f"Company Name: {company_name.strip()}")
            print(f"Required Skills: None specified")
            print(f"More Info: {job_url}")
        else:
            print(f"Company Name: {company_name.strip()}")
            print(f"Required Skills: {skills.strip()}")
            print(f"More Info: {job_url}")
            

        
        print(' ')
```

Additions to code;
```
for job in jobs:
    published_date = job.find('span', class_='date').text
    if 'Just' in published_date: 
        company_name = job.find('span', class_='company').text # used to return just the comany name
        skills = job.find('div', class_='jobCardReqList')
        more_info = job.a['href']
        job_url = 'https://www.indeed.co.uk/viewjob?' + more_info[8:] 
```

- We added the variable `more_info`. This is assigned the value of `job.a['href']`. 
	- In this code, we use the `job.a` to get the `a` tag inside the job URL. The reason for this is because the `href` (URL) is stored inside this tag. 
	- We then use `['href']` to return just the value of `href`
- `job_url` is created because the link that is given didn't seem to work when not accessed from VS code.
	- The link was missing the string that has been added in the code. 
	- `more_info[8:]` is used because we only need to access a part of the link that was given, not the whole link, to get it to work

* * *
**Part 6: User input filtering**

Using user input to filter by job location and adding a job role.

The finished code for this section;

```
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
        more_info = job.a['href']
        job_role = job.h2.a.text
        job_url = 'https://www.indeed.co.uk/viewjob?' + more_info[8:] 
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
```
Added or edited code;

```
print("Where is your desired Location?")
user_location = input(">> ").capitalize()
print(f'filtering out all results not in {user_location}')
```
```
        more_info = job.a['href']
        job_role = job.h2.a.text
        job_url = 'https://www.indeed.co.uk/viewjob?' + more_info[8:] 
        job_location = job.find('span', class_='location accessible-contrast-color-location').text
        if user_location in job_location:
```

- First, we added the print statements and user input statements. This will be used later on in the code to filter our results. 
- Later in the code `job_role` variable is created and assigned to the tag which contains the job role.
- Next, `job_location` is defined and is assigned to the tag in which the job location is defined. 
- The an `if` statement is used to see if the user's input is in the `job_location` string. 

* * * 
**Part 7: Writing to a file and automating the script**

Adding code to append the job listing to a text file and automating the job to run every 10 minutes. 

The finished code;	

```
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
```

Newly added or edited code;

```
from bs4 import BeautifulSoup
import requests
import time
```
`for index, job in enumerate(jobs):`
```
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
```

- First, `time` is imported. This will be used late for automation
- the next line that's changed is the first for loop. We add `index` and `enumerate()`.
	- `enumerate()` assigns an index for each item in an iterable list, for this, we need to add `index` in the for loop. The index can then be referenced.
- `with open` is then used to open a file in a folder that's been created. We then use the `index` to give the text file a name.
- The `print` statements are then changed for `f.write` statements. 
- A `__name__ == '__main__' is then used along with a while loop to run the code every x amount of time.
- `time_wait` is used to specify a time in minutes 
- `time.sleep` is then used with `time_wait` and the multiplication operator to make sure the script runs every ten minutes.