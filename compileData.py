import json
from tkinter import W

year = 2021

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
  null_game_reg = {
  'week' : x,
  "opp" : None,
  "team_score" : None,
  "opp_score" : None,
  "result" : None,
  "loc" : None,
  'season_type' : 'regular'
}
  try:
    if team['reg_game_data'][x]['week'] != x and team['reg_game_data'][x]['season_type'] != 'postseason':
      team['reg_game_data'].insert(x, null_game_reg)
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
  null_game_reg = {
  'week' : None,
  "opp" : None,
  "team_score" : None,
  "opp_score" : None,
  "result" : None,
  "loc" : None,
  'season_type' : 'regular'
}
  season_length = len(team['reg_game_data'])
  if season_length < 16:
    x = 16 - season_length
    for i in range(x):
      null_game_reg['week'] = season_length
      team['reg_game_data'].append(null_game_reg)
      


#########################################################
# WRITE TO JSON FILE

json_object = json.dumps(sched_list_a, indent=4)

with open('data/schedules/' + str(year) + 'schedules.json', 'w') as outfile:
  outfile.write(json_object)