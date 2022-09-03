from __future__ import print_function
import time
import cfbd
from cfbd.rest import ApiException
from pprint import pprint


api_key = 'kf4KXdtp2JFvq+7wy4yipT75+3mcVzeTl56SvjdONO3cdEksOHxWuZdPf2fB92hl'

configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = api_key
configuration.api_key_prefix['Authorization'] = 'Bearer'

api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))

year = 2021
team = 'Alabama'

try:
  api_response = api_instance.get_team_records(year=year)
  record_list = api_response
except ApiException as e:
  print("Error accessing game info: %s\n" % e)

class TeamRecord:
  def __init__(self, team, conf):
    self.team = team
    self.conf = conf

team_info_list = []

for record_class in record_list:
  team = TeamRecord(record_class.team, record_class.conference)
  team.games = record_class.total['games']
  team.wins = record_class.total['wins']
  team.losses = record_class.total['losses']
  team_info_list.append(team)

for team in team_info_list:
  if(team.team == "Alabama"):
    print(vars(team))