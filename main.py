import requests
from bs4 import BeautifulSoup
import csv
def get_matches():
    data = "05/13/2024"
    soup = BeautifulSoup(requests.get(f"https://www.yallakora.com/Match-Center/?date={data}").content, "lxml")
    match_details = []
    championships = soup.find_all("div", {'class': 'matchCard'})

    def get_match_info(championships):
        championship_title = championships.contents[1].find("h2").text.strip()
        all_matches = championships.contents[3].find_all("div", {"class": "item future liItem"})
        number_of_matches = len(all_matches)
        for i in range(number_of_matches):
            teamA = all_matches[i].find("div", {"class": "teamA"}).text.strip()
            teamB = all_matches[i].find("div", {"class": "teamB"}).text.strip()
            match_result = all_matches[i].find("div", {"class": "MResult"}).find_all("span", {"class": "score"})
            score = f"{match_result[0].text.strip()}-{match_result[1].text.strip()}"
            match_time = all_matches[0].find("div", {"class": "MResult"}).find("span", {"class": "time"}).text.strip()
            match_details.append({"Championship: " : championship_title, "Team A: " : teamA, "Team B: " : teamB, "Score: " : score, "Time: " : match_time})
       
    for i in range(len(championships)):
        get_match_info(championships[i])
    keys = match_details[0].keys()

    with open("yallakora.csv", "w") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(match_details)

def Rank_soccer():
    url = "https://en.wikipedia.org/wiki/FIFA_Men%27s_World_Ranking"

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    divs = soup.find('table', {'class': 'wikitable'})
    ranks = []
    trs = divs.find_all('tr')
    for i in range(3, 23):
        rank = trs[i].find('td').text
        team = (trs[i].find('a').text)
        points = trs[i].find_all('td')[3].text.strip()
        ranks.append({"rank": rank, "team": team, "points": points})

    with open('fifa.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['rank', 'team', 'points'])
        writer.writeheader()
        writer.writerows(ranks)

def get_jobs():
    url_template = "https://wuzzuf.net/search/jobs/?q=python&a=hpb&page={}"

    jobs = []

    for page in range(0, 2): 
        url = url_template.format(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        divs = soup.find_all('div', {'class': 'css-1gatmva e1v1l3u10'})
        for div in divs:
            title = div.find('a', {'class': 'css-o171kl'}).text.strip()
            city = div.find('span', {'class': 'css-5wys0k'}).text.strip()
            requirements = [a.text.strip() for a in div.find_all('a', {'class': 'css-o171kl'})]
            place = div.find('span', {'class': 'css-o1vzmt eoyjyou0'}).text.strip()
            jobs.append({"title": title, "city": city, "requirements": requirements, "place": place})

    with open('jobs.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'place','city', 'requirements'])
        writer.writeheader()
        for job in jobs:
            writer.writerow(job)

def main():
    Rank_soccer()
    get_jobs()
    get_matches()

if __name__ == "__main__":
    main()







