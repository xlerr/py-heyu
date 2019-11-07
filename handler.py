from PIL import Image, ImageDraw, ImageFont
from configparser import ConfigParser
import re
import os


class Handler:
    src_dir: str
    save_path: str
    files: list

    text: str
    text_color: str

    signatureColor: list

    def __init__(self, config):
        self.src_dir = config['sourcePath'].rstrip('/') + '/'
        self.save_path = config['savePath'].rstrip('/') + '/'
        self.files = self.findImageFile()

        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path, 0o755)

        self.text = config['title']
        self.text_color = config['titleColor']

        self.signatureColor = config['signatureColor']

    def run(self):
        for file in self.files:
            self.process(file)

    def process(self, file_name):
        width = 690
        height = 360
        img = Image.open(self.src_dir + file_name).resize((824, 488), Image.ANTIALIAS).crop((115, 100, width, height))
        img = self.transparent_back(img)

        nImg = Image.new("RGBA", (width * 4, height))

        for i in range(0, 4):
            pos = (width * i, 0)
            nImg.paste(img, pos)

        width, height = (2409, int(2409 / nImg.size[0] * height))

        nImg = nImg.resize((width, height), Image.ANTIALIAS)

        img = Image.new("RGBA", (2479, 3508), (255, 255, 255, 255))
        for i in range(0, 11):
            pos = (30, 200 + (height + 24) * i)
            img.paste(nImg, pos, nImg)

        font = ImageFont.truetype('./static/simsun.ttc', 82)

        text_width, text_height = font.getsize(self.text)

        draw = ImageDraw.Draw(img)
        draw.text((int((width - text_width) / 2), 40), self.text, fill=self.text_color, font=font)

        img.save(self.save_path + file_name + '.png')

    def findImageFile(self):
        filenames = []
        for root, dirs, files in os.walk(self.src_dir):
            for file in files:
                if re.search('.(jpe?g|png)$', file, re.M | re.I):
                    filenames.append(file)
        return filenames

    @staticmethod
    def hex2rgb(hex_color: str):
        hex_color = hex_color.lstrip('#')
        opt = re.findall(r'(.{2})', hex_color)
        color = []
        for i in range(0, len(opt)):
            color.append(int(opt[i], 16))
        return tuple(color)

    def transparent_back(self, imgIns):
        signatureColor = self.signatureColor
        imgIns = imgIns.convert('RGBA')
        L, H = imgIns.size
        for h in range(H):
            for l in range(L):
                dot = (l, h)
                r, g, b, a = imgIns.getpixel(dot)
                if 0 < r < 255:
                    a = r
                else:
                    a = 0
                signatureColor[3] = a
                imgIns.putpixel(dot, tuple(signatureColor))
        return imgIns
