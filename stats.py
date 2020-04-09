from nba_api.stats.endpoints import leaguedashplayerstats, leaguedashteamstats, commonplayerinfo
from nba_api.stats.static import teams, players
import pandas as pd
import csv

def get_player_position(id):
    return commonplayerinfo.CommonPlayerInfo(id).get_data_frames()[0].iloc[0]['POSITION']

teams_basic = leaguedashteamstats.LeagueDashTeamStats().get_data_frames()[0]
teams_advanced = leaguedashteamstats.LeagueDashTeamStats(measure_type_detailed_defense='Advanced').get_data_frames()[0]

players_basic = leaguedashplayerstats.LeagueDashPlayerStats().get_data_frames()[0]
players_advanced = leaguedashplayerstats.LeagueDashPlayerStats(measure_type_detailed_defense='Advanced').get_data_frames()[0]