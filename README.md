**Part 1**

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