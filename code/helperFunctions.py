# Author
# Name: Fabian Sieper
# Email: sieper.fabian@outlook.com


import json
import numpy as np
import cv2
import traceback

# Adds text on top of an image
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

    try:
        file = open(path)
        loadedJson = json.load(file)
        return loadedJson
    except:
        print("[ERROR] - Not able to load the setings file!")
        exit()

     

# Takes a path to a json file, containing settings
# takes a json, containing all settings

# Returns a dict with all read settings
def saveSettings(settings, path = "settings.json"):

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

# For testing purposes:
if __name__ == "__main__":

    readSettings("settings.json")
