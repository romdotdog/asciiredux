import cv2
from glob import glob
from json import load

glyphs = {img: cv2.imread(img, cv2.IMREAD_GRAYSCALE)
          for img in glob("img/*.png")}

with open("img/meta.json", "r") as outf:
    meta = load(outf)

spaces = {v: k for k, v in meta["spaces"].items()}
spaceMeasurements: list = list(spaces.keys())
maxGridSize: int = meta["maxGridSize"]

def compare(contour):
    return {path: cv2.matchShapes(contour, glyph, 1, 0.0) for path, glyph in glyphs.items()}
