# Count Dots

This project aims to count a number of (by default blue) dots on an image. It was originally built for counting amounts of cells on breeding grounds in order to simplify the tasks of e.g. chemists and biologists.



|                          Raw image                           |                       Selected points                        |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| <img src="images\rawDots.jpg" alt="rawDots" style="zoom:50%;" /> | <img src="images\selectedDots.jpg" alt="selectedDots" style="zoom:50%;" /> |

Dots outlined in **green** are recognized as one Dots. **Yellow** outlined dots were detected as a cluster of dots. The actual number of dots counted is determined by the area. If the area is twice as large as an average dot, two dots are counted for this.



# Installation

### Requirements
To use this application a python of version `3.9.7` (https://www.python.org/downloads/) or higher is recommended. Additionally, the following packages are required:
- cv2
- tkinter
- tqdm
- numpy

To install these packages simply copy the following command into your command line:

```
pip install tk numpy opencv-python tqdm
```

### Pulling the project
To pull the project using git type the following line:
```
git clone https://github.com/FabianSieper/countDots
```
# Usage (GUI)

To run the GUI version of the program, enter the following line into your command line: 

```
python app.py
```

or **double click** the file _app.py_.

## Slides

You can modify contrast and saturation by sliding the corresponding slider. 

## Previews

There are three different previews, which can accessed:

- **Contrast boost**
  - Displays the original selected image, which has an increase in contrast. 
- **Saturation boost**
  - Displays the contrast-increased image in addition with an increase in saturation.
- **Final image**
  - Displays the final image, containing the detected dots, the amount of detected dots and further possibilities. For further possibilities read the section _Usage (Raw)_.

## Saving a processed image

If you are happy with your selected settings, you can save the final image by pressing the button _SaveFinalImage_.

## Selecting the Area of interest

Use the mouse to narrow down the area of interest by overdrawing areas. Points are not searched in overdrawn areas.

## Further settings

Further settings, have to be changed inside of the file `code/settings.json`. For further information lookup descriptions in secion _Usage (Raw)_. 

# Usage (Raw)

To run the raw scripts enter the following line into your command line: 

```
python main.py
```

or **double click** the file _main.py_. This requires python to be selected as the default application for files with the ending _.py_.

You are asked to select whether you'd like to select a single file or multiple files inside of a folder (type "file" to select a single file). The selected file(s) are then processed, the amount of found dots displayed in the command line and an image (or multiple images) are saved under the folder `processedFiles/`. These images display which dots were found (green), which dots seem to be merged (yellow) and which areas aren't detected as dots (red).

## Usage tips

For the best performance over multiple images, the _**same distance**_ to the dots should be maintained. This is, because the area detected is depending on the resolution of the dots, which varies when the distance varies. 

## Settings

All settings can be found in the file `code/settings.json`.

### Dot size
As the size of dots (measured in area, amount of pixels) might differ between cameras, they can be changed. For this adjust the variables _s1, s2, s3_ to your liking.

- `s1`: The minimal dot size. If a dot's area is smaller than _s1_, it won't be counted.
- `s2`: The maximal dot size. If a dot is between _s1_ and _s2_, the dots are detected. If they are bigger than _s2_, they aren't detected as single but as multiple dots.
- `s3`: The maximal area a collection of dots can have. If an area is bigger than _s2_, the area might represent multiple dots, laying near each other. If the area is bigger than _s2_ and also _smaller_ than _s3_, the size of the area is divided by the average dot size _(s1 + s2) / 2_. By doing so, an approximate amount of dots in this area can be calculated.

#### Color codes

- _green_ contours: A single detected dot
- _orange_ contours: Multiple detected dots
- _red_ contours: No dots detected, as the area is too big to be a bundle of dots

### Merged dots

If some of the dots are too close to each other, it can appear that they may be a single dot. For this, the area found is compared to the maximal set dot size. If the area is not *too* large, the area is divided by the maximal dot-area. By this, an approximate amount of dots is calculated. To show how many dots are approximated per found instance, set the parameter `show` underneath the parameter `amountDotsCounted` to _true_. 


### Color of interest
By default only dots with the color _blue_ are minded. To change the color range, you can simply modify the values `lowerColor` and `upperColor` in the settings. The color values are set in the hsv-color space. Thus the values have to be:

```
Color = [Hue, Saturation, Value]
```

with the max values being

```
Color = [180, 255, 255]
```

If you transfer color codes from other applications or websites, keep in mind the scale them accordingly.

### Contrast boost

If the image is washed out, or the dots might not be as distinguishable from each other, you can increase the contrast of the image. Settings regarding the contrast can be found underneath the parameter `contrast`.

- `contrastIncrease`: A number describing how much the contrast shall be increased. 
  - _<1_ describes a reduction in contrast
  - _=1_ has no effect on the contrast - it stays the same
  - _>1_ increases the contrast
- `showImage`: Describes, if the saturated image shall be shown. This option can be used in order to calibrate the program.

By default the saturation increase has the value _1_ and no image regarding the contrast is shown.

### Saturation boost

As some dots might not be as colorful as others, the option for boosting saturation exists. Settings regarding the saturation can be found underneath the parameter `saturation`. This option builds up on the settings _contrast_. At first the contrast is applied.

- `saturationIncrease`: How much shall the saturation be increased. The values _0_ would describe no increase in saturation.
  - `showImage`: Describes, if the saturated image shall be shown. This option can be used to calibrate the program.

By default, the saturation increase has the value _10_ and no saturated increased image is shown.

### Source

If you'd like to compute multiple files at once, you can place all your files inside of one folder. All files inside of this folder will be processed. For this, change the parameter `source` to _folder_. By default, only one file can be selected.

### Show final image

To automatically view the final image, which contains marked dots, set the parameter `showFinalImage` to _true_. By default, the value _false_ is set. However, it should be kept in mind, that showing the image at the end lowers the performance of the program. 

### Overlay original image

In addition to _Show final image_ it is also possible to overlay the original image with the image containing the marked dots. To enable this adjust the parameter `overlayOriginalImage`. The possible values range between _0.0_ and _1.0_, where 0.0 describes full transparency of the original image and 1.0 no transparency. A value of _0.8_ is recommended if wanted. By default, the value is _0.0_.

### Save the image

If you'd like to save the image, set the parameter `saveImage` to _true_. This also represents the default value. If no image shall be saved, set the value to _false_.

### Save directory

To change the folder where the final images will be saved, adjust the parameter `saveDir`. This parameter has to contain a path to a folder. By default, the images are saved inside the folder _processedFiles/_, which again lies inside the project folder.

### Write Description on Image

#### Counts

If you'd like to display the amount of dots counted on an image, you can enter the section `countedDotsToImage` inside of the settings-file. These parameters all belong to the text for displaying the amount of dots counted on an image.

- `show`: Shall the text be shown?
- `lineWidth`: How thick shall the text be?
- `color`: Which color shall the text be in?
- `position`: At which position shall the text be? _[x, y]_
- `fontSize`: How big shall the text be?

### Name of Image

If you'd like to display the name of a file on the image itself, you can enter the section `fileNameToImage` inside of the settings-file. These parameters all belong to the text for displaying the name of a file.

- `show`: Shall the text be shown?
- `lineWidth`: How thick shall the text be?
- `color`: Which color shall the text be in?
- `position`: At which position shall the text be? _[x, y]_
- `fontSize`: How big shall the text be?
