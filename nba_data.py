from nba_api.stats.endpoints import leaguedashplayerstats, leaguedashteamstats, commonplayerinfo
from nba_api.stats.static import teams, players
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

def get_player_position(id):
    return commonplayerinfo.CommonPlayerInfo(id).get_data_frames()[0].iloc[0]['POSITION']

def teams_stats_from(yr, end_date):
    return leaguedashteamstats.LeagueDashTeamStats(measure_type_detailed_defense='Advanced', season=yr, date_to_nullable=end_date, headers=headers).get_data_frames()[0]

def format_date(date):
    return('{}/{}/{}'.format(date.month, date.day, date.year))

teams_basic = leaguedashteamstats.LeagueDashTeamStats(headers=headers).get_data_frames()[0]
teams_advanced = leaguedashteamstats.LeagueDashTeamStats(measure_type_detailed_defense='Advanced', headers=headers).get_data_frames()[0]

players_basic = leaguedashplayerstats.LeagueDashPlayerStats(headers=headers).get_data_frames()[0]
players_advanced = leaguedashplayerstats.LeagueDashPlayerStats(measure_type_detailed_defense='Advanced', headers=headers).get_data_frames()[0]
players_raptor = pd.read_csv('latest_RAPTOR_by_player.csv')

yr = 2001
formatted_yr = '{}-{}'.format(yr, str(yr+1)[-2:])

start = datetime.date(2001, 11, 21)
end_dates = [format_date(start+datetime.timedelta(days=(10*step))) for step in range(20)]
year_stats = [teams_stats_from(formatted_yr, date) for date in end_dates]