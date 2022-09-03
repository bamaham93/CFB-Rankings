import json
import csv
from config import year
from checkScheduleIntegrity import ScheduleCheck

# year = 2021

############################################################
# Import JSON Files

# Teams file
f = open('data/teams/' + str(year) + 'teams.json')
team_dict = json.load(f)

# Games file
f = open('data/games/' + str(year) + 'games.json')
game_dict = json.load(f)

############################################################
################## Compile Team Schedules ##################

# Define everything here
team_schedules = [] # Used to hold list of team schedules
teams = [] # Used in filtering FBS teams
games = [] # Used in compiling game data for each team

############################################################
# Functions

# 1 win, 0 loss
def game_result(home, game):
  if home == 1:
    if game['_home_points'] > game['_away_points']:
      return 1
    else:
      return 0
  else:
    if game['_home_points'] > game['_away_points']:
      return 0
    else:
      return 1

# 0.5 neutral site, 1 home, 0 away
def determine_location(team, game):
  if game['_neutral_site'] == True:
    return 0.5
  elif game['_home_team'] == team:
    return 1
  else:
    return 0

def completed_game(game):
  if game['_home_points'] == None or game['_away_points'] == None:
    return False
  else:
    return True

############################################################
############################################################
# Compile data for each team

for team in team_dict:
  team_data = {}
  team_data['id'] = team['id']
  team_data['team'] = team['team']
  team_data['year'] = year
  team_data['classification'] = team['classification']
  team_data['conference'] = team['conference']
  team_data['reg_game_data'] = []
  team_data['post_game_data'] = []

  for game in game_dict:
    if completed_game(game):
      if game['_home_team'] == team['team'] or game['_away_team'] == team['team']:
        game_data = {}
        game_data['week'] = game['_week']

        if game['_home_team'] == team['team']:
          game_data['opp'] = game['_away_team']
          game_data['team_score'] = game['_home_points']
          game_data['opp_score'] = game['_away_points']
          game_data['result'] = game_result(1, game)
        else:
          game_data['opp'] = game['_home_team']
          game_data['team_score'] = game['_away_points']
          game_data['opp_score'] = game['_home_points']
          game_data['result'] = game_result(0, game)
        game_data['loc'] = determine_location(team['team'], game)
        game_data['season_type'] = game['_season_type']
        if game_data['season_type'] == 'regular':
          team_data['reg_game_data'].append(game_data)
        else:
          team_data['post_game_data'].append(game_data)
  team_schedules.append(team_data)

#########################################################
# Eliminate teams with no game data
sched_list_a = []

for sched in team_schedules:
  if sched['reg_game_data'] != []:
    sched_list_a.append(sched)

#########################################################
# Ensure week 0 games display correctly
for team in team_schedules:
  try:
    if team['reg_game_data'][0]['week'] == 1 and team['reg_game_data'][1]['week'] == 1:
      team['reg_game_data'][0]['week'] = 0
  except:
    continue

#########################################################
# Insert NULL game for BYE week

# Formula to check if team has a game each week and insert null games
def check_week(x, team):
  null_game_reg_a = {
  'week' : x,
  "opp" : 0,
  "team_score" : 0,
  "opp_score" : 0,
  "result" : 0,
  "loc" : 0,
  'season_type' : 'regular'
}
  try:
    if team['reg_game_data'][x]['week'] != x and team['reg_game_data'][x]['season_type'] != 'postseason':
      team['reg_game_data'].insert(x, null_game_reg_a)
  except:
    exit

for team in sched_list_a:
  n = 0
  while n < 20:
    check_week(n, team)
    n = n + 1

#########################################################
# Add null games up to 15 games per team

for team in sched_list_a:
  def insert_game(x, team):
    null_game_reg_b = {
    'week': x,
    "opp": 0,
    "team_score": 0,
    "opp_score": 0,
    "result": 0,
    "loc": 0,
    'season_type': 'regular'
    }
    team['reg_game_data'].append(null_game_reg_b)

  season_length = len(team['reg_game_data'])
  if season_length < 16:
    # x = 16 - season_length
    for i in range(season_length, 16):
      insert_game(i, team)

#########################################################
# WRITE TO JSON FILE

json_object = json.dumps(sched_list_a, indent=4)

with open('data/schedules/' + str(year) + 'schedules.json', 'w') as outfile:
  outfile.write(json_object)


#########################################################
# Runs data integrity checks

checks  = ScheduleCheck()
checks.run()

#########################################################
# OPEN JSON FILE
# Schedules file
f = open('data/schedules/' + str(year) + 'schedules.json')
schedules_dict = json.load(f)



#########################################################
# Prep data for CSV format
CSV_team_data = []

for team in schedules_dict:
  team_csv_data = []
  # print(f"{team}\n")
  team_csv_data.append(team['id'])
  team_csv_data.append(team['team'])
  team_csv_data.append(team['year'])
  team_csv_data.append(team['classification'])
  team_csv_data.append(team['conference'])

  for game in team['reg_game_data']:
    for k in game:
      team_csv_data.append(game[k])

  CSV_team_data.append(team_csv_data)

# print(len(CSV_team_data))

#########################################################
# WRITE TO CSV FILE
csv_columns = ['id', 'team', 'year', 'classification', 'division', 'conference']

game_columns = ['week', 'opp', 'team score', 'opp score', 'result', 'location', 'season type']

for i in range(18):
  for item in game_columns:
    csv_columns.append(item)

with open('data/excel/' + str(year) + 'data.csv', 'w', newline='') as f:
  write = csv.writer(f)

  write.writerow(csv_columns)
  write.writerows(CSV_team_data)