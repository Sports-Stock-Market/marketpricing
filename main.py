import numpy as np
import pandas as pd
import stats

team_stat_weights = {
    'W_PCT': 5,
    'NET_RATING': 3,
    'OFF_RATING': 4,
    'DEF_RATING': 3,
    'EFG_PCT': 2,
    'TS_PCT': 2,
    'PIE': 5
}

def find_max_team_stats():
    for stat in team_stat_weights:
        team_stat_weights[stat] = [team_stat_weights[stat], stats.teams_advanced[stat].max()]

def normalize(n, stat_type):
    if n < 0:
        raise ValueError("rating cannot be negative")
    if stat_type == 'player':
        return np.log(n)**3
    elif stat_type == 'team':
        return n*3
    else:
        raise ValueError("argument stat_type must be either 'player' or 'team'")

def guard_rating(row):
    return row['USG_PCT']*(row['PIE']+((row['NET_RATING']/2)+((row['AST_PCT']+row['REB_PCT'])/12)))

def forward_rating(row):
    return row['USG_PCT']*(row['PIE']+((row['NET_RATING']/2)+((row['AST_PCT']+row['REB_PCT'])/10)))

def center_rating(row):
    return row['USG_PCT']*(row['PIE']+((row['NET_RATING']/2)+(((row['AST_PCT']/2)+(row['REB_PCT']*2.25))/12)))

def update_team_ratings():
    team_ratings = {}
    find_max_team_stats()
    for index, row in stats.teams_advanced.iterrows():
        rating = 0
        for stat in team_stat_weights:
            if stat == 'NET_RATING':
                rating += team_stat_weights[stat][0]*(row[stat]+10)/(team_stat_weights[stat][1]+10)
            else:
                rating += team_stat_weights[stat][0]*(row[stat]/team_stat_weights[stat][1])
        team_ratings[row['TEAM_ID']] = normalize(rating, 'team')
    return team_ratings

def update_player_ratings():
    player_ratings = {}
    for index, row in stats.players_advanced.iterrows():
        pos = stats.get_player_position(row['PLAYER_ID'])
        if pos == "Guard":
            rating = guard_rating(row)
        elif pos == "Forward" or "Forward-Guard":
            rating = forward_rating(row)
        else:
            rating = center_rating(row)
        player_ratings[row['PLAYER_ID']] = [normalize(rating, 'player'), row['TEAM_ID']]

