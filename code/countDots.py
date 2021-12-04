# Author
# Name: Fabian Sieper
# Email: sieper.fabian@outlook.com

import PIL
import cv2
import numpy as np
import math
from PIL import Image, ImageEnhance, ImageShow
import os
from helperFunctions import addTextToImage

# takes
# json ettings
# string file name
# pil image
# returns pil image
def increaseContrast(settings, filename, img):

    # incrase contrast
    contrast_converter = ImageEnhance.Contrast(img.copy())
    contr_img = contrast_converter.enhance(settings["contrast"]["contrastIncrease"])

    if settings["contrast"]["showImage"]:

        convertedImage = cv2.cvtColor(cv2.cvtColor(np.array(contr_img), cv2.COLOR_RGB2BGR), cv2.COLOR_BGR2RGB)

        if settings["fileNameToImage"]["show"]:

            addTextToImage(convertedImage, 
                        os.path.basename(filename), 
                        settings["fileNameToImage"]["position"], 
                        settings["fileNameToImage"]["fontSize"], 
                        settings["fileNameToImage"]["color"],
                        settings["fileNameToImage"]["lineWidth"])


        pil_img = Image.fromarray(convertedImage)

        ImageShow.show(pil_img)

    return contr_img

# takes
# json ettings
# string file name
# pil image
# returns pil image
def incraseSaturation(settings, filename, img):

    saturation_converter = ImageEnhance.Color(img.copy())
    pushed_img = saturation_converter.enhance(settings["saturation"]["saturationIncrease"])

    if settings["saturation"]["showImage"]:

        convertedImage = cv2.cvtColor(cv2.cvtColor(np.array(pushed_img), cv2.COLOR_RGB2BGR), cv2.COLOR_BGR2RGB)

        if settings["fileNameToImage"]["show"]:

            addTextToImage(convertedImage, 
                        os.path.basename(filename), 
                        settings["fileNameToImage"]["position"], 
                        settings["fileNameToImage"]["fontSize"], 
                        settings["fileNameToImage"]["color"],
                        settings["fileNameToImage"]["lineWidth"])

        pil_img = Image.fromarray(convertedImage)

        ImageShow.show(pil_img)


    return pushed_img

# transforms a pil image to an opencv image
def pilToOpenCVImage(pilImg):

    return np.array(pilImg)


def getCountours(settings, pilImage):


    opencvImage = pilToOpenCVImage(pilImage)

    # possible idea from site: https://stackoverflow.com/questions/50210304/i-want-to-change-the-colors-in-image-with-python-from-specific-color-range-to-an

    hsv=cv2.cvtColor(opencvImage, cv2.COLOR_RGB2HSV)

    # Mask image to only select browns
    mask = cv2.inRange(hsv, np.array(settings["color"]["lowerColor"]), np.array(settings["color"]["upperColor"]))

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
    contours, _ = cv2.findContours(morphImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contoursImg = cv2.cvtColor(morphImg, cv2.COLOR_GRAY2BGR)


    ## filter by area
    detectedContours = []
    multipleContours = []
    tooBigContours = []

    for cnt in contours:

        # if the area is the right size to be a dot
        if settings["sizes"]["s1"] < cv2.contourArea(cnt) < settings["sizes"]["s2"]:
            detectedContours.append(cnt)

        # if the area is too big to be a dot
        elif settings["sizes"]["s2"] < cv2.contourArea(cnt):

            # if the area is smaller than s3, it may consist of multiple dots
            if cv2.contourArea(cnt) < settings["sizes"]["s3"]:

                # calculate how many dots (of average size (s1 + s2) / 2) could be inside of that row
                amountDots = cv2.contourArea(cnt) / ((settings["sizes"]["s1"] + settings["sizes"]["s2"]) / 2)

                # if amount dots < 1.5, it gets floored, thus only counted as 1 point
                # in this case apend the single dot to the list of single dots
                if round(amountDots) == 1:
                    detectedContours.append(cnt)
                else:
                    # add the contour to the list of contours as often as a dot could fit into the form
                    for _ in range(round(amountDots)):

                        multipleContours.append(cnt)

                        if settings["amountDotsCounted"]["show"]:
                            # write amount of dots counted at that position
                            addTextToImage(contoursImg, 
                                                str(round(amountDots)),
                                                cnt[0][0],
                                                settings["amountDotsCounted"]["fontSize"],
                                                settings["amountDotsCounted"]["color"],
                                                settings["amountDotsCounted"]["lineWidth"])

            else:

                tooBigContours.append(cnt)

    cv2.drawContours(contoursImg, detectedContours, -1, (0,180,0), 10) # draw detected contours
    cv2.drawContours(contoursImg, multipleContours, -1, (240,180,0), 10) # draw multiple contours
    cv2.drawContours(contoursImg, tooBigContours, -1, (255,0,0), 10) # draw contours which are too big

    return contoursImg, detectedContours, multipleContours, tooBigContours


def getFinalImage(detectedContours, multipleContours, settings, contoursImgPIL, originalImgPIL, filename):

    # for safety reasons, convert the image to a cv2 image (does not hurt if it already is an cv2 iamge)
    contoursImgOPENCV = pilToOpenCVImage(contoursImgPIL)
    originalImgOPENCV = pilToOpenCVImage(originalImgPIL)
    
    # if the images dont have the right dimensions, transpose one of the images
    if contoursImgOPENCV.shape != originalImgOPENCV.shape:
        contoursImgOPENCV = np.transpose(contoursImgOPENCV, axes=(1, 0, 2))


    # count how many dots were detected
    countedDots = len(detectedContours) + len(multipleContours)

    # if the original image and the final image shall be overlayed
    if settings["overlayOriginalImage"] > 0.0:

        cv2.addWeighted(originalImgOPENCV, settings["overlayOriginalImage"],
                        contoursImgOPENCV, 1.0 - settings["overlayOriginalImage"], 0.0, contoursImgOPENCV)


    # convert image to other color space in order to apply 
    if settings["countedDotsToImage"]["show"]:

        addTextToImage(contoursImgOPENCV, 
                    str(countedDots), 
                    settings["countedDotsToImage"]["position"], 
                    settings["countedDotsToImage"]["fontSize"], 
                    settings["countedDotsToImage"]["color"],
                    settings["countedDotsToImage"]["lineWidth"])

    if settings["fileNameToImage"]["show"]:

            addTextToImage(contoursImgOPENCV, 
                        os.path.basename(filename), 
                        settings["fileNameToImage"]["position"], 
                        settings["fileNameToImage"]["fontSize"], 
                        settings["fileNameToImage"]["color"],
                        settings["fileNameToImage"]["lineWidth"])
                    
    # shall the image, containing the contours, be shown?
    if settings["showFinalImage"]:

        pil_img = Image.fromarray(contoursImgOPENCV)

        ImageShow.show(pil_img)

    return contoursImgOPENCV, countedDots



def saveImage(filename, settings, countedDots, opencvImage):

    # compute image path name
    basename = os.path.basename(filename)
    ending = ".jpg" if ".jpg" in basename else ".jpeg"

    bareBaseName = basename.replace(ending, "")

    saveImagePath = os.path.join(settings["saveDir"], bareBaseName + "_dotsCounted-" + str(countedDots) + ".jpg")

    # cange color space to original
    detectedDotsImage = cv2.cvtColor(opencvImage, cv2.COLOR_BGR2RGB)

    # convert color space back to what cv2 is used to
    cv2.imwrite(saveImagePath, detectedDotsImage)

    print("[INFO] - The file was saved at: '" + saveImagePath + "'.")


# Counts the dots of the given image
# settings: Json of settings required 
# Returns amount of dots counted in image (and saves image if wanted)

def countDots(  file,
                settings):

    # Image read
    img = Image.open(file)

    # incrase contrast
    contr_img = increaseContrast(settings, file, img.copy())

    # increase saturation
    sat_img = incraseSaturation(settings, file, contr_img.copy())

    # detect dots
    contoursImg, detectedContours, multipleContours, tooBigContours = getCountours(settings, sat_img)

    # draw detected dots and text on image
    detectedDotsImage, countedDots = getFinalImage(detectedContours, multipleContours, settings, contoursImg.copy(), img.copy(), file)

    # save image
    if settings["saveImage"]:

        saveImage(file, settings, countedDots, detectedDotsImage)

    print("Counted dots in file '" + os.path.basename(file) + "': " + str(countedDots))

    return countedDots