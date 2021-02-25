from sklearn.preprocessing import normalize
import database
from sys import argv
from PIL import Image
import numpy as np
from os.path import splitext, basename
import operator
import re

scale = 0.43
cols = 80

invert = True
threshold = 10
above_threshold = 255 if invert else 0
below_threshold = 0 if invert else 255

# based on https://www.geeksforgeeks.org/converting-image-ascii-image-python/
if __name__ == "__main__":
    image = Image.open(argv[1]).convert("LA")# .point(lambda p: above_threshold if p > threshold else below_threshold)
    
    bbox = image.getbbox()
    image = np.array(image.crop(bbox))

    L, A = image[:, :, 0], image[:, :, 1]

    adjustedThreshold = threshold / 255
    thresholdAlgorithm = np.uint8(np.where(normalize(L*A) > adjustedThreshold, above_threshold, below_threshold))
    
    print(np.shape(thresholdAlgorithm))
    image = Image.fromarray(thresholdAlgorithm, "L")

    print(image.mode)

    image.show()

    W, H = image.size[0], image.size[1]

    w = W/cols
    h = w/scale
    rows = int(H/h)

    print((cols, rows))

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
                aimg[j] += " "
                continue

            newHeight = 16
            newWidth = int(w * newHeight / h)
            newImg = np.array(img.resize((newWidth, newHeight), Image.NEAREST))

            rankings = database.compare(newImg)
            bestComparison = min(rankings.items(), key=operator.itemgetter(1))[0]
            fileNameWithoutExtension = splitext(basename(bestComparison))[0]

            c = int(fileNameWithoutExtension)
            aimg[j] += chr(c)


    with open("out.txt", "w+", encoding="utf8") as outf:
        for row in aimg:
            outf.write(re.sub(r"\s+$", "", row, re.MULTILINE) + "\n")




