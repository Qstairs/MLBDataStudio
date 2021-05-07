import os

from models.Player import Player

def get_players(data):
    players = []
    for playerxml in data.iter('player'):
        player = Player(playerxml.attrib)
        players.append(player)

    return players