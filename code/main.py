# Author
# Name: Fabian Sieper
# Email: sieper.fabian@outlook.com


from countDots import countDots
from tkinter import Tk     
from tkinter.filedialog import askopenfilename, askdirectory
import os
from tqdm import tqdm
from helperFunctions import readSettings


print("Hello to my point counting program!")

# hide the tk window
Tk().withdraw() 

# Path to file, which contains the settings of the program
settingsPath = "settings.json"

settings = readSettings(settingsPath)

# create folder, in which the processed files are to be stored
saveDir = settings["saveDir"]

# only create if dir not already exists
if not os.path.exists(settings["saveDir"]):
    os.mkdir(settings["saveDir"])


# source = input("Would you like to use a file or a folder? To use a file, type 'file'!\n")

# shall the final, manipulated and and marked image be saved?

if settings["source"] == "file":    # if a file is selected

    # ask for file
    print("Select a jpg- or jpeg-file")
    file = askopenfilename(title="Select a jpg- or jpeg-file") 

    dotsCounted = 0

    if file.endswith(".jpg") or file.endswith(".jpeg"):

        dotsCounted = countDots(file = file, 
                                settings = settings) 

    else:
        print("[WARNING] - File could not be processed, as it is not of type 'jpeg' or 'jpg'")


    print("Amount of dots counted: " + str(dotsCounted))
    input()

else:       # if a foulder is to be selected

    print("Select a folder containing jpg-files")
    folder = askdirectory(title="Select a folder containing jpg-files")

    amountOfDotsCounted = 0     # tells how many dots have been counted so far
    amountFilesCounted = 0

    for file in tqdm(os.listdir(folder), "Files processed"):

        if file.endswith(".jpg") or file.endswith(".jpeg"):

            # count dots of file
            countedDots = countDots(os.path.join(folder, file), 
                                    settings = settings) 

            amountOfDotsCounted += countedDots

            # one additional file processed
            amountFilesCounted += 1


    
    print("Amount of files processed: " + str(amountFilesCounted))
    print("Amount of dots counted: " + str(amountOfDotsCounted))
    input()