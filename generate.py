from fontTools.ttLib import TTFont
from json import dump
from sys import argv

from os import mkdir
from os.path import exists

from PIL import Image, ImageFont, ImageDraw

fontFallback = "C:/Windows/Fonts/Arial.ttf"
def generate(fontName, pointSize=12):
    pilFontFallback = ImageFont.truetype(fontFallback, pointSize)
    pilFont = ImageFont.truetype(fontName, pointSize)

    fontToolsFontFallback = TTFont(fontFallback)
    cmapFallback = fontToolsFontFallback['cmap']

    fontToolsFont = TTFont(fontName)
    cmap = fontToolsFont['cmap']

    t = cmap.getcmap(3, 1).cmap
    s = fontToolsFont.getGlyphSet()

    tFallback = cmapFallback.getcmap(3, 1).cmap
    sFallback = fontToolsFontFallback.getGlyphSet()

    units_per_emFallback = fontToolsFontFallback['head'].unitsPerEm
    units_per_em = fontToolsFont['head'].unitsPerEm

    # https://stackoverflow.com/questions/4190667/how-to-get-width-of-a-truetype-font-character-in-1200ths-of-an-inch-with-python
    def getTextWidth(c: int):
        if c in t and t[c] in s:
            return s[t[c]].width*float(pointSize)/units_per_em
        if c in tFallback and tFallback[c] in sFallback:
            return sFallback[tFallback[c]].width*float(pointSize)/units_per_emFallback

    # Range is exclusive, so + 1
    spaces = [0x20, *range(0x2000, 0x200A + 1)]
    spaceWidth = {chr(x): getTextWidth(x) for x in spaces}
    maxGridSize = round(getTextWidth(9608))
    lineHeight = 22

    if not exists("img/"):
        mkdir("img")

    with open("img/meta.json", "w+") as outf:
        dump({"spaces": spaceWidth, "maxGridSize": maxGridSize}, outf)

    for c in range(0, 129995):
        size = getTextWidth(c)
        if size is None or size > maxGridSize:
            continue

        image = Image.new("L", (maxGridSize, lineHeight), (0))
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), chr(c), font=(pilFont if c in t and t[c] in s else pilFontFallback), fill=(255))

        bbox = image.getbbox()
        if not bbox: # Image is empty
            continue

        image = image.crop((0, 0, maxGridSize, bbox[1] + bbox[3])) # Create even spacing between top and bottom of glyph
        image.save("img/{}.png".format(c))
        image.close()

if __name__ == "__main__":
    generate(argv[1])
