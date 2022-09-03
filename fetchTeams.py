import cfbd
from cfbd.rest import ApiException
import json

######################## MAKE SURE YOU DEFINE THE YEAR ########################
year = 2021
######################## MAKE SURE YOU DEFINE THE YEAR ########################

api_key = 'kf4KXdtp2JFvq+7wy4yipT75+3mcVzeTl56SvjdONO3cdEksOHxWuZdPf2fB92hl'

configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = api_key
configuration.api_key_prefix['Authorization'] = 'Bearer'

teams_api_instance = cfbd.TeamsApi(cfbd.ApiClient(configuration))

############################### BEGIN API CALLS ###############################

# Gets list of all teams and write to JSON
try:
    # Team information
    get_teams_api_response = teams_api_instance.get_teams()
    team_list = get_teams_api_response
except ApiException as e:
    print("Error accessing TeamsApi->get_teams: %s\n" % e)

team_dict_list = []

for team in team_list:
  team_dict = {}
  team_dict['id'] = team.id
  team_dict['team'] = team.school
  team_dict['classification'] = team.classification
  team_dict['conference'] = team.conference
  team_dict_list.append(team_dict)

#########################################################
# WRITE TEAMS TO JSON FILE
json_object = json.dumps(team_dict_list, indent=4)
file_path = ""

with open('data/teams/' + str(year) + 'teams.json', 'w') as outfile:
  outfile.write(json_object)