import tkinter
from tkinter.constants import CENTER, HORIZONTAL, RAISED, ROUND
import cv2
import PIL.Image, PIL.ImageTk
from tkinter.filedialog import askopenfilename, askdirectory
from helperFunctions import readSettings, saveSettings
from countDots import increaseContrast, incraseSaturation, getCountours, getFinalImage, pilToOpenCVImage, saveImage
from PIL import Image
import numpy as np
import os

class App:
    def __init__(self, window, window_title, canvasWidth = 400, settingsPath = "settings.json"):

        # read settings
        self.settings = readSettings(settingsPath)

        # set object-values
        self.canvasSize = self.settings["canvasSize"]

        ## for single file processing
        self.imageName = None
        ## for processing of multiple files
        self.imageDir = None
        self.listOfImages = []
        self.imageIndex = 0

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

    def loadNewImage(self, loadFirstImage = True):

        # check if a single file or a whole folder shall be computed
        if self.settings["source"] == "file":
            self.imageName = askopenfilename()

        elif loadFirstImage:  # if no file has been read of the folder by now
            self.imageDir = askdirectory()  
            self.listOfImages = os.listdir(self.imageDir)
            self.imageName = os.path.join(self.imageDir, self.listOfImages[self.imageIndex])

        else:   # if images already have been read
            self.imageName = os.path.join(self.imageDir, self.listOfImages[self.imageIndex])

        self.originalImageCV = cv2.imread(self.imageName)

        # transpose image if the image is in portrait mode
        if self.originalImageCV.shape[0] > self.originalImageCV.shape[1]:
            self.originalImageCV = cv2.transpose(self.originalImageCV)

        self.cv_img = cv2.cvtColor(self.originalImageCV, cv2.COLOR_BGR2RGB)


    def createCanvas(self, update = False):

        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        self.height, self.width, _ = self.cv_img.shape

        # adjust the size of the canvas depending on the format of the image
        if self.height > self.width:

            self.canvasHeight = self.canvasSize
            self.canvasWidth =  int(self.canvasHeight * (self.width / self.height))

        else:
            self.canvasWidth = self.canvasSize
            self.canvasHeight =  int(self.canvasWidth * (self.height / self.width))

        if not update:
            self.canvas = tkinter.Canvas(self.window, width = self.canvasWidth, height = self.canvasHeight)
            self.canvas.pack()
        else:
            self.canvas.config(width = self.canvasWidth, height = self.canvasHeight)

    def updateSize1(self, value):

        self.settings["sizes"]["s1"] = int(value)

    def updateSize2(self, value):

        self.settings["sizes"]["s2"] = int(value)

    def updateSize3(self, value):

        self.settings["sizes"]["s3"] = int(value)

    def updateBrushSize(self, value):

        self.settings["brush"]["linewidth"] = int(value)

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
                                        from_=1, 
                                        to=15, 
                                        orient=HORIZONTAL, 
                                        length = self.canvasWidth / 3, 
                                        command=self.contrChanged)
                                        
        self.contrSlider.grid(row = 1, column=0, sticky = tkinter.W + tkinter.E)
        self.contrSlider.set(self.settings["contrast"]["contrastIncrease"])

        # saturation
        # label for saturation slider
        self.saturLabel = tkinter.Label(self.slider_frame1, text="Saturation")
        self.saturLabel.grid(row = 0, column=1)

        # slider for saturation
        self.satSlider = tkinter.Scale( self.slider_frame1, 
                                        from_=1, 
                                        to=100, 
                                        orient=HORIZONTAL, 
                                        length = self.canvasWidth / 3, 
                                        command=self.saturationChanged)

        self.satSlider.grid(row = 1, column=1, sticky = tkinter.W + tkinter.E)
        self.satSlider.set(self.settings["saturation"]["saturationIncrease"])

        # label for brush size
        self.brushLabel = tkinter.Label(self.slider_frame1, text="Brush size")
        self.brushLabel.grid(row = 0, column=2)

        # slider for brush size
        self.brushSlider = tkinter.Scale( self.slider_frame1, 
                                        from_=0, 
                                        to=100, 
                                        orient=HORIZONTAL, 
                                        length = self.canvasWidth / 3, 
                                        command=self.updateBrushSize)

        self.brushSlider.grid(row = 1, column=2, sticky = tkinter.W + tkinter.E)
        self.brushSlider.set(self.settings["brush"]["linewidth"])

        # sizes of dots
        # label for dot size 1
        self.size1Label = tkinter.Label(self.slider_frame1, text="Smallest dots")
        self.size1Label.grid(row = 2, column = 0)

        # slider for size 1
        self.size1Slider = tkinter.Scale(self.slider_frame1,
                                        from_=0,
                                        to=2000,
                                        orient=HORIZONTAL,
                                        length=self.canvasWidth / 3,
                                        command=self.updateSize1)
        self.size1Slider.grid(row = 3, column = 0, sticky = tkinter.W + tkinter.E)
        self.size1Slider.set(self.settings["sizes"]["s1"])

        # label for dot size 2
        self.size2Label = tkinter.Label(self.slider_frame1, text="Biggest dots")
        self.size2Label.grid(row = 2, column = 1)
        
        # slider for size 2
        self.size2Slider = tkinter.Scale(self.slider_frame1,
                                        from_=0,
                                        to=10000,
                                        orient=HORIZONTAL,
                                        length=self.canvasWidth / 3,
                                        command=self.updateSize2)
        self.size2Slider.grid(row = 3, column = 1, sticky = tkinter.W + tkinter.E)
        self.size2Slider.set(self.settings["sizes"]["s2"])

        # label for dot size 3
        self.size3Label = tkinter.Label(self.slider_frame1, text="Max Dot collection-size")
        self.size3Label.grid(row = 2, column = 2)

        # slider for size 3
        self.size3Slider = tkinter.Scale(self.slider_frame1,
                                        from_=0,
                                        to=30000,
                                        orient=HORIZONTAL,
                                        length=self.canvasWidth / 3,
                                        command=self.updateSize3)
        self.size3Slider.grid(row = 3, column = 2, sticky = tkinter.W + tkinter.E)
        self.size3Slider.set(self.settings["sizes"]["s3"])

        self.slider_frame1.columnconfigure(0, weight=1)
        self.slider_frame1.columnconfigure(1, weight=1)
        self.slider_frame1.columnconfigure(2, weight=1)

    def addButtons(self):
        
        # ---------------------------------
        # Add buttons to gui

        # frame for all of the buttons
        self.button_frame = tkinter.Frame(self.window)
        self.button_frame.pack(fill=tkinter.X, side=tkinter.BOTTOM)

        columnCounter = 0

        # if multiple images shall be process, add a "next" button,
        if self.settings["source"] != "file":

            self.nextImgButton = tkinter.Button(self.button_frame, command=self.nextImage, text="Next Image", anchor=CENTER)
            self.nextImgButton.grid(row = 0, column = 6)

            self.prevImgButton = tkinter.Button(self.button_frame, command=self.prevImage, text="Previous Image", anchor=CENTER)
            self.prevImgButton.grid(row = 0, column = columnCounter)
            columnCounter += 1

        ## append static buttons
        self.resetDrawingButton = tkinter.Button(self.button_frame, command=self.resetDrawing, text="Reset")
        self.resetDrawingButton.grid(row = 0, column = columnCounter, sticky = tkinter.W + tkinter.E)
        columnCounter += 1

        self.showContrImgButton = tkinter.Button(self.button_frame, command=self.computeAndShowContrImg, text="ShowContrImg")
        self.showContrImgButton.grid(row = 0, column = columnCounter, sticky = tkinter.W + tkinter.E)
        columnCounter += 1

        self.showSatImgButton = tkinter.Button(self.button_frame, command=self.computeAndShowSatImg, text="ShowSatImg")
        self.showSatImgButton.grid(row = 0, column = columnCounter, sticky = tkinter.W + tkinter.E)
        columnCounter += 1

        self.computeButton = tkinter.Button(self.button_frame, command=self.computeAndShowFinalImg, text="Compute")
        self.computeButton.grid(row = 0, column = columnCounter, sticky = tkinter.W + tkinter.E)
        columnCounter += 1

        self.saveImageButton = tkinter.Button(self.button_frame, command=self.saveFinalImage, text="SaveFinalImage")
        self.saveImageButton.grid(row = 0, column = columnCounter, sticky = tkinter.W + tkinter.E)
        columnCounter += 1

        # configure the button frame
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.button_frame.columnconfigure(3, weight=1)
        self.button_frame.columnconfigure(4, weight=1)

        if self.settings["source"] != "file":

            self.button_frame.columnconfigure(5, weight=1)
            self.button_frame.columnconfigure(6, weight=1)


    # sets the next image in the list of images 
    def nextImage(self):

        self.imageIndex += 1

        if len(self.listOfImages) > self.imageIndex and self.imageDir != None:
            
            self.imageName = os.path.join(self.imageDir, self.listOfImages[self.imageIndex])
            self.loadNewImage(loadFirstImage=False) # reads the new image 
            self.createCanvas(update=True)
            self.updateImage(self.cv_img)

        elif len(self.listOfImages) <= self.imageIndex:

            print("[INFO] - The last image inside of the folder has been reached.")
            self.imageIndex = len(self.listOfImages) - 1

        else:

            print("[WARNING] - Not able to go to load the next image!")

    # sets the previous image in the list of images 
    def prevImage(self):

        self.imageIndex -= 1

        if 0 <= self.imageIndex and self.imageDir != None:
            
            self.imageName = os.path.join(self.imageDir, self.listOfImages[self.imageIndex])
            self.loadNewImage(loadFirstImage=False) # reads the new image 
            self.createCanvas(update=True)
            self.updateImage(self.cv_img)

        elif 0 > self.imageIndex:

            print("[INFO] - The first image inside of the folder has been reached.")
            self.imageIndex = 0

        else:

            print("[WARNING] - Not able to go to load the previous image!")


    # reload the manipulated image, in order to remove the drawn elements
    def resetDrawing(self):

        self.originalImageCV = cv2.imread(self.imageName)
        self.cv_img = cv2.cvtColor(self.originalImageCV, cv2.COLOR_BGR2RGB)

        self.updateImage(self.cv_img)

    def addUIElements(self):

        self.addButtons()
        
        self.addSlider()

    def saveFinalImage(self):

        finalImgPIL, countedDots = self.computeFinalImg()

        saveImage(self.imageName, self.settings, countedDots, pilToOpenCVImage(finalImgPIL))


    def computeFinalImg(self):

        # TODO: contrImg and orignalImg have transposed sizes
        
        satImg = self.computeSatImg()
        originalImg = self.originalImageCV
        
        contrImg, detectedContours, multipleContours, tooBigContours = getCountours(self.settings, satImg)

        finalImg, amountCountedDots = getFinalImage(detectedContours, multipleContours, self.settings, contrImg, originalImg, self.imageName)

        self.finalImage = pilToOpenCVImage(finalImg)

        return finalImg, amountCountedDots

    def computeAndShowFinalImg(self):

        finalImg, amountCountedDots = self.computeFinalImg()

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