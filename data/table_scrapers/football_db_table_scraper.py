from bs4 import BeautifulSoup
import requests
import csv
import os
import traceback
BASE = "https://footballdatabase.com"
passed = {}

def scrape_league(URL):
    page = requests.get(URL)

    leagueSoup = BeautifulSoup(page.content,"html.parser")

    # League name
    nameTag = leagueSoup.find("h1", class_="featured-club-name")
    league_name_year = nameTag.text.strip()


    # Standings
    standingsResult = leagueSoup.find("div",class_="tab-pane",id="total")

    results = standingsResult.find("tbody").find_all("tr")
    league_dict = {}
    for row in results:
        columns = row.find_all("td")
        pos = columns[0].text.strip()
        name = columns[1].text.strip()
        league_dict[pos] = name
    return league_dict

def get_season(URL):
    page = requests.get(URL)

    leagueSoup = BeautifulSoup(page.content,"html.parser")

    # League name
    nameTag = leagueSoup.find("h1", class_="featured-club-name")
    league_name_year : str = nameTag.text.strip()

    index = league_name_year.index("20")
    season = league_name_year[index:index+4]
    try:
        if league_name_year[index+4] == "/":
            length = len(league_name_year[index+5:])
            if length == 4:
                season += "-" + league_name_year[index+7:index+9]
            else: 
                season += "-" + league_name_year[index+5:index+7]
    except Exception as e:
        season += "-" + season[2:]
    return season

def create_header(league_name):
    league_name = league_name.replace(" ","_")
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    file_name = "table_data\standings_" + league_name + ".csv"
    abs_file_path = os.path.join(script_dir, file_name)
    header = ["team","pos","season"]
    with open(abs_file_path,'w', newline='', encoding='utf-8') as f:
        print("writing")
        writer = csv.writer(f)
        writer.writerow(header)
def save_dict(league_dict : dict,league_name:str,league_season:str):
    league_name = league_name.replace(" ","_")
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    file_name = "table_data\standings_" + league_name + ".csv"
    abs_file_path = os.path.join(script_dir, file_name)
    with open(abs_file_path,'a', newline='', encoding='utf-8') as f:
        print("writing")
        writer = csv.writer(f)
        for (pos,name) in league_dict.items():
            writer.writerow([name,pos,league_season])
   
def scrape_all_years(URL,league_name):
    
    page = requests.get(URL)
    leagueSoup = BeautifulSoup(page.content,"html.parser")

    select = leagueSoup.find("select",attrs={"name":"pastCompetitions"})
    options = select.find_all("option")

    create_header(league_name)
    for option in options:
        if option["value"].strip() == "":
            continue
        endpoint = option["value"].strip()
        curr_URL = BASE + endpoint
        print(curr_URL)
        league_dict = scrape_league(curr_URL)
        league_season = get_season(curr_URL)
        save_dict(league_dict,league_name,league_season)
        

if __name__ == "__main__":
    BASE = "https://footballdatabase.com"
    # Scrape all URLs
    INDEX_URL= "https://footballdatabase.com/competitions-index"
    indexpage = requests.get(INDEX_URL)
    indexSoup = BeautifulSoup(indexpage.content,"html.parser")
    clubBrowser = indexSoup.find("div",class_="tab-content").find("div",class_="clubbrowser")
    hrefs = clubBrowser.find_all("a")
    for href in hrefs:
        endpoint = href["href"]
        URL = BASE + endpoint
        league_name = href.text.strip()
        try:
            scrape_all_years(URL,league_name)
        except Exception as e:
            print(traceback.format_exc())
            continue


