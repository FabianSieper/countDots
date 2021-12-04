from ntpath import join
import tkinter
from tkinter.constants import HORIZONTAL, RAISED, ROUND
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

        self.originalImageCV = None
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

        # setup brush variables
        self.setupBrush()

        # set an image to the screen
        self.updateImage()

        # add stuff like buttons and slider
        self.addUIElements()

        # start the main loop
        self.window.mainloop()

    def setupBrush(self):
        # Idea from site: https://gist.github.com/nikhilkumarsingh/85501ee2c3d8c0cfa9d1a27be5781f06 
        self.old_x = None
        self.old_y = None
        self.line_width = self.settings["brush"]["linewidth"]
        self.color = "black"    
        
        
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def paint(self, event):

        self.line_width = self.settings["brush"]["linewidth"]


        if self.old_x and self.old_y:

            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=self.color,
                               capstyle=ROUND, smooth=True, splinesteps=36)

            # also draw on original image

            # compute how much bigger the original image is
            scaleUpOriginalImage = self.cv_img.shape[0] / int(self.canvasWidth * (self.height / self.width))

            # compute dots on the original image (wichnormally is bigger)
            original_point1 = (int(self.old_x * scaleUpOriginalImage), int(self.old_y * scaleUpOriginalImage))
            original_point2 = (int(event.x * scaleUpOriginalImage), int(event.y * scaleUpOriginalImage))

            self.originalImageCV = cv2.line(self.originalImageCV, 
                                            original_point1, 
                                            original_point2, 
                                            (0, 0, 0),
                                            int(self.line_width * scaleUpOriginalImage))

                                    
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def loadNewImage(self):

        self.imageName = askopenfilename()
        self.originalImageCV = cv2.imread(self.imageName)

        self.cv_img = cv2.cvtColor(self.originalImageCV, cv2.COLOR_BGR2RGB)

    def createCanvas(self):

        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        self.height, self.width, _ = self.cv_img.shape

        self.canvasHeight = int(self.canvasWidth * (self.height / self.width))

    
        self.canvas = tkinter.Canvas(self.window, width = self.canvasWidth, height = self.canvasHeight)
        self.canvas.pack()

    def addSlider(self):
        # --------------------------------
        # Add settings slider

        # create a frame for the slider section
        self.slider_frame1 = tkinter.Frame(self.window)
        self.slider_frame1.pack(fill=tkinter.X, side=tkinter.BOTTOM)

        # contrast
        # label for contrast slider
        self.contrLabel = tkinter.Label(self.slider_frame1, text="Contrast")
        self.contrLabel.grid(row = 0, column=0)

        # contrast slider
        self.contrSlider = tkinter.Scale( self.slider_frame1, 
                                        from_=0, 
                                        to=50, 
                                        orient=HORIZONTAL, 
                                        length = self.canvasWidth / 2, 
                                        command=self.contrChanged)
                                        
        self.contrSlider.grid(row = 1, column=0, sticky = tkinter.W + tkinter.E)
        self.contrSlider.set(self.settings["contrast"]["contrastIncrease"])

        # saturation
        # label for saturation slider
        self.saturLabel = tkinter.Label(self.slider_frame1, text="Saturation")
        self.saturLabel.grid(row = 0, column=1)

        self.satSlider = tkinter.Scale( self.slider_frame1, 
                                        from_=0, 
                                        to=50, 
                                        orient=HORIZONTAL, 
                                        length = self.canvasWidth / 2, 
                                        command=self.saturationChanged)

        self.satSlider.grid(row = 1, column=1, sticky = tkinter.W + tkinter.E)
        self.satSlider.set(self.settings["saturation"]["saturationIncrease"])

        self.slider_frame1.columnconfigure(0, weight=1)
        self.slider_frame1.columnconfigure(1, weight=1)
        self.slider_frame1.columnconfigure(2, weight=1)
        self.slider_frame1.columnconfigure(3, weight=1)

    def addButtons(self):
        
        # ---------------------------------
        # Add buttons to gui

        self.button_frame = tkinter.Frame(self.window)
        self.button_frame.pack(fill=tkinter.X, side=tkinter.BOTTOM)

        self.resetDrawingButton = tkinter.Button(self.button_frame, command=self.resetDrawing, text="Reset")
        self.resetDrawingButton.grid(row = 0, column = 0, sticky = tkinter.W + tkinter.E)

        self.showContrImgButton = tkinter.Button(self.button_frame, command=self.computeAndShowContrImg, text="ShowContrImg")
        self.showContrImgButton.grid(row = 0, column = 1, sticky = tkinter.W + tkinter.E)

        self.showSatImgButton = tkinter.Button(self.button_frame, command=self.computeAndShowSatImg, text="ShowSatImg")
        self.showSatImgButton.grid(row = 0, column = 2, sticky = tkinter.W + tkinter.E)

        self.computeButton = tkinter.Button(self.button_frame, command=self.computeAndShowFinalImg, text="Compute")
        self.computeButton.grid(row = 0, column = 3, sticky = tkinter.W + tkinter.E)

        self.saveImageButton = tkinter.Button(self.button_frame, command=self.saveFinalImage, text="SaveFinalImage")
        self.saveImageButton.grid(row = 0, column = 4, sticky = tkinter.W + tkinter.E)

        # configure the button frame
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.button_frame.columnconfigure(3, weight=1)
        self.button_frame.columnconfigure(4, weight=1)

    # reload the manipulated image, in order to remove the drawn elements
    def resetDrawing(self):

        self.originalImageCV = cv2.imread(self.imageName)
        self.cv_img = cv2.cvtColor(self.originalImageCV, cv2.COLOR_BGR2RGB)

        self.updateImage(self.cv_img)

    def addUIElements(self):

        self.addSlider()
        
        self.addButtons()

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
        
        # convert original image to pil-image
        img = cv2.cvtColor(self.originalImageCV, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)

        # compute contrast-boosted image
        contrImage = increaseContrast(self.settings, self.imageName, im_pil.copy())

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