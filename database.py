import cv2
from glob import glob
from json import load

glyphs = {img: cv2.imread(img, cv2.IMREAD_GRAYSCALE)
          for img in glob("img/*.png")}

def compare(contour):
    return {path: cv2.matchShapes(contour, glyph, 3, 0.0) for path, glyph in glyphs.items()}
