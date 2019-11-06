from PIL import Image, ImageDraw, ImageFont
from PIL import ImageOps
from configparser import ConfigParser
import re
import string
import os


def hex2rgb(hex_color: string):
    hex_color = hex_color.strip('#')
    opt = re.findall(r'(.{2})', hex_color)
    color = []
    for i in range(0, len(opt)):
        color.append(int(opt[i], 16))
    return tuple(color)


def transparent_back(imgIns, auto_graph_color):
    R, G, B = auto_graph_color
    imgIns = imgIns.convert('RGBA')
    L, H = imgIns.size
    for h in range(H):
        for l in range(L):
            dot = (l, h)
            r, g, b, a = imgIns.getpixel(dot)
            if r > 0 & r < 255:
                a = r
            else:
                a = 0
            imgIns.putpixel(dot, (R, G, B, a))
    return imgIns


cfg = ConfigParser()
cfg.read('config.ini')

text = cfg.get('title', 'text')
text_color = cfg.get('title', 'color')

autograph_color = hex2rgb(cfg.get('autograph', 'color'))

img = Image.open('./static/source.png')
img = img.resize((824, 488), Image.ANTIALIAS)

box = (115, 100, 690, 360)
img = img.crop(box)

# img = ImageOps.invert(img)

img = transparent_back(img, autograph_color)

width, height = img.size

nImg = Image.new("RGBA", (width * 4, height))

for i in range(0, 4):
    pos = (width * i, 0)
    nImg.paste(img, pos)

width, height = (2409, int(2409 / nImg.size[0] * height))

nImg = nImg.resize((width, height), Image.ANTIALIAS)

img = Image.new("RGBA", (2479, 3508), (255, 255, 255, 255))
for i in range(0, 11):
    pos = (30, 3508 - (height + 30 * int(bool(i))) * (i + 1))
    img.paste(nImg, pos, nImg)

font = ImageFont.truetype('./static/simsun.ttc', 82)

text_width, text_height = font.getsize(text)

draw = ImageDraw.Draw(img)
draw.text((int((width - text_width) / 2), 40), text, fill=text_color, font=font)

img.save('./temp.png')
