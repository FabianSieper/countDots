from os import read
import cv2
from helperFunctions import readSizesFromJson
import numpy as np
# Counts the dots of the given image
# saveImagePath: Path to where to save the image
# jsonPath: path to file, which contains information about the sizes of dots
# Returns amount of dots counted in image
def countDots(file, saveImagePath = None, jsonPath = "sizes.json"):

    
    # Image read
    img = cv2.imread(file, 0)


    # Denoising
    # denoisedImg = cv2.fastNlMeansDenoising(img)

    # Threshold (binary image)
    # thresh – threshold value.
    # maxval – maximum value to use with the THRESH_BINARY and THRESH_BINARY_INV thresholding types.
    # type – thresholding type

    _, threshedImg = cv2.threshold(img, 140, 255, 1) # src, thresh, maxval, type

    # Perform morphological transformations using an erosion and dilation as basic operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
    morphImg = cv2.morphologyEx(threshedImg, cv2.MORPH_OPEN, kernel)

    # Find and draw contours
    contours, hierarchy = cv2.findContours(morphImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contoursImg = cv2.cvtColor(morphImg, cv2.COLOR_GRAY2RGB)


    ## filter by area

    # read the sizes for the dots from the default file
    # if they cant be read, default values are assigned
    s1, s2, s3 = readSizesFromJson(jsonPath)

    detectedContours = []
    multipleContours = []
    tooBigContours = []

    for cnt in contours:

        # if the area is the right size to be a dot
        if s1 < cv2.contourArea(cnt) < s2:
            detectedContours.append(cnt)

        # if the area is too big to be a dot
        elif s2 < cv2.contourArea(cnt):

            # if the area is smaller than s3, it may consist of multiple dots
            if cv2.contourArea(cnt) < s3:

                # calculate how many dots (of max size (s2)) could be inside of that row
                amountDots = cv2.contourArea(cnt) / s2

                # add the contour to the list of contours as often as a dot could fit into the form
                for _ in range(int(amountDots)):
                    multipleContours.append(cnt)

            else:

                tooBigContours.append(cnt)

    cv2.drawContours(contoursImg, detectedContours, -1, (0,180,0), 2) # draw detected contours
    cv2.drawContours(contoursImg, multipleContours, -1, (0,180,240), 2) # draw multiple contours
    cv2.drawContours(contoursImg, tooBigContours, -1, (0,0,255), 2) # draw contours which are too big

    # save image
    if saveImagePath != None:
        cv2.imwrite(saveImagePath, contoursImg)

    print(file + ", " + str(len(detectedContours)))
    return len(detectedContours) + len(multipleContours)