import numpy as np
import pandas as pd
import nba_data

class Player:
    def __init__(self, id, team, info_df=nba_data.players_advanced, raptor_df=nba_data.players_raptor):
        self.id = id
        self.info = info_df.loc[info_df['PLAYER_ID'] == self.id]
        self.first_name = self.info['PLAYER_NAME'].split()[0]
        self.last_name = self.info['PLAYER_NAME'].split()[1]
        self.teamid = self.info['TEAM_ID']
        self.mpg = self.info['MIN']
        self.adv = raptor_df.loc[raptor_df['Player_name'] == self.first_name + ' ' + self.last_name]
        self.raptor = {
            'offense': self.adv['Raptor_offense'],
            'defense': self.adv['Raptor_defense'],
            'total': self.adv['Raptor_total']
        }
        self.war = self.adv_stats['War_total']
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

    def __init__(self, id, players):
        self.id = id
        self.info = df.loc[df['TEAM_ID'] == self.id]
        self.city = self.info['TEAM_ID'].split()[0]
        self.name = self.info['TEAM_ID'].split()[1]
        self.players = players
        self.curr_rating = self.update_rating()
        self.proj_rating = self.update_rating(proj=True)
        self.raptor = {
            'offense': 0,
            'defense': 0,
            'total': 0
        }
        self.update_all_raptor()

    def update_info(self, df=df=nba_data.teams_advanced):
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
    pass

def init_teams(players, df=nba_data.teams_advanced):
    pass