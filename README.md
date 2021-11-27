# Count Dots

This project aims to count a number of (by default blue) dots on a image. It was originally build for counting amounts of cells on breeding grounds in order to simplify the tasks of e.g. chemists and biologists.



|                          Rare image                          |                       Selected points                        |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| <img src="images\rawDots.png" alt="rareDots" style="zoom:50%;" /> | <img src="images\selectedDots.png" alt="selectedDots" style="zoom:50%;" /> |

Dots outlined in **green** are recognized as one Dots. **Yellow** outlined dots were detected as a cluster of dots. The actual number of dots counted is determined by the area. If the area is twice as large as an average dot, two dots are counted for this.



## Installation

### Requirements
To use this application a python of version `3.9.7` (https://www.python.org/downloads/) or higher is recommended. Additionally the following packages are required:
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
## Usage

To run it simply run 
`python main.py`. You are asked to select whether you'd like to select a single file or multiple files inside of a folder (type "file" in order to select a single file). The selected file(s) are then processed, the amount of found dots displayed in the command line and an image (or multiple images) are saved under the folder `processedFiles/`. These images display which dots were found (green), which dots seem to be merged (yellow) and which areas aren't detected as dots (red).

### Merged dots
If some of the dots are to close to each other, it can appear that they are a single dot. For this, the area found is compared to the maximal set dot size. If the area is not _too_ large, the area is divided by the maximal dot-area. By this a approximate amount of dots is calculated. 

### Changing the dot size
As the size of dots (measured in area, amount of pixels) might differ between cameras, they can be changed. For this open the file `code/settings.json`and change the variables `s1, s2, s3` to your liking.

- s1: The minimal dot size. If a dot's area is smaller than `s1`, it won't be counted.
- s2: The maximal dot size. If a dot is between `s1` and `s2`, the dots are detected. If they are bigger than `s2`, they aren't detected as single but as multiple dots.
- s3: The maximal area a collection of dots can have. If an area is bigger than `s2`, the area might represent multiple dots, laying near each other. If the area is bigger than `s2` and also _smaller_ than `s3`, the size of the area is divided by the average dot size `(s1 + s2) / 2`. By doing so, a approximate amount of dots in this area can be calculated.


### Changing the color of interest
By default only dots with the color 'blue' are minded. To change the color range, you can simply modify the values `lowerColor` and `upperColor` in the file `code/settings.json`. The color values are set in the hsv-color space. Thus the values have to be:

```
Color = (Hue, Saturation, Value)
```

with the max values being

```
Color = (180, 360, 360)
```

### Changing the saturation boost

As some dots might not be as colorful as others, the option for boosting saturation exists. The file `code/settings.json` contains two values:

- `saturationIncrease`: How much shall the saturation be increased. The values `0` would describe no increase in saturation.
- `showImag`: Describes, if the saturated image shall be shown. This can be used in order to calibrate the program.

By default the saturation increase has the value `10` and no saturated increased image is shown.
