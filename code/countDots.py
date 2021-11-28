# Author
# Name: Fabian Sieper
# Email: sieper.fabian@outlook.com

import PIL
import cv2
import numpy as np
import math
from PIL import Image, ImageEnhance, ImageShow
import os

# Counts the dots of the given image
# settings: Dict of settings required 
# Returns amount of dots counted in image (and saves image if wanted)

def countDots(  file,
                settings = {"s1" : 0, "s2" : 80, "s3" : 100, 
                            "lower_color" : np.array([45,28,0]), "upper_color" : np.array([110,255,255]),
                            "saturation_increase" : 10.0, "show_increase_sat_image" : False,
                            "showFinalImage" : False,
                            "saveImage" : True,
                            "saveDir" : "../processedFiles/" ,
                            "overlay" : 0.0,
                            "source" : "file"}):

    # Image read
    img = Image.open(file)

    # increase saturation
    converter = ImageEnhance.Color(img.copy())
    pushed_img = converter.enhance(settings["saturation_increase"])

    if settings["show_increase_sat_image"]:

        convertedImage = cv2.cvtColor(cv2.cvtColor(np.array(pushed_img), cv2.COLOR_RGB2BGR), cv2.COLOR_BGR2RGB)

        if settings["showTextOnImage_text"]:
            # write the name of file onto the image
            cv2.putText(convertedImage, 
                        os.path.basename(file), 
                        settings["position_text"], 
                        cv2.FONT_HERSHEY_SIMPLEX,
                        settings["fontsize_text"],  
                        settings["color_text"],
                        settings["lineWidth_text"]) 

        pil_img = Image.fromarray(convertedImage)

        ImageShow.show(pil_img)


    # convert image to cv2 image
    opencvImage = np.array(pushed_img)

    # possible idea from site: https://stackoverflow.com/questions/50210304/i-want-to-change-the-colors-in-image-with-python-from-specific-color-range-to-an

    hsv=cv2.cvtColor(opencvImage, cv2.COLOR_RGB2HSV)

    # Mask image to only select browns
    mask = cv2.inRange(hsv, settings["lower_color"], settings["upper_color"])

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
    contoursImg = cv2.cvtColor(morphImg, cv2.COLOR_GRAY2RGB)


    ## filter by area
    detectedContours = []
    multipleContours = []
    tooBigContours = []

    for cnt in contours:

        # if the area is the right size to be a dot
        if settings["s1"] < cv2.contourArea(cnt) < settings["s2"]:
            detectedContours.append(cnt)

        # if the area is too big to be a dot
        elif settings["s2"] < cv2.contourArea(cnt):

            # if the area is smaller than s3, it may consist of multiple dots
            if cv2.contourArea(cnt) < settings["s3"]:

                # calculate how many dots (of average size (s1 + s2) / 2) could be inside of that row
                amountDots = cv2.contourArea(cnt) / ((settings["s1"] + settings["s2"]) / 2)

                # if amount dots < 1.5, it gets floored, thus only counted as 1 point
                # in this case apend the single dot to the list of single dots
                if math.floor(amountDots) == 1:
                    detectedContours.append(cnt)
                else:
                    # add the contour to the list of contours as often as a dot could fit into the form
                    for _ in range(math.floor(amountDots)):
                        multipleContours.append(cnt)

            else:

                tooBigContours.append(cnt)

    cv2.drawContours(contoursImg, detectedContours, -1, (0,180,0), 10) # draw detected contours
    cv2.drawContours(contoursImg, multipleContours, -1, (0,180,240), 10) # draw multiple contours
    cv2.drawContours(contoursImg, tooBigContours, -1, (0,0,255), 10) # draw contours which are too big

    countedDots = len(detectedContours) + len(multipleContours)

    # if the original image and the final image shall be overlayed
    if settings["overlay"] > 0.0:

        originalImage = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        cv2.addWeighted(originalImage, settings["overlay"],
                        contoursImg, 1.0 - settings["overlay"], 0.0, contoursImg)


    # convert image to other color space in order to apply 
    convertedImage = cv2.cvtColor(contoursImg, cv2.COLOR_BGR2RGB)

    if settings["showCountOnImage_count"]:
        # write the amount of counted dots onto the image
        cv2.putText(convertedImage, 
                    str(countedDots), 
                    settings["position_count"], 
                    cv2.FONT_HERSHEY_SIMPLEX,
                    settings["fontsize_count"], 
                    settings["color_count"], 
                    settings["lineWidth_count"]) 

    if settings["showTextOnImage_text"]:
        # write the name of file onto the image
        cv2.putText(convertedImage, 
                    os.path.basename(file), 
                    settings["position_text"], 
                    cv2.FONT_HERSHEY_SIMPLEX,
                    settings["fontsize_text"],  
                    settings["color_text"],
                    settings["lineWidth_text"])
                    
    # shall the image, containing the contours, be shown?
    if settings["showFinalImage"]:

        pil_img = Image.fromarray(convertedImage)

        ImageShow.show(pil_img)



    # save image
    if settings["saveImage"]:

        # compute image path name
        basename = os.path.basename(file)
        ending = ".jpg" if ".jpg" in basename else ".jpeg"

        bareBaseName = basename.replace(ending, "")

        saveImagePath = os.path.join(settings["saveDir"], bareBaseName + "_dotsCounted-" + str(countedDots) + ".jpg")

        # convert color space back to what cv2 is used to
        contoursImg = cv2.cvtColor(convertedImage, cv2.COLOR_RGB2BGR)
        cv2.imwrite(saveImagePath, contoursImg)


    print("Counted dots in file '" + os.path.basename(file) + "': " + str(countedDots))

    return countedDots