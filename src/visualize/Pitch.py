
import numpy as np
import bokeh
import cv2
from PIL import Image, ImageDraw, ImageFont

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import pandas as pd

from models import *
from terms.ja import *

HSIZE = 500
WSIZE = 400
RATE = 100

BATTER_L_IMG_PATH = "E:\\10_download\\Baseball\\162740_L_gray_clip.png"
BATTER_R_IMG_PATH = "E:\\10_download\\Baseball\\162740_R_gray_clip.png"

def pil2cv(pilimg):
    new_image = np.array(pilimg, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = new_image[:, :, ::-1]
    elif new_image.shape[2] == 4:  # 透過
        new_image = new_image[:, :, [2, 1, 0, 3]]
    return new_image

def cv2pil(cvimg):
    new_image = cvimg.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = new_image[:, :, ::-1]
    elif new_image.shape[2] == 4:  # 透過
        new_image = new_image[:, :, [2, 1, 0, 3]]
    new_image = Image.fromarray(new_image)
    return new_image

def putTextJP(img, text, org, fontFace, fontScale, color):
    x, y = org
    b, g, r = color
    colorRGB = (r, g, b)
    pilimg = cv2pil(img)
    draw = ImageDraw.Draw(pilimg)
    fontPIL = ImageFont.truetype(font = 'C:\\Windows\\Fonts\\Meiryo UI\\meiryo.ttc', size = fontScale)
    w, h = draw.textsize(text, font = fontPIL)
    # draw.text(xy = (x,y-h), text = text, fill = colorRGB, font = fontPIL)
    draw.text(xy = (x,y), text = text, fill = colorRGB, font = fontPIL)
    cvimg = pil2cv(pilimg)
    return cvimg


def putTextJP_backcolor(text, fontScale, textcolor, backcolor):
    _textcolor = (textcolor[2], textcolor[1], textcolor[0])
    _backcolor = (backcolor[2], backcolor[1], backcolor[0])

    tmp = Image.new('RGB', (1, 1), (0, 0, 0)) # dummy for get text_size
    tmp_d = ImageDraw.Draw(tmp)
    fontPIL = ImageFont.truetype(font = 'C:\\Windows\\Fonts\\Meiryo UI\\meiryo.ttc', size = fontScale)
    # text_size = tmp_d.textsize(text, fontPIL)
    text_size = tmp_d.multiline_textsize(text, font=fontPIL, stroke_width=0)
    
    pilimg = Image.new('RGB', text_size, _backcolor) # background: transparent
    img_d = ImageDraw.Draw(pilimg)
    bbox = img_d.multiline_textbbox((0, 0), text, font=fontPIL, stroke_width=0)
    tl = (0,0)
    img_d.multiline_text((tl[0] - bbox[0], tl[1] - bbox[1]), text, fill=_textcolor, font=fontPIL, stroke_width=0)

    text_size = bbox[2:]
    margin_x = int(text_size[0]*0.15)
    margin_y = int(text_size[1]*0.15)
    text_size = (int(text_size[0]+margin_x*2), int(text_size[1]+margin_y*2))
    result = Image.new(pilimg.mode, text_size, _backcolor)
    result.paste(pilimg, (margin_x, margin_y))

    cvimg = pil2cv(result)
    return cvimg

def circle_text(text, size, circlecolor, textcolor=(255,255,255), backcolor=(0,0,0)):
    # unit image
    s = 101
    img = np.zeros((s,s,3), dtype=np.uint8)
    img[::] = backcolor
    cv2.circle(img, (int(s/2),int(s/2)), int(s/2), circlecolor, -1)
    cv2.putText(img, text, (20, 82), cv2.FONT_HERSHEY_PLAIN, 6, textcolor, 6, cv2.LINE_AA)
    
    img = cv2.resize(img, size)
    return img

def strike_zone(img):

    # s = (-.95, 3.5)
    # e = (.95, 1.6)

    # main line
    s = (-.85, 3.5)
    e = (.85, 1.6)
    s = (int(WSIZE+s[0]*RATE), HSIZE-int(s[1]*RATE))
    e = (int(WSIZE+e[0]*RATE), HSIZE-int(e[1]*RATE))
    cv2.rectangle(img, s, e, (255,255,255), 2)

    # sub lines
    w = e[0] - s[0]
    h = e[1] - s[1]
    bin = int(w/3+0.5)
    for x in range(bin, w, bin):
        cv2.rectangle(img, (x+s[0], s[1]), (x+s[0], e[1]), (255,255,255), 1)
    bin = int(h/3+0.5)
    for y in range(bin, h, bin):
        cv2.rectangle(img, (s[0], y+s[1]), (e[0], y+s[1]), (255,255,255), 1)

def draw_batter(img, stand):

    if stand == "L":
        batter = cv2.imread(BATTER_L_IMG_PATH)
        batter = cv2.resize(batter, None, fx=.38, fy=.38)
        h, w = batter.shape[:2]
        img[10:10+h, 100:100+w] = batter
    else:
        batter = cv2.imread(BATTER_R_IMG_PATH)
        batter = cv2.resize(batter, None, fx=.38, fy=.38)
        h, w = batter.shape[:2]
        img[10:10+h, 540:540+w] = batter

def pitch_color(pitch:Pitch):
    color = (255,255,255)
    if "Strike" in pitch.des or "Foul" in pitch.des:
        # color = (0,255,255)
        color = (42, 221, 252)
    elif "Ball" in pitch.des:
        color = (0,255,0)
    elif "In play, no out" == pitch.des:
        color = (255,0,0)
    elif "In play, out(s)" == pitch.des:
        color = (0,0,255)
    elif "In play, run(s)" == pitch.des:
        color = (255,0,0)

    return color

def one_pitching(img, pitch:Pitch):
    x = int(WSIZE+pitch.px*RATE)
    y = max(0, min(HSIZE, HSIZE-int(pitch.pz*RATE)))

    color = pitch_color(pitch)
    cv2.circle(img, (x, y), 5, color, -1)

    # cv2.putText(img, f"{pitch.start_speed} mph", (20, 230), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA)
    # speed = int(pitch.start_speed*1.60934)
    # cv2.putText(img, f"{pitch.pitch_type} {speed}km/h", (20, 200), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA)

def course(img, atbat:AtBat, pitch:Pitch):

    strike_zone(img)
    draw_batter(img, atbat.stand)

    if pitch.des != "Automatic Ball":
        one_pitching(img, pitch)

    # cv2.putText(img, pitch.des, (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA)

def pitch_history(img, idx:int, pitch:Pitch):

    sx = 20
    font_size = 16

    size = (21,21)
    backcolor = (0,0,0)
    circlecolor = (0,255,0)
    textcolor = (255,255,255)

    bin = 25

    if pitch.des != "Automatic Ball":
        speed = int(pitch.start_speed*1.60934)
        # cv2.putText(img, f"{idx+1}", (sx, 30+idx*30), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA)
        # cv2.putText(img, f"{pitch.pitch_type}", (sx+50, 30+idx*30), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA)
        # cv2.putText(img, f"{speed}km/h", (sx+120, 30+idx*30), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA)
        # cv2.putText(img, f"{PITCH_DES[pitch.des]}", (sx+300, 30+idx*30), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA)
        circlecolor = pitch_color(pitch)
        count_img = circle_text(f"{idx+1}", size, circlecolor, textcolor, backcolor)
        h, w = count_img.shape[:2]
        if bin+idx*bin+h >= img.shape[0]:
            pass
        else:
            img[bin+idx*bin:bin+idx*bin+h, sx:sx+w] = count_img
            # img = putTextJP(img, f"{idx+1}", (sx, 30+idx*30), cv2.FONT_HERSHEY_PLAIN, font_size, (255,255,255))
            img = putTextJP(img, f"{pitch.pitch_type}", (sx+50, bin+idx*bin), cv2.FONT_HERSHEY_PLAIN, font_size, (255,255,255))
            img = putTextJP(img, f"{speed}km/h", (sx+100, bin+idx*bin), cv2.FONT_HERSHEY_PLAIN, font_size, (255,255,255))
            img = putTextJP(img, f"{PITCH_DES[pitch.des]}", (sx+200, bin+idx*bin), cv2.FONT_HERSHEY_PLAIN, font_size, (255,255,255))

    return img

def batter_info(img, batter, stand, home:bool):
    h, w = img.shape[:2]
    half_w = int(w/2)
    halfhalf_w = int(w/4)
    # sx = 20
    sx = int(w*2/5)
    font_size = 16

    if home:
        pos_x = sx
    else:
        pos_x = sx+halfhalf_w
    
    bin = 25
    img = putTextJP(img, f"{batter.team_abbrev}", (pos_x, bin), cv2.FONT_HERSHEY_PLAIN, font_size, (255,255,255))
    img = putTextJP(img, f"Batter | {batter.num}", (pos_x, bin*2), cv2.FONT_HERSHEY_PLAIN, font_size, (255,255,255))
    name = f"{batter.first} {batter.last}"
    img = putTextJP(img, name, (pos_x, bin*3), cv2.FONT_HERSHEY_PLAIN, font_size, (255,255,255))

    if stand == "R":
        stand_img = putTextJP_backcolor(BATTER_INFO[stand], 12, (255,255,255), (20,20,255))
    else:
        stand_img = putTextJP_backcolor(BATTER_INFO[stand], 12, (255,255,255), (255,20,20))

    h, w = stand_img.shape[:2]
    img[70:70+h, pos_x+120:pos_x+120+w] = stand_img

    return img

def pitcher_info(img, pitcher, throw, home:bool):
    h, w = img.shape[:2]
    half_w = int(w/2)
    halfhalf_w = int(w/4)
    sx = int(w*2/5)
    font_size = 16

    if home:
        pos_x = sx
    else:
        pos_x = sx+halfhalf_w

    bin = 25
    img = putTextJP(img, f"{pitcher.team_abbrev}", (pos_x, bin), cv2.FONT_HERSHEY_PLAIN, font_size, (255,255,255))
    img = putTextJP(img, f"Pitcher | {pitcher.num}", (pos_x, bin*2), cv2.FONT_HERSHEY_PLAIN, font_size, (255,255,255))
    name = f"{pitcher.first} {pitcher.last}"
    img = putTextJP(img, f"{name} {throw}", (pos_x, bin*3), cv2.FONT_HERSHEY_PLAIN, font_size, (255,255,255))

    return img
