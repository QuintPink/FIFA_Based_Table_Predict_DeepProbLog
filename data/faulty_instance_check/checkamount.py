import os
import csv
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in


incomplete_season_per_league = {'standings_Argentina_Primera.csv': ('21', '22'), 
'standings_South_Korea_K-League_Classic.csv': ('20', '09', '14', '18', '17', '16', '21', '15', '19', '22', '11'), 
'standings_Spain_LaLiga_2.csv': ('10', '07', '08'), 
'standings_Turkey_Super_Lig.csv': ('13', '10', '14', '12', '11'), 
'standings_United_States_Major_League_Soccer.csv': ('20', '09', '18', '17', '10', '21', '12', '19', '22', '11')}

seasons = set()
dirname = os.path.join(script_dir,'../tables')
for fdir in os.listdir(dirname):
    filename = os.path.join(dirname,fdir)
    start = True
    with open(filename,encoding='utf-8') as f:
        csv_reader = csv.reader(f,delimiter=",")
        for row in csv_reader:
            if start:
                start = False
                continue
            team_name = row[0]
            season = row[2]   
            season_end = season[-2:]
            if season_end == "23" or season_end == "24" :
                continue
            if fdir in incomplete_season_per_league:
                if season_end in incomplete_season_per_league[fdir]:
                    continue
            else:
                seasons.add(fdir + season_end)

print(len(seasons))