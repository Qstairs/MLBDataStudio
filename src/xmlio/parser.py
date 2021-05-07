import xml.etree.ElementTree as ET


def parse_path(path:str):
    #xmlデータを読み込みます
    tree = ET.parse(path)
    #一番上の階層の要素を取り出します
    root = tree.getroot()

    return root

def parse(strdata:str):
    root = ET.fromstring(strdata)

    return root
