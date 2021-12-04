import tkinter
from tkinter.constants import HORIZONTAL
import cv2
import PIL.Image, PIL.ImageTk
from tkinter.filedialog import askopenfilename
from helperFunctions import readSettings, saveSettings
from countDots import increaseContrast, incraseSaturation, getCountours, getFinalImage, pilToOpenCVImage, saveImage
from PIL import Image
import numpy as np


class App:
    def __init__(self, window, window_title, canvasWidth = 400, settingsPath = "settings.json"):

        # read settings
        self.settings = readSettings(settingsPath)

        # set object-values
        self.canvasWidth = self.settings["canvasWidth"]

        self.contrImage = None
        self.satImage = None
        self.finalImage = None

        # create tkinter window
        self.window = window
        self.window.title(window_title)

        # Load an image using OpenCV
        self.loadNewImage()

        # Create a canvas that can fit the above image
        self.createCanvas()

        # set an image to the screen
        self.updateImage()

        # add stuff like buttons and slider
        self.addUIElements()

        # start the main loop
        self.window.mainloop()

    def loadNewImage(self):

        self.imageName = askopenfilename()
        self.cv_img = cv2.cvtColor(cv2.imread(self.imageName), cv2.COLOR_BGR2RGB)

    def createCanvas(self):

        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        self.height, self.width, _ = self.cv_img.shape

        self.canvasHeight = int(self.canvasWidth * (self.height / self.width))

    
        self.canvas = tkinter.Canvas(self.window, width = self.canvasWidth, height = self.canvasHeight)
        self.canvas.pack()

    def addUIElements(self):

        # --------------------------------
        # Add settings slider
        # contrast
        self.contrSlider = tkinter.Scale( self.window, 
                                        from_=0, 
                                        to=50, 
                                        orient=HORIZONTAL, 
                                        length = self.canvasWidth, 
                                        command=self.contrChanged)
                                        
        self.contrSlider.pack(anchor=tkinter.CENTER, expand=True)
        self.contrSlider.set(self.settings["contrast"]["contrastIncrease"])

        # saturation
        self.satSlider = tkinter.Scale( self.window, 
                                        from_=0, 
                                        to=50, 
                                        orient=HORIZONTAL, 
                                        length = self.canvasWidth, 
                                        command=self.saturationChanged)

        self.satSlider.pack(anchor=tkinter.CENTER, expand=True)
        self.satSlider.set(self.settings["saturation"]["saturationIncrease"])

        # ---------------------------------
        # Add button for start computing

        self.button_frame = tkinter.Frame(self.window)
        self.button_frame.pack(fill=tkinter.X, side=tkinter.BOTTOM)

        self.showContrImgButton = tkinter.Button(self.button_frame, command=self.computeAndShowContrImg, text="ShowContrImg")
        self.showContrImgButton.grid(row = 0, column = 0, sticky = tkinter.W + tkinter.E)

        self.showSatImgButton = tkinter.Button(self.button_frame, command=self.computeAndShowSatImg, text="ShowSatImg")
        self.showSatImgButton.grid(row = 0, column = 1, sticky = tkinter.W + tkinter.E)

        self.computeButton = tkinter.Button(self.button_frame, command=self.computeAndShowFinalImg, text="Compute")
        self.computeButton.grid(row = 0, column = 2, sticky = tkinter.W + tkinter.E)

        self.saveImageButton = tkinter.Button(self.button_frame, command=self.saveFinalImage, text="SaveFinalImage")
        self.saveImageButton.grid(row = 0, column = 3, sticky = tkinter.W + tkinter.E)

        # configure the button frame
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.button_frame.columnconfigure(3, weight=1)


    def saveFinalImage(self):

        finalImgPIL, countedDots = self.computeFinalImg()

        saveImage(self.imageName, self.settings, countedDots, pilToOpenCVImage(finalImgPIL))


    def computeFinalImg(self):

        satImg = self.computeSatImg()
        originalImg = Image.open(self.imageName)

        contrImg, detectedContours, multipleContours, tooBigContours = getCountours(self.settings, satImg)
        finalImg, amountCountedDots = getFinalImage(detectedContours, multipleContours, self.settings, contrImg, originalImg, self.imageName)

        self.finalImage = pilToOpenCVImage(finalImg)

        return finalImg, amountCountedDots

    def computeAndShowFinalImg(self):

        satImg = self.computeSatImg()
        originalImg = Image.open(self.imageName)

        contrImg, detectedContours, multipleContours, tooBigContours = getCountours(self.settings, satImg)
        finalImg, amountCountedDots = getFinalImage(detectedContours, multipleContours, self.settings, contrImg, originalImg, self.imageName)

        self.finalImage = pilToOpenCVImage(finalImg)

        self.updateImage(self.finalImage)

    def computeContrImg(self):

        img = Image.open(self.imageName)
        contrImage = increaseContrast(self.settings, self.imageName, img.copy())

        self.contrImage = pilToOpenCVImage(contrImage)

        return contrImage

    def computeAndShowContrImg(self):
        
        self.computeContrImg()

        self.updateImage(self.contrImage)

    def computeSatImg(self):

        contrImg = self.computeContrImg()

        # compute saturation image on top
        satImage = incraseSaturation(self.settings, self.imageName, contrImg)
        self.satImage = pilToOpenCVImage(satImage)

        return satImage

    def computeAndShowSatImg(self):

        self.computeSatImg()

        self.updateImage(self.satImage)

        
    def updateImage(self, openCVImage = np.array([])):

        print(len(openCVImage))
        if len(openCVImage) == 0:
            openCVImage = self.cv_img

        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        resizedImage = cv2.resize(openCVImage, (self.canvasWidth, self.canvasHeight), interpolation=cv2.INTER_AREA)

        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(resizedImage))

        # Add a PhotoImage to the Canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Updating the saturation setting
    def saturationChanged(self, value):

        self.settings["saturation"]["saturationIncrease"] = int(value)

    # Updating the contrast settings
    def contrChanged(self, value):

        self.settings["contrast"]["contrastIncrease"] = int(value)

    # when program is closed, save the settings to file
    def __del__(self):

        saveSettings(self.settings)

        print("[INFO] - Saved settings")

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")