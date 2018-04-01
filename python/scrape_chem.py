import urllib.request
import re
import bs4
from bs4 import BeautifulSoup

my_site = "https://www.chemistry.ucla.edu/seminars"
base_site = "https://www.chemistry.ucla.edu"
page = urllib.request.urlopen(my_site)
soup = BeautifulSoup(page, 'html.parser')

all_list_speaker=soup.find_all('div', attrs={'class':"speaker"})
all_list_date=soup.find_all('div', attrs={'class':"date"})
all_list_time =soup.find_all('div', attrs={'class':"time"})
all_list_location =soup.find_all('div', attrs={'class':"location"})
all_list_title = soup.find_all('div', attrs={'class':"title"})

list_prospeaker = []
list_speaker = []
list_date = []
list_time=[]
list_location=[]
list_link = []
list_title=[]

for chunk in all_list_date:
	for x in chunk.findAll("span"):
		list_date.append(x.text)

for chunk in all_list_speaker:
	x=chunk.encode("utf-8")
	m=re.search("\s[A-Z]",x)
	if m:
		list_prospeaker.append(x[m.start():])

for x in list_prospeaker:
	n=re.search("\s<",x)
	if n:
		list_speaker.append(x[:n.start()-5])

for chunk in all_list_time:
	for x in chunk.findAll("span"):
		list_time.append(x.text)

for chunk in all_list_location:
	for x in chunk.findAll("div"):
		list_location.append(x.text)

for chunk in all_list_title:
	for link in chunk.findAll('a'):
		if (link.get('href'))[0:4]=="http":
			list_link.append(link.get('href'))
		else:
			list_link.append(base_site + link.get('href'))
for x in list_link:
	new_page = urllib.request.urlopen(x)
	new_soup = BeautifulSoup(new_page, 'html.parser')
	new_list_title=new_soup.find_all('div',attrs={'property':"content:encoded"})
	for newchunk in new_list_title:
		x=newchunk.encode("utf-8")
		m1=re.search("p>",x)
		m2=re.search("g>",x)
		n=re.search("</",x)
		if m2:
			if x[m2.start()+2] != "<":
				list_title.append(x[m2.start()+2:n.start()])
			else:
				list_title.append("None")
		else:
			if x[m1.start()+2] != "<":
				list_title.append(x[m1.start()+2:n.start()])
			else:
				list_title.append("None")

