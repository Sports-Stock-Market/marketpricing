import numpy as np
import pandas as pd
import stats

def normalize(n):
    if n < 0:
        raise Exception("negative value used")
    return np.log(n) ** 3

def guard_rating(row):
    return row['USG_PCT']*(row['PIE']+((row['NET_RATING']/2)+((row['AST_PCT']+row['REB_PCT'])/12)))

def forward_rating(row):
    return row['USG_PCT']*(row['PIE']+((row['NET_RATING']/2)+((row['AST_PCT']+row['REB_PCT'])/10)))

def center_rating(row):
    return row['USG_PCT']*(row['PIE']+((row['NET_RATING']/2)+(((row['AST_PCT']/2)+(row['REB_PCT']*2.25))/12)))


player_ratings = {}

for index, row in stats.players.iterrows():
    pos = stats.get_player_position(row['PLAYER_ID'])
    if pos == "Guard":
        rating = guard_rating(row)
    elif pos == "Forward" or "Forward-Guard":
        rating = forward_rating(row)
    else:
        rating = center_rating(row)
    player_ratings[row['PLAYER_ID']] = normalize(rating)

