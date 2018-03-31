# import library used to query website
# import BeautifulSoup functions to parse data returned from website
# import date parser
import urllib.request
from bs4 import BeautifulSoup
from dateutil import parser

my_site = "https://www.mcdb.ucla.edu/seminars"
my_site_base = "https://www.mcdb.ucla.edu"


# query website and return html to a variable
orig_html = urllib.request.urlopen(my_site)

# parse HTML in the orig_html variable and store in BeautifulSoup format
# 'lxml' = HTML parser recommended by compiler
parsed_page = BeautifulSoup(orig_html, 'lxml')

# begin separating titles, speakers, dates/times, locations
all_titles = parsed_page.find_all('div', class_='views-field views-field-title')
all_speakers = parsed_page.find_all('div', class_='views-field views-field-field-speaker')
all_times = parsed_page.find_all('div', class_='views-field views-field-field-date')
all_locations = parsed_page.find_all('div', class_='views-field views-field-field-location')


# process links
list_links = []

for chunk in all_titles:
	for x in chunk.findAll('a'):
		if (x.get('href'))[0:4]=='http':
			list_links.append(x.get('href'))
		else:
			list_links.append(my_site_base + x.get('href'))


# process titles
list_titles = []

for chunk in all_titles:
	for x in chunk.findAll('a'):
		list_titles.append(x.string)


# process speakers
list_speakers = []

for chunk in all_speakers:
	for x in chunk.findAll('div', class_='field-content'):
		list_speakers.append(x.string)
		
		
# process dates and times
list_dates = []
list_start_times = []
list_end_times = []

for chunk in all_times:
	for x in chunk.findAll('span', class_='date-display-single'):
		my_date = parser.parse(x['content']).now().date()
		list_dates.append(my_date.isoformat())
		
		my_time = parser.parse(x['content']).time()
		list_start_times.append(my_time.isoformat())

		
# process locations
list_locations = []

for chunk in all_locations:
	for x in chunk.findAll('div', class_='field-content'):
		list_locations.append(x.string)
		

print(list_links)
print(list_titles)
print(list_speakers)
print(list_locations)

print(list_dates)
print(list_start_times)
print(list_end_times)

		

