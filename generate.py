from fontTools.ttLib import TTFont
from json import dump
from sys import argv

from os import mkdir
from os.path import exists
from itertools import chain

from PIL import Image, ImageFont, ImageDraw

def generate(fontName, pointSize=12):
    pilFont = ImageFont.truetype(fontName, pointSize)
    fontToolsFont = TTFont(fontName)
    cmap = fontToolsFont['cmap']

    t = cmap.getcmap(3, 1).cmap
    s = fontToolsFont.getGlyphSet()
    units_per_em = fontToolsFont['head'].unitsPerEm

    # https://stackoverflow.com/questions/4190667/how-to-get-width-of-a-truetype-font-character-in-1200ths-of-an-inch-with-python
    def getTextWidth(c: int):
        if c in t and t[c] in s:
            return s[t[c]].width*float(pointSize)/units_per_em

    # Range is exclusive, so + 1
    spaces = [0x20, *range(0x2000, 0x200A + 1)]
    spaceWidth = {getTextWidth(x): chr(x) for x in spaces}
    maxGridSize = round(getTextWidth(87))
    lineHeight = 22

    if not exists("img/"):
        mkdir("img")

    with open("img/meta.json", "w+") as outf:
        dump({"spaces": spaceWidth, "maxGridSize": maxGridSize}, outf)

    # https://stackoverflow.com/questions/30470079/emoji-value-range & https://stackoverflow.com/questions/30964449/iterate-two-ranges-in-for-loop
    nonEmoji = chain(range(0, 169), range(175, 8205), range(12954, 126980), range(127570, 127744), range(129751, 129995))
    
    for c in nonEmoji:
        size = getTextWidth(c)
        if size is None or size > maxGridSize:
            continue
        image = Image.new("RGBA", (maxGridSize, lineHeight))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), chr(c), font=pilFont, fill=(0, 0, 0))

        bbox = image.getbbox()
        if not bbox:
            continue
        image = image.crop((0, bbox[1], maxGridSize, bbox[3]))
        image.save("img/{}.png".format(c))
        image.close()

if __name__ == "__main__":
    generate(argv[1])
