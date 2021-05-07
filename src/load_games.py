import os

from models.Game import Game

def get_games(data):

    games = []
    for gamexml in data.iter('go_game'):
        game_data = {}
        for g in gamexml:
            print(g)
            if g.tag == "game":
                game_data["game_id"] = g.attrib.get("id")
                game_data["basic"] = g.attrib
            elif g.tag == "team":
                game_data.setdefault("team", {})
                for gameteam in g.iter('gameteam'):
                    print(gameteam.attrib)
                    game_data["team"][g.attrib.get("name")] = gameteam.attrib
            elif g.tag == "w_pitcher":
                game_data["w_pitcher"] = g.attrib
                for pitcher in g.iter('pitcher'):
                    game_data["w_pitcher"]["name"] = pitcher.attrib
            elif g.tag == "l_pitcher":
                game_data["l_pitcher"] = g.attrib
                for pitcher in g.iter('pitcher'):
                    game_data["l_pitcher"]["name"] = pitcher.attrib
            elif g.tag == "sv_pitcher":
                game_data["sv_pitcher"] = g.attrib
                for pitcher in g.iter('pitcher'):
                    game_data["sv_pitcher"]["name"] = pitcher.attrib

        game = Game(game_data)
        games.append(game)

    return games