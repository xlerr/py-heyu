from PIL import Image, ImageDraw, ImageFont
from PIL import ImageOps


def transparent_back(img):
    img = img.convert('RGBA')
    L, H = img.size
    for h in range(H):
        for l in range(L):
            dot = (l, h)
            r, g, b, a = img.getpixel(dot)
            if r > 0 & r < 255:
                a = r
            else:
                a = 0
            img.putpixel(dot, (255, 0, 0, a))
    return img


img = Image.open('./static/source.png')

box = (115, 100, 690, 360)
img = img.crop(box)

# img = ImageOps.invert(img)

img = transparent_back(img)

width, height = img.size

nImg = Image.new("RGBA", (width * 4, height), (0, 0, 0, 0))

for i in range(0, 4):
    pos = (width * i, 0)
    nImg.paste(img, pos)

width, height = (2409, int(2409 / nImg.size[0] * height))

nImg = nImg.resize((width, height), Image.ANTIALIAS)

img = Image.new("RGBA", (2479, 3508), (0, 0, 0, 0))
for i in range(0, 11):
    pos = (30, 3508 - (height + 30) * (i + 1))
    img.paste(nImg, pos)

font = ImageFont.truetype('./static/simsun.ttc', 82, encoding="unic")

draw = ImageDraw.Draw(img)
draw.text((350, 40), "了卡就是的了疯狂骄傲爱上了的开发就", fill="red", font=font)

img.save('./temp.png')
