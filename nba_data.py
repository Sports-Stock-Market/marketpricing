from nba_api.stats.endpoints import leaguedashplayerstats, leaguedashteamstats, commonplayerinfo
from nba_api.stats.static import teams, players
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
import os.path
import pandas as pd
import csv
import datetime

headers = {
    'Origin': 'https://stats.nba.com',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.42 Safari/537.36',
    'Host': 'stats.nba.com', 
    'Accept': 'application/json, text/plain, */*', 
    'Accept-Language': 'en-US,en;q=0.5', 
    'Accept-Encoding': 'gzip, deflate, br', 
    'x-nba-stats-origin': 'stats', 
    'x-nba-stats-token': 'true', 
    'Connection': 'keep-alive', 
    'Referer': 'https://stats.nba.com/', 
    'Pragma': 'no-cache', 
    'Cache-Control': 'no-cache'
}

format_year = lambda yr: '{}-{}'.format(yr, str(yr+1)[-2:])
format_date = lambda date: '{}/{}/{}'.format(date.month, date.day, date.year)

def get_player_position(id):
    return commonplayerinfo.CommonPlayerInfo(id).get_data_frames()[0].iloc[0]['POSITION']

def teams_stats_from(yr, end_date):
    return leaguedashteamstats.LeagueDashTeamStats(measure_type_detailed_defense='Advanced', season=format_year(yr), date_to_nullable=format_date(end_date), headers=headers).get_data_frames()[0]

def new_season_schedule_csv(end_yr):
    path = './schedules/{}_schedule.csv'.format(format_year(end_yr-1))
    client.season_schedule(season_end_year=end_yr, output_type=OutputType.CSV, output_file_path=path)

def get_season_schedule(end_yr):
    path = './schedules/{}_schedule.csv'.format(format_year(end_yr-1))
    if not os.path.isfile(path):
        new_season_schedule_csv(end_yr)
    return pd.read_csv(path)

teams_basic = leaguedashteamstats.LeagueDashTeamStats(headers=headers).get_data_frames()[0]
teams_advanced = leaguedashteamstats.LeagueDashTeamStats(measure_type_detailed_defense='Advanced', headers=headers).get_data_frames()[0]

players_basic = leaguedashplayerstats.LeagueDashPlayerStats(headers=headers).get_data_frames()[0]
players_advanced = leaguedashplayerstats.LeagueDashPlayerStats(measure_type_detailed_defense='Advanced', headers=headers).get_data_frames()[0]
players_raptor = pd.read_csv('./player_info/latest_RAPTOR_by_player.csv')