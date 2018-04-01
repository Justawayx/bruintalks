# import library used to query website
# import bs4 for Tag object
# import BeautifulSoup functions to parse data returned from website
# import date parser
# import datetime for datetime object
# import pandas to convert list to DataFrame
# import numpy for NaN values in DataFrame
import urllib.request
import bs4
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import datetime
import pandas as pd
import numpy as np

my_site = "https://www.cee.ucla.edu/upcoming-events/"
my_site_base = "https://www.cee.ucla.edu"


# query website and return html to a variable
orig_html = urllib.request.urlopen(my_site)

# parse HTML in the orig_html variable and store in BeautifulSoup format
# 'html5lib' = HTML parser recommended by compiler
parsed_page = BeautifulSoup(orig_html, 'html5lib')

# locate table and separate out the body
table = parsed_page.find('table', class_='custom_events_manager_list')

list_links = []
list_titles = []
list_speakers = []
list_locations = []
list_pre_dates = []
list_orig_times = []

# process each row
for row in table.findAll('tr'):

	# process each cell
	if len(row.findAll('td')) > 0:
	
		# FIRST CELL
		first_cell = row.findAll('td')[0]
		
		list_pre_dates.append(first_cell.contents[0].strip())
		list_orig_times.append(first_cell.contents[2].strip())
		
		
		# SECOND CELL
		second_cell = row.findAll('td')[1]
		
		link_and_title_found = False
		speaker_found = False
		location_found = False
		
		for i in range(0, len(second_cell.contents)):
			item = second_cell.contents[i]
			
			if isinstance(item, bs4.element.Tag):
				
				if item.name == 'a':
					# process link
					my_link = item.get('href')
					if (my_link)[0:4]=='http':
						list_links.append(my_link)
					else:
						list_links.append(my_site_base + my_link)
				
					# process title
					list_titles.append(item.string)
					link_and_title_found = True
					
					
				elif item.name == 'b' and (i + 1) < len(second_cell.contents):
					next_item = second_cell.contents[i + 1]
					
					# process speaker
					if item.string == 'Speaker:':
						list_speakers.append(next_item.strip())
						speaker_found = True
						
					# process location
					elif item.string == 'Location:':
						list_locations.append(next_item.strip())
						location_found = True
					
					
		# fill default values if necessary
		if not link_and_title_found:
			list_links.append('#')
			list_titles.append('TBA')
		if not speaker_found:
			list_speakers.append(np.nan)
		if not location_found:
			list_locations.append(np.nan)
				

# standardize date format
list_dates = []
for date in list_pre_dates:
	new_date = datetime.strptime(date, '%b %d, %Y').date().isoformat()
	list_dates.append(new_date)
	
# standardize time format
list_start_times = []
list_end_times = []

for time in list_orig_times:
	if time == 'All Day':
		list_start_times.append('00:00:00')
		list_end_times.append('11:59:59')
	else:
		both_times = time.split(" - ")
		start_time = datetime.strptime(both_times[0], '%I:%M %p').time().isoformat()
		end_time = datetime.strptime(both_times[1], '%I:%M %p').time().isoformat()
		
		list_start_times.append(start_time)
		list_end_times.append(end_time)
	
			
# create DataFrame
info_df = pd.DataFrame(
	{'link': list_links,
	'title': list_titles,
	'speaker': list_speakers,
	'location': list_locations,
	'date': list_dates,
	'start-time': list_start_times,
	'end-time': list_end_times,
	'subject': 'Civil and Enviro Eng',
	'type': 'seminar'})
	
# preserve column order
info_df = info_df[['link', 'title', 'speaker', 'location', 'date', 'start-time', 'end-time', 'subject', 'type']]
	
	
# 
# print(list_links)
# print(list_titles)
# print(list_speakers)
# print(list_locations)
# 
# print(list_dates)
# print(list_start_times)
# 

print(info_df)
