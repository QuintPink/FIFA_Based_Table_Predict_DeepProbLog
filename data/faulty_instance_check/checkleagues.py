import os
import csv
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

def get_supposed_file_name(team_name,season):
    return f'{team_name}_FIFA_{season[-2:]}'

def get_all_club_files():
    clubs = set()

    script_dir = os.path.dirname(__file__)
    data_dir = os.path.join(script_dir,"../fifa_data")
    for filename in os.listdir(data_dir):
        clubs.add(filename[:-4])
    return clubs

incomplete_leagues_teams = {}
incomplete_season_per_league = {}

clubs = get_all_club_files()
dirname = os.path.join(script_dir,'../tables')
for fdir in os.listdir(dirname):
    filename = os.path.join(dirname,fdir)
    start = True
    with open(filename,encoding='utf-8') as f:
        csv_reader = csv.reader(f,delimiter=",")
        used_seasons = set()
        for row in csv_reader:
            if start:
                start = False
                continue
            team_name = row[0]
            season = row[2]   
            season_end = season[-2:]
            if season_end == "23" or season_end == "24" :
                continue     
            supposed_file_name = get_supposed_file_name(team_name,season)
            teamseason = team_name + season_end
            if not supposed_file_name in clubs:
                if fdir not in incomplete_season_per_league:
                    incomplete_season_per_league[fdir] = set()
                    incomplete_season_per_league[fdir].add(season_end)
                else:
                    incomplete_season_per_league[fdir].add(season_end)

                if not (season in used_seasons):
                    incomplete_leagues_teams[fdir+"_"+season_end] = [team_name]
                    used_seasons.add(season)
                else:
                    incomplete_leagues_teams[fdir+"_"+season_end].append(team_name)


save_file = os.path.join(script_dir,"INCOMPLETELEAGUES.txt")
with open(save_file,'w',encoding="utf-8") as f:
    f.write(str(incomplete_leagues_teams))

save_file = os.path.join(script_dir,"INCOMPLETEPERLEAGUE.txt")
with open(save_file,'w',encoding="utf-8") as f:
    f.write(str(incomplete_season_per_league))