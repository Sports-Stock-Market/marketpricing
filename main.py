import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import nba
import nba_data

season = nba.Season(2011)
for i in range(len(season.dates)):
    for j in range(i, len(season.dates)):
        for game in season.games[season.dates[j]]:
            game.predict()
    for index, row in season.stats[season.dates[i]].iterrows():
        team = nba.find_team(season.teams, row['TEAM_NAME'])
        team.update_info()
        team.update_rating()