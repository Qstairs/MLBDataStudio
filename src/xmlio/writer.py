import os

import xml.etree.ElementTree as ET

def writer(path, xmldata):

    os.makedirs(os.path.dirname(path), exist_ok=True)
    # tree = ET.ElementTree(roots) 
    tree = ET.ElementTree(xmldata)
    tree.write(path, encoding='utf-8')
