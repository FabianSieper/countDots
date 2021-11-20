
import json

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



# For testing purposes:
if __name__ == "__main__":

    readSizesFromJson("sizes.json")