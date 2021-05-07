import sys

import pytest

sys.path.append("./src")
from load_inningdata import *

# def test_get_at_bat():

#     atbat_list = get_at_bat()

#     # for atbat in atbat_list:
#     #     print(type(atbat.data), atbat.data)

#     # print(type(root), root.tag, root.attrib)
#     # assert root.tag == "game"
#     # assert type(root.attrib) == dict

def test_get_inning():
    top_atbat_list, bot_atbat_list = get_inning(1)

    assert len(top_atbat_list) == 3
    assert len(bot_atbat_list) == 5

    for atbat in top_atbat_list:
        assert type(atbat) == AtBat
        assert atbat.away_team_runs == 0
        assert atbat.home_team_runs == 0

        print(atbat)

    for atbat in bot_atbat_list:
        assert type(atbat) == AtBat
        assert atbat.away_team_runs == 0
        assert atbat.home_team_runs == 0

        print(atbat)

def test_get_pitch_by_pitch_per_atbat():

    atbat_num = 1
    pitch_by_pitch = get_pitch_by_pitch_per_atbat(atbat_num)

    correct = {'id': 5.0, 'event_num': 5.0, 'des_es': 'Status Change - In Progress', 'des': 'Called Strike', 'mt': '', 'cc': '', 'spin_rate': 'placeholder', 'spin_dir': 'placeholder', 'play_guid': '001cb4e1-2a64-4365-b619-db8feb6b37fe', 'nasty': '', 'zone': 'placeholder', 'type_confidence': 'placeholder', 'pitch_type': 'FF', 'break_length': 4.8, 'break_angle': 21.6, 'break_y': 24.0, 'az': -17.33, 'ay': 27.32, 'ax': -8.4, 'vz0': -5.38, 'vy0': -133.68, 'vx0': 5.81, 'z0': 6.13, 'y0': 50.0, 'x0': -2.0, 'pz': 2.86, 'px': 0.41, 'pfx_z': 8.16, 'pfx_x': -4.62, 'end_speed': 84.5, 'start_speed': 91.9, 'sv_id': '', 'tfs_zulu': '2020-09-23T23:11:16.982Z', 'sz_bot': 1.46, 'sz_top': 3.29, 'y': 161.58, 'x': 132.54, 'tfs': 231116.0, 'code': 'C', 'type': 'C', 'raw_px': -0.41, 'raw_pz': 2.86}

    des_list = []
    for pitch in pitch_by_pitch:
        print(pitch.des)
        des_list.append(pitch.des)

    print(list(set(des_list)))

# def test_get_pitch_by_pitch_per_atbat2():

#     des_list = []

#     for atbat_num in range(100):
#         pitch_by_pitch = get_pitch_by_pitch_per_atbat(atbat_num)

#         for pitch in pitch_by_pitch:
#             print(pitch.des)
#             des_list.append(pitch.des)

#     print("----")
#     for a in list(set(des_list)):
#         print(a)
