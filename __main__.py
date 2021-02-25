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
above_threshold = invert and 255 or 0
below_threshold = invert and 0 or 255

# based on https://www.geeksforgeeks.org/converting-image-ascii-image-python/
if __name__ == "__main__":
    image = Image.open(argv[1]).convert("L")
    image = image.point(lambda p: p > threshold and above_threshold or below_threshold)

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

            rankings = database.compare(np.array(img))
            bestComparison = max(rankings.items(), key=operator.itemgetter(1))[0]
            fileNameWithoutExtension = splitext(basename(bestComparison))[0]
            aimg[j] += chr(int(fileNameWithoutExtension))


    with open("out.txt", "w+", encoding="utf8") as outf:
        for row in aimg:
            outf.write(row + "\n")




