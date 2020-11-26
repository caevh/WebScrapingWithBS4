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