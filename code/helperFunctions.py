# Author
# Name: Fabian Sieper
# Email: sieper.fabian@outlook.com


import json
import numpy as np
import cv2
import traceback

def addTextToImage(image, text, text_position, text_size, text_color, lineWidth):

    cv2.putText(image, 
        text, 
        text_position, 
        cv2.FONT_HERSHEY_SIMPLEX,
        text_size,  
        text_color,
        lineWidth) 

# Takes a path to a json file, which contains settings
# Returns a dict with all read settings
def readSettings(path = "settings.json"):

    # s1: minimal size of dots
    # s2: maximal size of dots
    # s3: maximal size of merged dots (e.g. dots in a line)

    # set default values
    s1 = 0
    s2 = 80
    s3 = 800

    lower_color = np.array([45,28,0])
    upper_color = np.array([110,255,255])

    saturation_increase = 10.0
    show_increase_sat_image = False

    contrast_increase = 1.0
    show_increase_contr_image = False

    showFinalImage = False 

    saveImage = True 

    saveDir = "../processedFiles/" 

    overlayOrigImage = 0.0

    source = "file"


    lineWidth_count = 3
    color_count = [209, 80, 0, 255]
    position_count = [50, 460]
    fontsize_count = 10
    showCountOnImage_count = True

    lineWidth_text = 3
    color_text = [209, 80, 0, 255]
    position_text = [50, 200]
    fontsize_text = 5
    showTextOnImage_text = True

    lineWidth_counted = 7
    color_counted = [209, 80, 0, 255]
    fontsize_counted = 5
    showTextOnImage_counted = True

    # try to overwrite the values by reading a file
    try:
        file = open(path)
        loadedJson = json.load(file)

        s1 = loadedJson["sizes"]["s1"]
        s2 = loadedJson["sizes"]["s2"]
        s3 = loadedJson["sizes"]["s3"]

        lower_color = np.array(loadedJson["color"]["lowerColor"])
        upper_color = np.array(loadedJson["color"]["upperColor"])

        saturation_increase = loadedJson["saturation"]["saturationIncrease"]
        show_increase_sat_image = loadedJson["saturation"]["showImage"]

        contrast_increase = loadedJson["contrast"]["contrastIncrease"]
        show_increase_contr_image = loadedJson["contrast"]["showImage"]

        showFinalImage = loadedJson["showFinalImage"]

        saveImage = loadedJson["saveImage"]

        saveDir = loadedJson["saveDir"]

        overlayOrigImage = loadedJson["overlayOriginalImage"]

        source = loadedJson["source"]

        lineWidth_count = loadedJson["countedDotsToImage"]["lineWidth"]
        color_count = loadedJson["countedDotsToImage"]["color"]
        position_count = loadedJson["countedDotsToImage"]["position"]
        fontsize_count = loadedJson["countedDotsToImage"]["fontSize"]
        showCountOnImage_count = loadedJson["countedDotsToImage"]["show"]

        lineWidth_text = loadedJson["fileNameToImage"]["lineWidth"]
        color_text = loadedJson["fileNameToImage"]["color"]
        position_text = loadedJson["fileNameToImage"]["position"]
        fontsize_text = loadedJson["fileNameToImage"]["fontSize"]
        showTextOnImage_text = loadedJson["fileNameToImage"]["show"]

        lineWidth_counted = loadedJson["amountDotsCounted"]["lineWidth"]
        color_counted = loadedJson["amountDotsCounted"]["color"]
        fontsize_counted = loadedJson["amountDotsCounted"]["fontSize"]
        showTextOnImage_counted = loadedJson["amountDotsCounted"]["show"]

    except Exception as e:
        
        print("[WARNING] - Not able to read settings. Default settings are used ...\nDoes the file exist, or does it maybe have some spelling errors inside of it? ")
        print(traceback.format_exc())

    finally:

        return {"s1" : s1, "s2" : s2, "s3" : s3, 
                "lower_color" : lower_color, "upper_color" : upper_color,
                "saturation_increase" : saturation_increase, "show_increase_sat_image" : show_increase_sat_image,
                "contrast_increase" : contrast_increase, "show_increased_contr_image" : show_increase_contr_image,
                "showFinalImage" : showFinalImage,
                "saveImage" : saveImage,
                "saveDir" : saveDir,
                "overlay" : overlayOrigImage,
                "source" : source,
                "lineWidth_count": lineWidth_count, "color_count" : color_count, "position_count" : position_count,
                "fontsize_count" : fontsize_count, "showCountOnImage_count" : showCountOnImage_count,
                "lineWidth_text": lineWidth_text, "color_text" : color_text, "position_text" : position_text,
                "fontsize_text" : fontsize_text, "showTextOnImage_text" : showTextOnImage_text,
                "lineWidth_counted": lineWidth_counted, "color_counted" : color_counted,
                "fontsize_counted" : fontsize_counted, "showTextOnImage_counted" : showTextOnImage_counted}

     

# For testing purposes:
if __name__ == "__main__":

    readSettings("settings.json")