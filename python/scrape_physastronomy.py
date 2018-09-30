import urllib.request
from bs4 import BeautifulSoup
import re

#needs fix for unicode fuckery
#needs multiple pages
#need to replace dumb whitespace removal prolocation stuff with strip()

page = urllib.request.urlopen("http://www.pa.ucla.edu/events")

# parse the html
soup_page = BeautifulSoup(page, "html.parser")

# find a list of all span elements
events = soup_page.find_all('span', class_="date-display-single")
names = soup_page.find_all('strong')
everything = soup_page.find_all('div', class_="event")

# create a list of events corresponding to element texts
lines = [span.get_text() for span in events]
lines2 = [strong.get_text() for strong in names]
lines3 = [div.get_text() for div in everything]
found_dates=[]
found_times=[]
found_title=[]
found_speaker=[]
found_prolocation=[]
found_location=[]

for line in lines:
    m = re.search("\s-", line)
    found_dates.append(line[0:m.start()])
    found_times.append(line[m.start()+3:])

for line in lines2:
    line.split("&quot;\s")
    m = re.search("\sby\s",line)
    n = re.search("\s\W[A-Z]",line)
    if m:
        found_title.append(line[0:m.start()])
        found_speaker.append(line[m.start()+4:n.start()])
    else:
        found_title.append(line)
        found_speaker.append("None")

for line in lines3:
    w = re.search("Location:\s+",line)
    if w:
        found_prolocation.append(line[w.start()+14:])
for line in found_prolocation:
    v = re.search("\w\s\s\s",line)
    if v:
        found_location.append(line[:v.start()+1])
