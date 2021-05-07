import os
import xml.etree.ElementTree as ET
try:
    from urllib.request import urlopen
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import urlopen, HTTPError

from models import *

def download_inningdata():
    path = "testdata\gid_2020_09_23_tbamlb_nynmlb_1.xml"
    tree = ET.parse(path)
    return tree

def get_inning(xmldata, num:int):
    for inning in xmldata:
        _num = inning.attrib.get("num")
        if num == int(_num):
            for top_bot in inning:
                if top_bot.tag == "top":
                    top_atbat_list = get_at_bat(top_bot)
                if top_bot.tag == "bottom":
                    bot_atbat_list = get_at_bat(top_bot)

    return top_atbat_list, bot_atbat_list

def get_at_bat(top_bot):

    atbat_list = []
    for detail in top_bot:
        if detail.tag == "atbat":
            atbat = AtBat(detail.attrib)
            pitch_by_pitch = get_pitch_by_pitch_per_atbat(detail)
            setattr(atbat, "pitch_by_pitch", pitch_by_pitch)
            atbat_list.append(atbat)

    return atbat_list

# def get_pitch_by_pitch():

#     data = download_inningdata()
#     root = data.getroot()

#     pitch_by_pitch = []
#     for pitch_xml in root.iter('pitch'):
#         pitch_data = pitch_xml.attrib
#         pitch = Pitch(pitch_data)
#         pitch_by_pitch.append(pitch)

#     return pitch_by_pitch

def get_pitch_by_pitch_per_atbat(atbat):

    # data = download_inningdata()
    # root = data.getroot()

    pitch_by_pitch = []
    for pitch_xml in atbat.iter('pitch'):
        pitch_data = pitch_xml.attrib
        pitch = Pitch(pitch_data)
        pitch_by_pitch.append(pitch)

    return pitch_by_pitch