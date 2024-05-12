
import requests 
from bs4 import BeautifulSoup 
import csv


data = "05/12/2024"
def main():
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
        

main()