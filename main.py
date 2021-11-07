from cv2 import solveCubic
from countDots import countDots
from tkinter import Tk     
from tkinter.filedialog import askopenfilename, askdirectory
import os
from tqdm import tqdm

import numpy as np

Tk().withdraw() 

# source = input("Would you like to use a file or a folder? To use a file, type 'file'!\n")
source = ""

if source == "file":    # if a file is selected

    # ask for file
    print("Select a jpg- or jpeg-file")
    file = askopenfilename(title="Select a jpg- or jpeg-file") 

    dotsCounted = countDots(file, "./save.jpg")

    print("Amount of dots counted: " + str(dotsCounted))
    input()

else:       # if a foulder is to be selected

    print("Select a folder containing jpg-files")
    folder = askdirectory(title="Select a folder containing jpg-files")

    amountOfDotsCounted = 0     # tells how many dots have been counted so far
    amountFilesCounted = 0

    # create folder, in which the processed files are to be stored
    saveDir = "./processedFiles/"

    # TODO: only create if dir not already exists
    if not os.path.exists(saveDir):
        os.mkdir(saveDir)

    for file in tqdm(os.listdir(folder), "Files processed"):

        if file.endswith(".jpg"):

            # count dots of file
            countedDots = countDots(os.path.join(folder, file), os.path.join(saveDir, file.replace(".jpg", "") + "_processed.jpg"))
            amountOfDotsCounted += countedDots

            # one additional file processed
            amountFilesCounted += 1

        elif file.endswith(".jpeg"):

            # count dots of file
            countedDots = countDots(os.path.join(folder, file), os.path.join(saveDir, file.replace(".jpeg", "") + "_processed.jpg"))
            amountOfDotsCounted += countedDots

            # one additional file processed
            amountFilesCounted += 1
    
    print("Amount of files processed: " + str(amountFilesCounted))
    print("Amount of dots counted: " + str(amountOfDotsCounted))
    input()