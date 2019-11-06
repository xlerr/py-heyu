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

    autograph_color: tuple

    def __init__(self, files: list, src_dir: str, save_path: str):
        self.files = files
        self.src_dir = src_dir.rstrip('/') + '/'
        self.save_path = save_path.rstrip('/') + '/'

        if not os.path.exists(self.src_dir):
            os.mkdir(self.src_dir, 0o755)

        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path, 0o755)

        cfg = ConfigParser()
        cfg.read('config.ini')

        self.text = cfg.get('title', 'text')
        self.text_color = cfg.get('title', 'color')

        self.autograph_color = self.hex2rgb(cfg.get('autograph', 'color'))

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

    @staticmethod
    def hex2rgb(hex_color: str):
        hex_color = hex_color.lstrip('#')
        opt = re.findall(r'(.{2})', hex_color)
        color = []
        for i in range(0, len(opt)):
            color.append(int(opt[i], 16))
        return tuple(color)

    def transparent_back(self, imgIns):
        R, G, B = self.autograph_color
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
