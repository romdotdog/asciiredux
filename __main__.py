from cv2 import data
import database
from sys import argv
from PIL import Image
import numpy as np
from os.path import splitext, basename
import operator

scale = 0.43
cols = 80

invert = True
threshold = 127
above_threshold = 255 if invert else 0
below_threshold = 0 if invert else 255

# https://code.activestate.com/recipes/415233-getting-minmax-in-a-sequence-greaterless-than-some/


def max_lt(seq, val):
    """
    Return greatest item in seq for which item < val applies.
    None is returned if seq was empty or all items in seq were >= val.

    >>> max_lt([3, 6, 7, 11], 10)
    7
    >>> max_lt((5, 9, 12, 13), 12)
    9
    """

    idx = len(seq)-1
    while idx >= 0:
        if seq[idx] < val:
            return seq[idx]
        idx -= 1
    return None

smallestSpace = min(database.spaceMeasurements)
def fillSpace(pt):
    r = ""
    while pt > smallestSpace:
        fittable = max_lt(database.spaceMeasurements, pt)
        pt -= fittable
        r += database.spaces[fittable]
    return r

# based on https://www.geeksforgeeks.org/converting-image-ascii-image-python/
if __name__ == "__main__":
    image = Image.open(argv[1]).convert("L").point(lambda p: above_threshold if p > threshold else below_threshold)

    W, H = image.size[0], image.size[1]

    w = W/cols
    h = w/scale
    rows = int(H/h)

    if cols > W or rows > H:
        print("Image too small")
        exit(0)
    
    aimg = []

    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)

        if j == rows-1:
            y2 = H

        aimg.append("")

        for i in range(cols):
            x1 = int(i*w)
            x2 = int((i+1)*w)

            # correct last tile
            if i == cols-1:
                x2 = W

            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))
            if not img.getbbox():
                aimg[j] += fillSpace(database.maxGridSize)
                continue
            img.show()

            rankings = database.compare(np.array(img))
            bestComparison = min(rankings.items(), key=operator.itemgetter(1))[0]
            fileNameWithoutExtension = splitext(basename(bestComparison))[0]
            print(fileNameWithoutExtension)
            aimg[j] += chr(int(fileNameWithoutExtension))


    with open("out.txt", "w+", encoding="utf8") as outf:
        for row in aimg:
            outf.write(row + "\n")




