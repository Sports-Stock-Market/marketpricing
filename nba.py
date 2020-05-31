import numpy as np
import pandas as pd
from scipy.stats import norm
import math
import datetime
import string
import nba_data

class Player:
    def __init__(self, info_row, raptor_df):
        self.info = info_row
        self.id = self.info['PLAYER_ID']
        self.full_name = self.info['PLAYER_NAME']
        if len(self.full_name.split()) > 1:
            self.first_name = self.full_name.split()[0]
            if len(self.full_name.split()[1:]) > 1:
                self.last_name = ' '.join(self.full_name.split()[1:])
            else:
                self.last_name = self.full_name.split()[1]
        else:
            self.first_name = ''
            self.last_name = self.full_name
        self.team_id = self.info['TEAM_ID']
        self.team = None
        self.mpg = self.info['MIN']
        self.adv = raptor_df.loc[raptor_df['player_name'] == self.full_name]
        self.raptor = {
            'offense': 0,
            'defense': 0,
            'total': 0
        }
        for category in self.raptor:
            stat = self.adv['raptor_{}'.format(category)].values
            if len(stat) > 0:
                self.raptor[category] = stat[0]
        self.war = self.adv['war_total']
        self.status = True
    
    def __str__(self):
        return self.full_name

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.full_name == other.full_name
    
    def __lt__(self, other):
        if self.last_name == other.last_name:
            return self.first_name < other.first_name
        return self.last_name < other.last_name

    def injury(self):
        self.status = False
        self.team.update_all_raptor()
        
class Team:
    stat_weights = {
        'W_PCT': [0.5, 1],
        # 'OFF_RATING': 0.2,
        # 'DEF_RATING': 0.2,
        'NET_RATING': [0.3, 1],
        'PIE': [0.2, 1]
    }
    max_raptor = 0

    def __init__(self, players, info_row, proj):
        self.info = info_row
        self.id = self.info['TEAM_ID']
        self.full_name = self.info['TEAM_NAME']
        city_len = len(self.full_name.split()[::-1][1:])
        self.city = self.full_name.split()[:city_len]
        if city_len > 1:
            self.city = " ".join(self.city)
        else:
            self.city = self.city[0]
        self.name = self.full_name.split()[city_len]
        self.players = players
        self.rating = round((6*(proj/47.5)-1), 2)
        self.raptor = {
            'offense': 0,
            'defense': 0,
            'total': 0
        }
        self.stats = {
            'W_PCT': proj/66,
            'OFF_RATING': 100,
            'DEF_RATING': 100,
            'NET_RATING': 0,
            'PIE': self.info['PIE']
        }
        self.calc_raptor()
        self.updated = 0
        self.proj_wins = 0
        self.proj_games = 0
        self.all_ratings = [self.rating]

    def __str__(self):
        return self.full_name

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.full_name == other.full_name
    
    def __lt__(self, other):
        return self.full_name < other.full_name

    def update_stats(self, row):
        self.updated += 1
        self.info = row
        self.stats['OFF_RATING'] = self.info['OFF_RATING'] #+ self.raptor['offense']
        self.stats['DEF_RATING'] = self.info['DEF_RATING'] #+ self.raptor['defense']
        self.stats['NET_RATING'] = self.info['NET_RATING'] + 10#+ self.raptor['total']
        self.stats['PIE'] = self.info['PIE']

    def update_wins(self):
        if self.updated > 0:
            self.stats['W_PCT'] = (self.info['W'] + self.proj_wins)/(self.info['GP'] + self.proj_games)
        # print(self.stats['W_PCT'])

    def calc_rating(self):
        weight = lambda stat: Team.stat_weights[stat][0] * (self.stats[stat]/Team.stat_weights[stat][1])
        # prev_percent = 0.5*math.exp((-1/8)*self.info['GP'])
        # normalized = (1-raptor_percent)*(sum([weight(stat) for stat in Team.stat_weights])+10)
        # raptor_weight = raptor_percent*((self.raptor['total']/Team.max_raptor)+10)
        # self.rating = round(3*(normalized + raptor_weight), 2)
        # self.rating = round(sum([weight(stat) for stat in Team.stat_weights])+10, 2)
        new_rating = sum([weight(stat) for stat in Team.stat_weights])
        # print(self, self.stats, new_rating)
        # self.rating = round(3*((prev_percent*self.all_ratings[-1]) + ((1-prev_percent)*new_rating)), 2)
        self.rating = round(3*(0.2*self.all_ratings[-1] + 0.8*new_rating), 2)
        self.all_ratings.append(self.rating)
        self.proj_wins = 0
        self.proj_games = 0
        return self.rating
    
    def calc_raptor(self):
        for category in self.raptor:
            mpg_weight = lambda mpg: mpg**(1/4)
            self.raptor[category] = sum([player.raptor[category]*mpg_weight(player.mpg) for player in self.players if player.status])
        return self.raptor
    
    @classmethod
    def update_max_stats(cls, teams):
        for stat in cls.stat_weights:
            max_stat = -100
            max_raptor = -100
            for team in teams:
                if team.stats[stat] > max_stat:
                    max_stat = team.stats[stat]
                if team.raptor['total'] > max_raptor:
                    max_raptor = team.raptor['total']
            cls.stat_weights[stat][1] = max_stat
            cls.max_raptor = max_raptor

class Game:
    def __init__(self, date, home_team, away_team, home_score, away_score):
        self.date = date
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score
        self.winner = self.home_team if home_score > away_score else self.away_team
    
    def __str__(self):
        return '{} @ {}, {}'.format(self.away_team, self.home_team, nba_data.format_date(self.date))
                
    def __repr__(self):
        return str(self)

    def includes(self, team):
        return team == self.home_team or team == self.away_team
        
    def predict(self):
        # es_home = (self.home_team.stats['OFF_RATING'] + self.away_team.stats['DEF_RATING'])/2
        # es_away = (self.away_team.stats['OFF_RATING'] + self.home_team.stats['DEF_RATING'])/2
        es_home = self.home_team.stats['NET_RATING']
        es_away = self.away_team.stats['NET_RATING']
        margin = es_home - es_away
        vary = self.home_team.info['W_PCT'] - self.away_team.info['W_PCT']
        std = ((-2/10) * vary) + 14
        win_prob = norm.cdf(0, loc=margin, scale=std)
        self.home_team.proj_games += 1
        self.away_team.proj_games += 1
        self.home_team.proj_wins += 1-win_prob
        self.away_team.proj_wins += win_prob
        return win_prob

 
class Season:
    def __init__(self, end_yr, num_games=82):
        self.schedule = nba_data.get_season_schedule(end_yr)
        self.yr = end_yr
        self.teams = init_teams(end_yr)
        self.dates = []
        self.games = {}
        self.stats = {}
        limit = num_games * 15
        for index, row in self.schedule.iterrows():
            if limit == 0:
                break
            date_info = list(map(int, row['start_time'][:10].split('-')))
            date = datetime.date(*date_info)             
            game = Game(date, find(self.teams, string.capwords(row['home_team'])), find(self.teams, string.capwords(row['away_team'])), row['home_team_score'], row['away_team_score'])
            if date not in self.dates:
                self.dates.append(date)
                self.games[date] = [game]
                self.stats[date] = nba_data.teams_stats_from(self.yr, date)
            else:
                self.games[date].append(game)
            limit -= 1
        
        # def has_game(self, name, date):
        #     team = find(self.teams, name)
        #     for game in self.games[date]:
        #         if game.includes(team):
        #             return True
        #     return False

def trade(p1, p2):
    team1 = p1.team
    team2 = p2.team
    team1.players[team1.players.index(p1)] = p2
    team2.players[team2.players.index(p2)] = p1
    p1.team = p2.team
    p2.team = team1

def init_players(end_yr):
    info_df = nba_data.players_stats_from(end_yr)
    raptor_df = nba_data.raptor_from(end_yr)
    return sorted([Player(row, raptor_df) for index, row in info_df.iterrows()])

def init_teams(end_yr):
    df = nba_data.teams_stats_from(end_yr)
    projs = nba_data.get_team_projections(end_yr)
    teams = []
    for index, row in df.iterrows():
        team_players = list(filter(lambda x: x.team_id == row['TEAM_ID'], init_players(end_yr)))
        proj = projs.loc[projs['Team'] == row['TEAM_NAME']]['W-L O/U'].values[0]
        team = Team(team_players, row, proj)
        for player in team.players:
            player.team = team
        teams.append(team)
    return sorted(teams)

def find(sorted_list, name):
    low = 0
    high = len(sorted_list) - 1
    while low <= high:
        middle = (low + high)//2
        if sorted_list[middle].full_name == name:
            return sorted_list[middle]
        elif sorted_list[middle].full_name > name:
            high = middle - 1
        else:
            low = middle + 1
    return -1

# season = Season(2012)
# Team.update_max_stats(season.teams)
# for team in season.teams:
#     print(team, team.raptor['total']/Team.max_raptor)