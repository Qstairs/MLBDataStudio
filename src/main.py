import os

import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation

try:
    from urllib.request import urlopen
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import urlopen, HTTPError

from load_inningdata import get_inning, get_pitch_by_pitch_per_atbat
from load_games import get_games
from load_players import get_players
from visualize.Pitch import course, pitch_history, pitcher_info, batter_info
from xmlio.parser import parse, parse_path
from xmlio.writer import writer as xmlwriter

HEIGHT = 720
WIDTH = 1280

def get_player(players, id):

    for player in players:
        if player.id == id:
            return player

    return None

def inning(atbat_list, players, dst_folder, top_bottom):
    for atbat in atbat_list:
        # pitch_by_pitch = get_pitch_by_pitch_per_atbat(atbat.num)
        pitch_by_pitch = atbat.pitch_by_pitch

        pitcher_id = atbat.pitcher
        batter_id = atbat.batter
        pitcher = get_player(players, pitcher_id)
        batter = get_player(players, batter_id)
        print("pitcher", pitcher)
        print("batter", batter)

        atbat_img = np.zeros((220,800,3), dtype=np.uint8)
        picthing_img = np.zeros((500,800,3), dtype=np.uint8)

        if top_bottom == "top":
            atbat_img = pitcher_info(atbat_img, pitcher, atbat.p_throws, True)
            atbat_img = batter_info(atbat_img, batter, atbat.stand, False)
        else:
            atbat_img = pitcher_info(atbat_img, pitcher, atbat.p_throws, False)
            atbat_img = batter_info(atbat_img, batter, atbat.stand, True)

        for idx, pitch in enumerate(pitch_by_pitch):
            # print(pitch)
            course(picthing_img, atbat, pitch)
            atbat_img = pitch_history(atbat_img, idx, pitch)

            img = cv2.vconcat([picthing_img, atbat_img])
            cv2.imshow("course", img)
            cv2.waitKey(100)

        os.makedirs(dst_folder, exist_ok=True)
        cv2.imwrite(os.path.join(dst_folder, f"{atbat.num:03d}.jpg"), img)

BASE_URL = 'http://gd2.mlb.com/components/game/mlb/year_{0}/month_{1:02d}/day_{2:02d}/'
GAME_URL = BASE_URL + 'gid_{3}/{4}'

BASE_PATH = './game/mlb/year_{0}/month_{1:02d}/day_{2:02d}/'
GAME_PATH = BASE_PATH + 'gid_{3}/{4}'

def download_xmldata(url):
    data = urlopen(url)
    data_str = data.read().decode("utf-8")
    xmldata = parse(data_str)
    return xmldata

def download_inningdata(year, month, day, game_id):
    path = GAME_PATH.format(year, month, day, game_id, 'inning/inning_all.xml')
    if os.path.exists(path):
        xmldata = parse_path(path)
    else:
        xmldata = download_xmldata(GAME_URL.format(year, month, day, game_id, 'inning/inning_all.xml'))
    xmlwriter(path, xmldata)

    inningdata = {}
    for i in range(1, 9+1):
        top_atbat_list, bot_atbat_list = get_inning(xmldata, i)
        inningdata[i] = {
            "top":top_atbat_list,
            "bottom":bot_atbat_list
        }
    
    return inningdata

def download_players(year, month, day, game_id):
    path = GAME_PATH.format(year, month, day, game_id, 'players.xml')
    if os.path.exists(path):
        xmldata = parse_path(path)
    else:
        xmldata = download_xmldata(GAME_URL.format(year, month, day, game_id, 'players.xml'))
    xmlwriter(path, xmldata)

    players = get_players(xmldata)
    return players

def download_games(year, month, day):
    path = BASE_PATH.format(year, month, day) + 'scoreboard.xml'
    if os.path.exists(path):
        xmldata = parse_path(path)
    else:
        xmldata = download_xmldata(BASE_URL.format(year, month, day) + 'scoreboard.xml')
    xmlwriter(path, xmldata)

    games = get_games(xmldata)
    return games

if __name__ == "__main__":
    year = 2021
    month = 5
    day = 5

    games = download_games(year, month, day)

    for game in games:
        players = download_players(year, month, day, game.game_id)
        inningdata = download_inningdata(year, month, day, game.game_id)
        dst_folder = f"dst_atbat/{game.game_id}"
        for i, _inning in inningdata.items():
            top_atbat_list = _inning.get("top")
            inning(top_atbat_list, players, dst_folder, "top")
            bot_atbat_list = _inning.get("bottom")
            inning(bot_atbat_list, players, dst_folder, "bottom")

        break
