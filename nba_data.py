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

format_year = lambda yr: '{}-{}'.format(yr-1, str(yr)[-2:])
format_date = lambda date: '{}/{}/{}'.format(date.month, date.day, date.year)

def get_player_position(id):
    return commonplayerinfo.CommonPlayerInfo(id).get_data_frames()[0].iloc[0]['POSITION']

def teams_stats_from(end_yr, end_date=''):
    if end_date:
        end_date = format_date(end_date)
    return leaguedashteamstats.LeagueDashTeamStats(measure_type_detailed_defense='Advanced', season=format_year(end_yr), date_to_nullable=end_date, headers=headers).get_data_frames()[0]

def get_team_projections(end_yr):
    path = './team_info/{}_projections.csv'.format(format_year(end_yr))
    return pd.read_csv(path)

def players_stats_from(end_yr, end_date=''):
    if end_date:
        end_date = format_date(end_date)
    return leaguedashplayerstats.LeagueDashPlayerStats(measure_type_detailed_defense='Advanced', season=format_year(end_yr), date_to_nullable=end_date, headers=headers).get_data_frames()[0]

def raptor_from(end_yr):
    df = pd.read_csv('./player_info/raptors.csv')
    return df.loc[df['season'] == end_yr-1]

def new_schedule_csv(end_yr):
    path = './schedules/{}_schedule.csv'.format(format_year(end_yr))
    client.season_schedule(season_end_year=end_yr, output_type=OutputType.CSV, output_file_path=path)

def get_schedule(end_yr):
    path = './schedules/{}_schedule.csv'.format(format_year(end_yr))
    if not os.path.isfile(path):
        new_schedule_csv(end_yr)
    return pd.read_csv(path)

def get_injuries(end_yr):
    path = './injuries/{}.csv'.format(format_year(end_yr))
    return pd.read_csv(path)

def get_trades(end_yr):
    path = './team_info/{}.csv'.format(format_year(end_yr))
    return pd.read_csv(path)