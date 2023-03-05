from bs4 import BeautifulSoup
import requests
import csv
import os
import traceback

def create_header(league_name):
    league_name = league_name.replace(" ","_")
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    file_name = "table_data\standings_" + league_name + ".csv"
    abs_file_path = os.path.join(script_dir, file_name)
    header = ["team","pos","season"]
    with open(abs_file_path,'w', newline='', encoding='utf-8') as f:
        print("writing header")
        writer = csv.writer(f)
        writer.writerow(header)
def save_dict(league_dict : dict,league_name:str,league_season:str):
    league_name = league_name.replace(" ","_")
    league_season = league_season.replace("/","-")
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    file_name = "table_data\standings_" + league_name + ".csv"
    abs_file_path = os.path.join(script_dir, file_name)
    with open(abs_file_path,'a', newline='', encoding='utf-8') as f:
        print("writing")
        writer = csv.writer(f)
        for (pos,name) in league_dict.items():
            writer.writerow([name,pos,league_season])
   
def scrape(URL,league_name,league_year):
    
    page = requests.get(URL)
    leagueSoup = BeautifulSoup(page.content,"html.parser")

    tbody = leagueSoup.find("tbody", class_="Table__TBODY")
    trs = tbody.find_all("tr")

    league_dict = {}
    for tr in trs:
        links = tr.find_all("a",class_="AnchorLink")
        club = links[2].text.strip()
        pos = tr.find("span",class_="team-position ml2 pr3").text.strip()
        league_dict[pos] = club
    save_dict(league_dict,league_name,league_year)
        

if __name__ == "__main__":

    URL = "https://www.espn.com/soccer/standings/_/league/SWE.1/season/2022"
    LEAGUE_NAME = "Sweden_Allsvenskan"
    BASE = "https://espn.com"
    indexpage = requests.get(URL)
    indexSoup = BeautifulSoup(indexpage.content,"html.parser")
    year_div = indexSoup.find_all("div",class_="dropdown mr3")[1]
    options = year_div.find("select",class_="dropdown__select").find_all("option")
    
    create_header(LEAGUE_NAME)
    for option in options:
        print(option.text.strip())
        endpoint = option["data-url"]
        URL = BASE + endpoint
        year = option.text.strip()
        try:
            scrape(URL,LEAGUE_NAME,year)
        except Exception as e:
            print(traceback.format_exc())
            continue


