import requests
from bs4 import BeautifulSoup
import csv

url_template = "https://wuzzuf.net/search/jobs/?q=python&a=hpb&page={}"

jobs = []

for page in range(1, 10): 
    url = url_template.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    divs = soup.find_all('div', {'class': 'css-1gatmva e1v1l3u10'})
    for div in divs:
        title = div.find('a', {'class': 'css-o171kl'}).text.strip()
        city = div.find('span', {'class': 'css-5wys0k'}).text.strip()
        requirements = [a.text.strip() for a in div.find_all('a', {'class': 'css-o171kl'})]
        

        jobs.append({"title": title, "city": city, "requirements": requirements})

with open('jobs.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['title', 'city', 'requirements'])
    writer.writeheader()
    for job in jobs:
        writer.writerow(job)
