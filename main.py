import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import nba
import nba_data

def simulate(end_yr, num_games):
    season = nba.Season(end_yr, num_games)
    for curr in range(len(season.dates)):
        if season.dates[curr] in season.injuries:
            injury = season.injuries[season.dates[curr]]
            inj_team = nba.find(season.teams, injury[0])
            inj_team.injury(injury[1], season.dates[curr], injury[2])
        # if season.dates[curr] in season.trades:
        #     trade = season.trades[season.dates[curr]]
        #     team1 = nba.find(season.teams, trade[0])
        #     team2 = nba.find(season.teams, trade[1])
        #     nba.trade(nba.find(team1.players, trade[2]), nba.find(team2.players, trade[3]))
        for index, row in season.stats[season.dates[curr]].iterrows():
            nba.find(season.teams, row['TEAM_NAME']).update_stats(row)
        for date in season.dates[curr:]:
            for game in season.games[date]:
                game.predict()
        for team in season.teams:
            team.update_wins()   
            nba.Team.update_avg_stats(season.teams)
            team.calc_rating()
    ratings = {}
    for team in season.teams:
        ratings[team.full_name] = team.all_ratings
    return [list(map(nba_data.format_date, season.dates)), ratings]

def win_predictor(end_yr):
    season = nba.Season(end_yr)
    total = 0
    correct = 0
    for date in season.dates:
        for game in season.games[date]:
            total +=1
            if game.winner == game.predict():
                correct += 1
            print([game.winner, game.predict()])
    return(correct/total)

dates, ratings = simulate(2012, 66)
dates.append('last')
for team in list(ratings.keys()):
    plt.plot(dates, ratings[team], label=team)
plt.xticks(rotation=90, fontsize=8)
plt.legend()
plt.show()