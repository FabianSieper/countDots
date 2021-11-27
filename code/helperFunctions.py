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

        saturation_increase = np.array(loadedJson["saturation"]["saturationIncrease"])
        show_increase_sat_image = np.array(loadedJson["saturation"]["showImag"])

    except Exception as e:

        pass    # intended

    finally:

        return saturation_increase, show_increase_sat_image

        
        
# For testing purposes:
if __name__ == "__main__":

    readSizesFromJson("sizes.json")