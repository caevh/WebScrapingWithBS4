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