from fontTools.ttLib import TTFont

fontFallback = "C:/Windows/Fonts/Arial.ttf"
class Util:
    def __init__(self, fontName, pointSize):
        self.fontName = fontName
        self.pointSize = pointSize

        fontToolsFontFallback = TTFont(fontFallback)
        cmapFallback = fontToolsFontFallback['cmap']

        fontToolsFont = TTFont(fontName)
        cmap = fontToolsFont['cmap']

        self.t = cmap.getcmap(3, 1).cmap
        self.s = fontToolsFont.getGlyphSet()

        self.tFallback = cmapFallback.getcmap(3, 1).cmap
        self.sFallback = fontToolsFontFallback.getGlyphSet()

        self.units_per_emFallback = fontToolsFontFallback['head'].unitsPerEm
        self.units_per_em = fontToolsFont['head'].unitsPerEm

    # https://stackoverflow.com/questions/4190667/how-to-get-width-of-a-truetype-font-character-in-1200ths-of-an-inch-with-python
    def getTextWidth(self, c: int):
        if c in self.t and self.t[c] in self.s:
            return self.s[self.t[c]].width*float(self.pointSize)/self.units_per_em
        if c in self.tFallback and self.tFallback[c] in self.sFallback:
            return self.sFallback[self.tFallback[c]].width*float(self.pointSize)/self.units_per_emFallback
