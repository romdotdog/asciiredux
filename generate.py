import unicodedata
import util
from unicodedata import combining
from json import dump
from sys import argv

from os import mkdir
from os.path import exists

from PIL import Image, ImageFont, ImageDraw

def isRTL(c):
    prop = unicodedata.bidirectional(c)
    return "AL" in prop or "R" in prop

def generate(fontName, pointSize=12):
    pilFontFallback = ImageFont.truetype(util.fontFallback, pointSize)
    pilFont = ImageFont.truetype(fontName, pointSize)

    Util = util.Util(fontName, pointSize)

    # Range is exclusive, so + 1
    spaces = [0x20, *range(0x2000, 0x200A + 1)]
    spaceWidth = {chr(x): Util.getTextWidth(x) for x in spaces}
    maxGridSize = round(Util.getTextWidth(9608))
    lineHeight = 22

    if not exists("img/"):
        mkdir("img")

    with open("img/meta.json", "w+") as outf:
        dump({"spaces": spaceWidth, "maxGridSize": maxGridSize,
              "fontName": fontName, "pointSize": pointSize}, outf)

    for c in range(0, 129995):
        size = Util.getTextWidth(c)
        ch = chr(c)
        if size is None or size > maxGridSize or combining(ch) or isRTL(ch):
            continue

        image = Image.new("L", (maxGridSize, lineHeight), (0))
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), ch, font=(
            pilFont if c in Util.t and Util.t[c] in Util.s else pilFontFallback), fill=(255))

        bbox = image.getbbox()
        if not bbox: # Image is empty
            continue

        image = image.crop((0, 0, maxGridSize, bbox[1] + bbox[3])) # Create even spacing between top and bottom of glyph
        image.save("img/{}.png".format(c))
        image.close()

if __name__ == "__main__":
    generate(argv[1])
