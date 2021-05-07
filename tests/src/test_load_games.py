import sys

import pytest
import xml.etree.ElementTree as ET

sys.path.append("./src")
from load_games import *

def download_inningdata():
    path = "testdata\scoreboard.xml"
    tree = ET.parse(path)
    return tree

def test_get_games():
    data = download_inningdata()
    games = get_games(data)

    assert len(games) == 15

    for game in games:
        print(game)

