# Author
# Name: Fabian Sieper
# Email: sieper.fabian@outlook.com


import json
import numpy as np

# This function reads a json file
# Returns s1, s2, s3 (three sizes for the dots to be detected)
def readSizesFromJson(path = "settings.json"):

    # s1: minimal size of dots
    # s2: maximal size of dots
    # s3: maximal size of merged dots (e.g. dots in a line)

    # set default values
    s1 = 0
    s2 = 80
    s3 = 800

    # try to overwrite the values by reading a file
    try:
        file = open(path)
        loadedJson = json.load(file)

        s1 = loadedJson["sizes"]["s1"]
        s2 = loadedJson["sizes"]["s2"]
        s3 = loadedJson["sizes"]["s3"]

    except Exception as e:

        pass    # intended

    finally:

        return s1, s2, s3


# Reads the color range-values from a json file
# Returns two np arrays, containing the lower color and upper color border
def readColorRangeFromJson(path = "settings.json"):

    # set default values
    lower_color = np.array([45,28,0])
    upper_color = np.array([110,255,255])

    # try to overwrite the values by reading a file
    try:
        file = open(path)
        loadedJson = json.load(file)

        lower_color = np.array(loadedJson["color"]["lowerColor"])
        upper_color = np.array(loadedJson["color"]["upperColor"])

    except Exception as e:

        pass    # intended

    finally:

        return lower_color, upper_color

# Reads information about the saturation increasement of the image in order to detect colored dots
# Returns 
# ... a float which describes how much the saturation shall be increased
# ... a boolean, which tells if the sat-increased image shall be shown

def readSatIncreaseValues(path = "settings.json"):

    # set default values
    saturation_increase = 10.0
    show_increase_sat_image = False

    # try to overwrite the values by reading a file
    try:
        file = open(path)
        loadedJson = json.load(file)

        saturation_increase = loadedJson["saturation"]["saturationIncrease"]
        show_increase_sat_image = loadedJson["saturation"]["showImag"]

    except Exception as e:

        pass    # intended

    finally:

        return saturation_increase, show_increase_sat_image

        
# Reads information from settings-file whether the final image, which has the counted dots marked,
# shall be shown
def readShowFinalImage(path = "settings.json"):

    # set default value
    showFinalImage = False 

    # try to overwrite the values by reading a file
    try:
        file = open(path)
        loadedJson = json.load(file)

        showFinalImage = loadedJson["showFinalImage"]

    except Exception as e:

        pass    # intended

    finally:

        return showFinalImage


# Reads information whether the manipulated image shall be saved
def readSaveImage(path = "settings.json"):

    # set default value
    saveImage = True 

    # try to overwrite the values by reading a file
    try:
        file = open(path)
        loadedJson = json.load(file)

        saveImage = loadedJson["saveImage"]

    except Exception as e:

        pass    # intended

    finally:

        return saveImage

# Gets folder-path, in which the images shall be stored
def readSaveDir(path = "settings.json"):

    # set default value
    saveDir = "../processedFiles/" 

    # try to overwrite the values by reading a file
    try:
        file = open(path)
        loadedJson = json.load(file)

        saveDir = loadedJson["saveDir"]

    except Exception as e:

        pass    # intended

    finally:

        return saveDir

# How transparant shall the original image be, which is overlaye over the edited, final image?
# If the value is 0, the original image does simply not get layed over the edited one
def readOverlayOrigImage(path = "settings.json"):

    # set default value
    overlayOrigImage = 0.0

    # try to overwrite the values by reading a file
    try:
        file = open(path)
        loadedJson = json.load(file)

        overlayOrigImage = loadedJson["overlayOriginalImage"]

    except Exception as e:

        pass    # intended

    finally:

        return overlayOrigImage

def readSource(path = "settings.json"):

    # set default value
    source = "file"

    # try to overwrite the values by reading a file
    try:
        file = open(path)
        loadedJson = json.load(file)

        source = loadedJson["source"]

    except Exception as e:

        pass    # intended

    finally:

        return source

# For testing purposes:
if __name__ == "__main__":

    readSizesFromJson("sizes.json")