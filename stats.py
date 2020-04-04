from nba_api.stats.endpoints import leaguedashplayerstats, leaguedashteamstats, commonplayerinfo
from nba_api.stats.static import teams, players

teams = leaguedashteamstats.LeagueDashTeamStats(measure_type_detailed_defense='Advanced')
players = leaguedashplayerstats.LeagueDashPlayerStats(measure_type_detailed_defense='Advanced').get_data_frames()[0]

def get_player_position(id):
    return commonplayerinfo.CommonPlayerInfo(id).get_data_frames()[0].iloc[0]['POSITION']
