import cfbd
from cfbd.rest import ApiException
import json

######################## MAKE SURE YOU DEFINE THE YEAR ########################
year = 2022
######################## MAKE SURE YOU DEFINE THE YEAR ########################

api_key = 'kf4KXdtp2JFvq+7wy4yipT75+3mcVzeTl56SvjdONO3cdEksOHxWuZdPf2fB92hl'

configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = api_key
configuration.api_key_prefix['Authorization'] = 'Bearer'

games_api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))

############################### BEGIN API CALLS ###############################

#########################################################
# CALL TO API FOR GAME DATA
try:
  get_games_api_response = games_api_instance.get_games(year=year, season_type="regular")
  game_list = get_games_api_response
except ApiException as e:
  print("Error accessing game info: %s\n" % e)

try:
  get_games_api_response = games_api_instance.get_games(year=year, season_type="postseason")
  for game_item in get_games_api_response:
    game_list.append(game_item)

except ApiException as e:
  print("Error accessing game info: %s\n" % e)

#########################################################
# Prep data for json format
modded_data = []

for game in game_list:
  game_data = vars(game)
  del game_data['_configuration']
  modded_data.append(game_data)

#########################################################
# WRITE TO JSON FILE

json_object = json.dumps(modded_data, indent=4)

with open('data/games/' + str(year) + 'games.json', 'w') as outfile:
  outfile.write(json_object)