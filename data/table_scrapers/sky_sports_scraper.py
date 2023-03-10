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

    tbody = leagueSoup.find("tbody")
    trs = tbody.find_all("tr",class_="standing-table__row")

    league_dict = {}
    for tr in trs:
        tds = tr.find_all("td")
        pos = tds[0].text.strip()
        club = tds[1].text.strip()
        league_dict[pos] = club
    save_dict(league_dict,league_name,league_year)
        

if __name__ == "__main__":
    # LEAGUE_NAME = "EFL_Championship"
    # URL = "https://www.skysports.com/championship-table/2022"
    URL = "https://www.skysports.com/league-2-table/2022"
    LEAGUE_NAME = "EFL_League_Two"
    BASE = "https://www.skysports.com"
    indexpage = requests.get(URL)
    indexSoup = BeautifulSoup(indexpage.content,"html.parser")
    unorderedlist = indexSoup.find("ul",class_="page-filters__filter-body")
    hrefs = unorderedlist.find_all("a")
    create_header(LEAGUE_NAME)
    for href in hrefs:
        print(href.text.strip())
        endpoint = href["href"]
        URL = BASE + endpoint
        year = href.text.strip()
        try:
            scrape(URL,LEAGUE_NAME,year)
        except Exception as e:
            print(traceback.format_exc())
            continue


