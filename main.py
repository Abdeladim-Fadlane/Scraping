import cfscrape
import requests 
from bs4 import BeautifulSoup 
import csv 



URL = "https://www.whoscored.com/Statistics" 
scraper = cfscrape.create_scraper()
res = scraper.get(URL) 

soup = BeautifulSoup(res.content, 'lxml')


divs = soup.find_all('tr', {'class': 'col12-lg-2 col12-m-3 col12-s-4 col12-xs-5 grid-abs overflow-text'})

print(divs)

























# url_template = "https://wuzzuf.net/search/jobs/?q=python&a=hpb&page={}"

# jobs = []

# for page in range(0, 2): 
#     url = url_template.format(page)
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'lxml')
#     divs = soup.find_all('div', {'class': 'css-1gatmva e1v1l3u10'})
#     for div in divs:
#         title = div.find('a', {'class': 'css-o171kl'}).text.strip()
#         city = div.find('span', {'class': 'css-5wys0k'}).text.strip()
#         requirements = [a.text.strip() for a in div.find_all('a', {'class': 'css-o171kl'})]
#         place = div.find('span', {'class': 'css-o1vzmt eoyjyou0'}).text.strip()
#         jobs.append({"title": title, "city": city, "requirements": requirements, "place": place})

# with open('jobs.csv', 'w', newline='') as file:
#     writer = csv.DictWriter(file, fieldnames=['title', 'place','city', 'requirements'])
#     writer.writeheader()
#     for job in jobs:
#         writer.writerow(job)
