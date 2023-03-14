import os
import csv
from deepproblog.dataset import Dataset
from domain.player import Player
from domain.team import Team
from domain.league import League
from deepproblog.query import Query
import random
import copy

script_dir = os.path.dirname(__file__)
FIFA_path_rel = "data/fifa_data"
FIFA_path_abs = os.path.join(script_dir,FIFA_path_rel)

table_path_rel = "data/tables"
table_path_abs = os.path.join(script_dir,table_path_rel)

incomplete_season_per_league = {'standings_Argentina_Primera.csv': ('21', '22'), 
'standings_South_Korea_K-League_Classic.csv': ('20', '09', '14', '18', '17', '16', '21', '15', '19', '22', '11'), 
'standings_Spain_LaLiga_2.csv': ('10', '07', '08'), 
'standings_Turkey_Super_Lig.csv': ('13', '10', '14', '12', '11'), 
'standings_United_States_Major_League_Soccer.csv': ('20', '09', '18', '17', '10', '21', '12', '19', '22', '11')}

def get_fifa_filename(team_name,season_end):
    return f'{team_name}_FIFA_{season_end}.csv'

def get_team(team_name : str,season_end : str) -> Team:

    # Init team
    team : Team = Team(team_name,season_end)

    fn = get_fifa_filename(team_name,season_end)
    team_path = os.path.join(FIFA_path_abs,fn)
    start = True
    with open(team_path,encoding='utf-8') as f:
        csv_reader = csv.reader(f,delimiter=",")
        for row in csv_reader:

            # Skip header row
            if start:
                start = False
                continue

            # Get player attributes
            player_name, OVR, POT = row[0], row[1], row[2]
            player = Player(player_name,OVR,POT)
            team.add_player(player)
    team.sort_players()
    return team
            

league_examples = []

# Loop through all leagues
for league_filename in os.listdir(table_path_abs):
    ftable_path = os.path.join(table_path_abs,league_filename)
    start = True
    with open(ftable_path,encoding='utf-8') as f:
        csv_reader = csv.reader(f,delimiter=",")
        curr_season = ""
        curr_teams = []
        for row in csv_reader:
            # Skip header row
            if start:
                start = False
                continue
            team_name = row[0]
            team_pos = row[1]
            season = row[2]   
            season_end = season[-2:]

            # Skip incomplete examples
            if season_end == "23" or season_end == "24":
                continue
            if league_filename in incomplete_season_per_league:
                if season_end in incomplete_season_per_league[league_filename]:
                    continue
            
            # Add fully gathered example
            # Init for next season
            if season != curr_season:
                if len(curr_teams) > 0:
                    curr_league = League(league_filename,curr_season)
                    curr_league.teamRanking = curr_teams
                    league_examples.append(curr_league)
                curr_season = season
                curr_teams = []
            
            # Get team composition
            curr_team = get_team(team_name,season_end)
            curr_teams.append(curr_team)

# Split in training and testing set 
nr_examples = len(league_examples)
third = nr_examples // 3
random.shuffle(league_examples)
test_set = league_examples[:third]
training_set = league_examples[third:] 



# print(len(test_set))
# print(len(training_set))
# print(len(league_examples))
    
datasets : dict[str,list[League]] = {
    "test" : test_set,
    "training" : training_set,
    "all" : league_examples
}


class FIFADataset(Dataset):

    def __init__(self, subset) -> None:
        self.subset = subset
        self.dataset = datasets[subset]

    def __len__(self):
        return len(self.dataset)

    def to_query(self,i : int) -> Query:
        self.dataset[i].teamRanking = self.dataset[i].teamRanking[:4]
        return self.dataset[i].to_query()

    def to_nr1_query(self,i:int) -> Query:
        self.dataset[i].teamRanking = self.dataset[i].teamRanking[:4]
        return self.dataset[i].to_nr1_query()

    def get(self, i : int) -> League:
        return self.dataset[i]
    

class MatchDataset():
    def __init__(self) -> None:
        super().__init__()
        self.dataset = []
        filename = os.path.join(script_dir,"data/matches_ch.csv")
        start = True
        with open(filename,encoding='utf-8') as f:
            csv_reader = csv.reader(f,delimiter=",")
            for row in csv_reader:
                if start:
                    start = False
                    continue
                season = row[0]   
                season_end = season[-2:]

                home_goals = row[1]
                away_goals = row[2]
                home_name = row[3]
                away_name = row[4]

                #  We don't care about draws
                if home_goals == away_goals:
                    continue
                if home_goals > away_goals:
                    result = "win"
                elif home_goals < away_goals:
                    result = "loss"

                # Some teams don't have fifa data
                try:
                    home_team = get_team(home_name,season_end)
                    away_team = get_team(away_name,season_end)
                except: 
                    continue

                # add neural predicate example
                self.dataset.append((home_team.getTeamOVRs()[:11] + away_team.getTeamOVRs()[:11],result))

    def shuffle(self):
        random.shuffle(self.dataset)
    
    def balance(self):
        count_w = 0
        count_l = 0
        for _ , result in self.dataset:
            if result == "win":
                count_w +=1
            if result == "loss":
                count_l +=1
        if count_w > count_l:
            target = (count_w - count_l) // 2
            for i in range(len(self.dataset)):
                example = self.dataset[i]
                OVRs , result = example
                if result == "win":
                    self.dataset[i] = (OVRs[11:] + OVRs[:11],"loss")
                    target -= 1
                if target == 0:
                    break
        
        elif count_w < count_l:
            target = (count_l - count_w) // 2
            for i in range(len(self.dataset)):
                example = self.dataset[i]
                OVRs , result = example
                if result == "loss":
                    self.dataset[i] = (OVRs[11:] + OVRs[:11],"win")
        self.shuffle()

