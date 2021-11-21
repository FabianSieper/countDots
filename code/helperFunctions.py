
import json
import numpy as np

# This function reads a json file
# Returns s1, s2, s3 (three sizes for the dots to be detected)
def readSizesFromJson(path):

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

        s1 = loadedJson["s1"]
        s2 = loadedJson["s2"]
        s3 = loadedJson["s3"]

    except Exception as e:

        pass    # intended

    finally:

        return s1, s2, s3


# Reads the color range-values from a json file
# Returns two np arrays, containing the lower color and upper color border
def readColorRangeFromJson(path):

    # set default values
    lower_color = np.array([45,28,0])
    upper_color = np.array([110,255,255])

    # try to overwrite the values by reading a file
    try:
        file = open(path)
        loadedJson = json.load(file)

        lower_color = np.array(loadedJson["lowerColor"])
        upper_color = np.array(loadedJson["upperColor"])

    except Exception as e:

        pass    # intended

    finally:

        return lower_color, upper_color

        
# For testing purposes:
if __name__ == "__main__":

    readSizesFromJson("sizes.json")