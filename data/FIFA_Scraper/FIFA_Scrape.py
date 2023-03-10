from bs4 import BeautifulSoup
import requests
import csv
import os
import traceback




# fifaindex.com
BASE = "https://www.fifaindex.com"
Errors = []

def get_soup(url:str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content,"html.parser")
    return soup

def get_year_hyperlinks(soup : BeautifulSoup):
    hyperlinks = {}
    dropdown_items = soup.find_all("li",class_="breadcrumb-item")[1].find_all('a',class_="dropdown-item")
    for item in dropdown_items:
        if len(item.text) == 7:
            endpoint = item["href"]
            hyperlinks[item.text] = endpoint
    return hyperlinks

def go_through_pages_for_game(url,soup : BeautifulSoup,year):
    last_page_nav = soup.find("nav",attrs={"aria-label":"Page navigation"}).find_all("li")[-1].find("a")
    last = int(last_page_nav["href"][-2:])

    base = "?page="
    for page_nr in range(1,last+1):
        print(year + "|" + str(page_nr))
        endpoint = base + str(page_nr)
        current_page_soup = get_soup(url+endpoint)
        go_through_teams_for_page(current_page_soup,year)

def go_through_teams_for_page(soup : BeautifulSoup,year):
    tds = soup.find("table",class_="table table-striped table-teams").find("tbody").find_all("td",attrs={"data-title":"Name"})

    for td in tds:
        href = td.find("a")
        endpoint = href["href"]
        club_name = href.text.strip()

        try:
            curr_soup = get_soup(BASE + endpoint)
            go_through_team(curr_soup,club_name,year)
        except:
            tb = traceback.format_exc()
            Errors.append(str(tb) + "|"  + year + "\n")
            continue

def go_through_team(soup,club_name,year):
    script_dir = os.path.dirname(__file__)
    club_name = check_clubname(club_name)
    save_file = os.path.join(script_dir,"../fifa_data/" + club_name + "_" + year + ".csv")
    with open(save_file,'w',newline='',encoding="utf-8") as f:
        # Write header
        writer = csv.writer(f)
        writer.writerow(["NAME","OVR","POT"])

        # Write players
        players_tr = soup.find("table",class_="table table-players table-striped").find("tbody").find_all("tr")
        for player_tr in players_tr:
            NAME = player_tr.find("td",attrs={"data-title":"Name"}).find("a").text

            OVR_POT_spans = player_tr.find("td",attrs={"data-title":"OVR / POT"}).find_all("span")
            OVR = OVR_POT_spans[0].text
            POT = OVR_POT_spans[1].text
            writer.writerow([NAME,OVR,POT])

def check_clubname(club_name:str):
    FORBIDDEN = ["/","\\",":","|","?","*","<",">",'"']
    new = club_name
    for char in FORBIDDEN:
        if club_name.find(char) != -1:
            new = club_name.replace(char,"_")
    return new

        

    


if __name__ == "__main__":  
    main_soup = get_soup("https://www.fifaindex.com/teams/")
    year_hyperlinks = get_year_hyperlinks(main_soup)
    for year,link in year_hyperlinks.items():
        year = year.replace(" ","_")

        if year == "FIFA_23":
            continue

        url = BASE + link
        yearPageSoup = get_soup(url)
        go_through_pages_for_game(url,yearPageSoup,year)

    script_dir = os.path.dirname(__file__)
    error_file = os.path.join(script_dir,"errors.txt")
    with open(error_file,'w',encoding="utf-8") as f:
        for i in Errors:
            f.write(i)


