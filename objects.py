import numpy as np
import pandas as pd
import nba_data

class Player:
    def __init__(self, info_row, raptor_df=nba_data.players_raptor):
        self.info = info_row
        self.id = self.info['PLAYER_ID']
        self.name = self.info['PLAYER_NAME']
        self.first_name = self.name.split()[0]
        self.last_name = self.name.split()[1]
        self.team_id = self.info['TEAM_ID']
        self.team = None
        self.mpg = self.info['MIN']
        self.adv = raptor_df.loc[raptor_df['player_name'] == self.first_name + ' ' + self.last_name]
        self.raptor = {
            'offense': self.adv['raptor_offense'],
            'defense': self.adv['raptor_defense'],
            'total': self.adv['raptor_total']
        }
        self.war = self.adv['war_total']
        self.status = True
    
    def injury(self, duration):
        self.status = False
        self.team.update_all_raptor()
        
class Team:
    curr_stats = {
        'W_PCT': [5, 0],
        'NET_RATING': [3, 0],
        'OFF_RATING': [4, 0],
        'DEF_RATING': [3, 0],
        'PIE': [5, 0]
    }

    proj_stats = {
        'W_PCT': [4, 0],
        'OFF_RATING': [3, 0],
        'DEF_RATING': [2, 0]
    }

    def __init__(self, players, info_row):
        self.info = info_row
        self.id = info_df['TEAM_ID']
        self.city = self.info['TEAM_NAME'].split()[0]
        self.name = self.info['TEAM_NAME'].split()[1]
        self.players = players
        self.curr_rating = self.update_curr_rating()
        self.raptor = {
            'offense': 0,
            'defense': 0,
            'total': 0
        }
        self.update_all_raptor()

    def update_info(self, df=nba_data.teams_advanced):
        self.info = df.loc[df['TEAM_ID'] == self.id]

    def update_curr_rating(self):
        cls.update_max_stats()
        self.update_info()
        weight = lambda a_dict, key: a_dict[key][0] * (self.info[key]/a_dict[key][1])
        self.rating = 3*sum([weight(self.curr_stats, stat) for stat in self.curr_stats]) 
        return self.rating

    def update_raptor(self, category):
        self.raptor[category] = sum([player.raptor[category] for player in players if player.status])
        return self.raptor[category]
    
    def update_all_raptor(self):
        for category in self.raptor:
            self.update_raptor(category)
        return self.raptor

    @classmethod
    def update_max_stats(cls, df=nba_data.teams_advanced):
        for stat in cls.curr_stats:
            cls.curr_stats[stat][1] = df[stat].max()
        return cls.curr_stats

def trade(p1, p2):
    team1 = p1.team
    team2 = p2.team
    team1.players[team1.players.index(p1)] = p2
    team2.players[team2.players.index(p2)] = p1
    p1.team = p2.team
    p2.team = team1

def init_players(df=nba_data.players_advanced):
    return [Player(row) for index, row in df.iterrows()]

def init_teams(players, df=nba_data.teams_advanced):
    teams = []
    for index, row in df.iterrows():
        team_players = list(filter(lambda x: x.team_id == row['TEAM_ID'], players))
        teams.append(Team(team_players, row))
    return teams