import cv2
from helperFunctions import readSizesFromJson, readColorRangeFromJson
import numpy as np
import math
from PIL import Image, ImageEnhance


# Counts the dots of the given image
# saveImagePath: Path to where to save the image
# jsonPath: path to file, which contains information about the sizes of dots
# saturation_increase: float, which tells how much saturation shall be applied to the image
                        # this increases the performance, as the colored dots are more easily selected
# show_increase_sat_image: Tells whether the satration-increased image shall be shown or not
# Returns amount of dots counted in image

def countDots(file, saveImagePath = None, sizePath = "sizes.json", colorPath = "colorRange.json", saturation_increase = 10.0, show_increase_sat_image = False):

    
    # Image read
    img = Image.open(file)
    
    # increase saturation
    converter = ImageEnhance.Color(img)
    img = converter.enhance(saturation_increase)

    if show_increase_sat_image:
        img.show()

    # convert image to cv2 image
    opencvImage = np.array(img)

    # possible idea from site: https://stackoverflow.com/questions/50210304/i-want-to-change-the-colors-in-image-with-python-from-specific-color-range-to-an
    
    hsv=cv2.cvtColor(opencvImage, cv2.COLOR_RGB2HSV)

    # Define lower and uppper limits of what we call "blue"
    lower_blue, upper_blue = readColorRangeFromJson(colorPath)

    # Mask image to only select browns
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # create new blank image
    newImg = np.zeros((opencvImage.shape[0], opencvImage.shape[1], 3), np.uint8)

    # only show dots with right color
    newImg[mask > 0] = (255, 255, 255)


    rgb = cv2.cvtColor(newImg, cv2.COLOR_HSV2RGB)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    
    # -----------------------

    _, threshedImg = cv2.threshold(gray, 160, 255, 1) # src, thresh, maxval, type

    # Perform morphological transformations using an erosion and dilation as basic operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    morphImg = cv2.morphologyEx(threshedImg, cv2.MORPH_OPEN, kernel)

    # Find and draw contours
    contours, hierarchy = cv2.findContours(morphImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contoursImg = cv2.cvtColor(morphImg, cv2.COLOR_GRAY2RGB)


    ## filter by area

    # read the sizes for the dots from the default file
    # if they cant be read, default values are assigned
    s1, s2, s3 = readSizesFromJson(sizePath)

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

                # calculate how many dots (of average size (s1 + s2) / 2) could be inside of that row
                amountDots = cv2.contourArea(cnt) / ((s1 + s2) / 2)

                # add the contour to the list of contours as often as a dot could fit into the form
                for _ in range(math.floor(amountDots)):
                    multipleContours.append(cnt)

            else:

                tooBigContours.append(cnt)

    cv2.drawContours(contoursImg, detectedContours, -1, (0,180,0), 3) # draw detected contours
    cv2.drawContours(contoursImg, multipleContours, -1, (0,180,240), 3) # draw multiple contours
    cv2.drawContours(contoursImg, tooBigContours, -1, (0,0,255), 3) # draw contours which are too big

    # save image
    if saveImagePath != None:
        cv2.imwrite(saveImagePath, contoursImg)

    print(file + ", " + str(len(detectedContours)))
    return len(detectedContours) + len(multipleContours)