
import requests 
from bs4 import BeautifulSoup 
import csv


url = "https://wuzzuf.net/search/jobs/?q=python&a=hpb"

response = requests.get(url)

soup = BeautifulSoup(response.content, 'lxml')

divs = soup.find_all('div', {'class': 'css-1gatmva e1v1l3u10'})
jobs = []

for i in range(len(divs)):
    title = divs[i].find('a', {'class': 'css-o171kl'}).text.strip()
    link = divs[i].find('a', {'class': 'css-o171kl'})['href']
    city = divs[i].find('span', {'class': 'css-5wys0k'}).text.strip()
    jobs.append({"title": title, "link": link, "city": city})
    requerment = divs[i].find_all('a', {'class': 'css-o171kl'})
    for j in range(len(requerment)):
        requerment[j] = requerment[j].text.strip()
    jobs.append({"requerment": requerment, "title": title, "link": link, "city": city})


with open('jobs.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['title', 'link', 'city', 'requerment'])
    writer.writeheader()
    for job in jobs:
        writer.writerow(job)
    

    