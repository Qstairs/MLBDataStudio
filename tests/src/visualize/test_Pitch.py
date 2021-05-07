import sys

import pytest
import cv2

sys.path.append("./src")
from visualize.Pitch import *

def putTextJP(img, text, org, fontFace, fontScale, color):
    x, y = org
    b, g, r = color
    colorRGB = (r, g, b)
    print(colorRGB)
    pilimg = cv2pil(img)
    draw = ImageDraw.Draw(pilimg)
    font_path = 'C:\\Windows\\Fonts\\Meiryo UI\\meiryo.ttc'
    fontPIL = ImageFont.truetype(font = font_path, size = fontScale)
    w, h = draw.textsize(text, font = fontPIL)
    draw.text(xy = (x,y-h), text = text, fill = colorRGB, font = fontPIL)
    # pilimg.save('text.jpg')
    cvimg = pil2cv(pilimg)
    return cvimg


# def test_putTextJP():
#     BATTER_L_IMG_PATH = "E:\\10_download\\Baseball\\162740_L_gray_clip.png"
#     img = cv2.imread(BATTER_L_IMG_PATH)
#     img = putTextJP(img, "テスト", (20, 30), None, 16, (255,255,255))

#     cv2.imshow("", img)
#     cv2.waitKey(0)

# def test_putTextJP_backcolor():
#     img = putTextJP_backcolor("右打", 16, (255,255,255), (50,50,255))

#     cv2.imshow("", img)
#     cv2.waitKey(0)

def test_circle_text():
    text = "2"
    size = (100,100)
    backcolor = (0,0,0)
    circlecolor = (0,255,0)
    textcolor = (255,255,255)
    img = circle_text(text, size, circlecolor, textcolor, backcolor)
    cv2.imshow("", img)
    cv2.waitKey(0)
