import pandas as pd
import sqlite3
import os
script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir,"database.sqlite")
target_path = os.path.join(script_dir,"matches.csv")
cnx = sqlite3.connect(data_path)
df = pd.read_sql_query("SELECT season, home_team_goal, away_team_goal, ht.team_long_name AS home_name, at.team_long_name AS away_name FROM Match, Team AS at, Team AS ht WHERE ht.team_api_id = home_team_api_id AND at.team_api_id = away_team_api_id", cnx)
print(df)
df.to_csv(target_path,index = False)