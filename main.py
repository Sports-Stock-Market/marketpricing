import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import nba
import nba_data

def simulate(end_yr):
    season = nba.Season(end_yr)
    for curr in range(len(season.dates)):
        # for index, row in season.stats[season.dates[curr]].iterrows():
        #     nba.find(season.teams, row['TEAM_NAME']).update_stats(row)
        for date in season.dates[curr:]:
                for game in season.games[date]:
                    game.predict() 
        for team in season.teams:
            team.update_wins()   
            team.calc_rating()
    ratings = {}
    for team in season.teams:
        ratings[team.full_name] = team.all_ratings
    return ratings

def win_predictor(end_yr):
    season = Season(2014)
    total = 0
    correct = 0
    for date in season.dates:
        for game in season.games[date]:
            total +=1
            if game.winner == game.predict():
                correct += 1
            print([game.winner, game.predict()])
    return(correct/total)
