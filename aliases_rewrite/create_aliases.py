import os
import csv
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

def get_supposed_file_name(team_name,season):
    return f'{team_name}_FIFA_{season[-2:]}'

def get_all_club_files():
    clubs = set()

    script_dir = os.path.dirname(__file__)
    data_dir = os.path.join(script_dir,"fifa_data")
    for filename in os.listdir(data_dir):
        clubs.add(filename[:-4])

    save_file = os.path.join(script_dir,"clubs.txt")
    with open(save_file,'w',encoding="utf-8") as f:
        f.write(str(clubs))
    return clubs

Aliases = {}
already_in_aliases = []
not_found = []

clubs = get_all_club_files()
dirname = os.path.join(script_dir,'table_data')
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
            supposed_file_name = get_supposed_file_name(team_name,season)
            teamseason = team_name + season[-2:]

            if season[-2:] == "23":
                continue
            elif team_name in Aliases:
                already_in_aliases.append(teamseason)
                continue
            elif supposed_file_name not in clubs:
                while supposed_file_name not in clubs:
                    input_team = input("Give alias for \"" + team_name + "\"" + f" (season {season[-2:]})?")
                    clubs = get_all_club_files()
                    if input_team == "":
                        not_found.append(teamseason)
                        break
                    supposed_file_name = get_supposed_file_name(input_team,season)
                    if supposed_file_name in clubs:
                        Aliases[team_name] = input_team
    

save_file = os.path.join(script_dir,"Aliases.txt")
with open(save_file,'w',encoding="utf-8") as f:
    f.write(str(Aliases))

save_file = os.path.join(script_dir,"AlreadyInAliases.txt")
with open(save_file,'w',encoding="utf-8") as f:
    f.write(str(already_in_aliases))

save_file = os.path.join(script_dir,"NotFound.txt")
with open(save_file,'w',encoding="utf-8") as f:
    f.write(str(not_found))