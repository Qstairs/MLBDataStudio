import sys

sys.path.append(".")
from src.xml.parser import *

def test_parse():
    path = "testdata\gid_2020_09_23_tbamlb_nynmlb_1.xml"
    root = parse_path(path)

    print(type(root), root.tag, root.attrib)
    assert root.tag == "game"
    assert type(root.attrib) == dict

    # for inning in root.iter('inning'):
    #     pitchs = inning.findall('pitch')
    #     for pitch in pitchs:
    #         print(pitch.tag)
    #         print(pitch.attrib)

    # for pitch in root.iter('pitch'):
    #     print(pitch.tag)
    #     print(pitch.attrib)
