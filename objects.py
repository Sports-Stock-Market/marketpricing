import numpy as np
import pandas as pd
import nba_data

class Player:
    def __init__(self, id, team, df=nba_data.players_advanced, csv='latest_RAPTOR_by_player'):
        self.id
        self.first_name
        self.last_name
        self.raptor
        self.war
        self.status
        self.team
        self.minutes
    
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
        self.players = players
        self.curr_rating = self.update_rating()
        self.proj_rating = self.update_rating(proj=True)
        self.raptor = {}

    def update_rating(self, proj=False, df=nba_data.teams_advanced):
        stats = curr_stats if time == False else stats = proj_stats
        self.rating = 3*sum([stats[stat][0]*(row[stat]/stats[stat][1])]) 
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
        return cls.main_stats

def trade(p1, p2):
    team1 = p1.team
    team2 = p2.team
    team1.players[team1.players.index(p1)] = p2
    team2.players[team2.players.index(p2)] = p1
    p1.team = p2.team
    p2.team = team1
    