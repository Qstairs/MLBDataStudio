import sys

import pytest
import xml.etree.ElementTree as ET

sys.path.append("./src")
from load_players import *

def download_players():
    path = "testdata\players.xml"
    tree = ET.parse(path)
    return tree

def test_get_players():
    data = download_players()
    players = get_players(data)

    assert len(players) == 56

    for player in players:
        print(player)

