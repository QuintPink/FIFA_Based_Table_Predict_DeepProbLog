import csv 
import os
from team import Team
from player import Player
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in


TeamDict : dict[str,Team] = {}

dirname = os.path.join(script_dir,'data')
for fdir in os.listdir(dirname):
    year_end = fdir[4:6]
    year = f'20{year_end}'
    filename = os.path.join(dirname,fdir)
    start = True
    with open(filename,encoding='utf-8') as f:
        csv_reader = csv.reader(f,delimiter=",")
        for row in csv_reader:
            if start:
                start = False
                continue
            team_name = row[8] + year
            if not (team_name in TeamDict):
                curr_team = Team(team_name,year)
                TeamDict[team_name] = curr_team
            else:
                curr_team = TeamDict[team_name]
            player_name = row[1]
            player_OVR = row[6]
            curr_player = Player(player_name,int(player_OVR))
            curr_team.add_player(curr_player)
 






save_file = os.path.join(script_dir,"Teams.txt")
with open(save_file,'w',encoding="utf-8") as f:
    f.write(str(TeamDict))
