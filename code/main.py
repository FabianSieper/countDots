from countDots import countDots
from tkinter import Tk     
from tkinter.filedialog import askopenfilename, askdirectory
import os
from tqdm import tqdm
from helperFunctions import readSatIncreaseValues

# hide the tk window
Tk().withdraw() 

# variable for increasement of saturation of the image
# ... this allows for a better hit rate when it comes to the selection of dots
# ... 
# saturation_increase: default -> 10.0

# bool variable, which describes if the image, whichs saturation got increased, shall be shown
# show_increase_sat_image: default -> False

saturation_increase, show_increase_sat_image = readSatIncreaseValues()

# create folder, in which the processed files are to be stored
saveDir = "../processedFiles/"
# only create if dir not already exists
if not os.path.exists(saveDir):
    os.mkdir(saveDir)

# source = input("Would you like to use a file or a folder? To use a file, type 'file'!\n")
source = "file"

if source == "file":    # if a file is selected

    # ask for file
    print("Select a jpg- or jpeg-file")
    file = askopenfilename(title="Select a jpg- or jpeg-file") 

    dotsCounted = 0

    filename = os.path.basename(file)

    if file.endswith(".jpg"):

        dotsCounted = countDots(file, os.path.join(saveDir, filename.replace(".jpg", "") + "_processed.jpg"), 
                                saturation_increase = saturation_increase,
                                show_increase_sat_image = show_increase_sat_image)

    elif file.endswith(".jpeg"):

            dotsCounted = countDots(file, os.path.join(saveDir, filename.replace(".jpeg", "") + "_processed.jpg"), 
                                                        saturation_increase = saturation_increase,
                                                        show_increase_sat_image = show_increase_sat_image)

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

        if file.endswith(".jpg"):

            # count dots of file
            countedDots = countDots(os.path.join(folder, file), os.path.join(saveDir, file.replace(".jpg", "") + "_processed.jpg"), 
                                    saturation_increase = saturation_increase,
                                    show_increase_sat_image = show_increase_sat_image) 
            amountOfDotsCounted += countedDots

            # one additional file processed
            amountFilesCounted += 1

        elif file.endswith(".jpeg"):

            # count dots of file
            countedDots = countDots(os.path.join(folder, file), os.path.join(saveDir, file.replace(".jpeg", "") + "_processed.jpg"),
                                    saturation_increase = saturation_increase,
                                    show_increase_sat_image = show_increase_sat_image)
            amountOfDotsCounted += countedDots

            # one additional file processed
            amountFilesCounted += 1
    
    print("Amount of files processed: " + str(amountFilesCounted))
    print("Amount of dots counted: " + str(amountOfDotsCounted))
    input()