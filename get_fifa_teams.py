import os
import csv

TeamDict = {"not-used":"not-used"}
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
dirname = os.path.join(script_dir,'data')
for fdir in os.listdir(dirname):
    filename = os.path.join(dirname,fdir)
    start = True
    with open(filename,encoding='utf-8') as f:
        csv_reader = csv.reader(f,delimiter=",")
        for row in csv_reader:
            if start:
                start = False
                continue
            team_name = row[8]
            TeamDict[team_name] = team_name

save_file = os.path.join(script_dir,"TeamsListed.txt")
with open(save_file,'w',encoding="utf-8") as f:
    f.write(str(TeamDict))
