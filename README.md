# Count Dots

This project aims to count a number of dots on a image. It was originally build for counting amounts of cells on breeding grounds in order to simplify the tasks of e.g. chemists and biologists.

## Usage

To run it simply run 
`python main.py`. You are asked to select wheter you'd like to select a single file or multiple files inside of a folder (type "file" in order to select a single file). The selected file(s) are then processed, the amount of found dots displayed in the command line and an image (or multiple images) are saved under the folder `processedFiles/`. These images display which dots were found (green), which dots seem to be merged (yellow) and which areas are'nt detected as dots (red).

### Merged dots
If some of the dots are to close to each other, it can appear that they are a single dot. For this, the area found is compared to the maximal set dot size. If the area is not _too_ large, the area is divided by the maximal dot-area. By this a approximate amount of dots is calculated. 

### Change dot size
As the size of dots might differ between usages, they can be changed. For this open the file `countDots.py`and change the variables `s1, s2, s3` to your liking.

- s1: The minimal dot size. If a dot's area is smaller than `s1`, it won't be detected.
- s2: The maximal dot size. If a dot is between `s1` and `s2`, the dots are detected. If they are bigger than `s2`, they arent detected as single dots.
- s3: The maximal area a collection of dots can have. If an area is bigger than `s2`, the area might represent multiple dots, laying near each other. If the area is bigger than `s2` and also _smaller_ than `s3`, the size of the area is divided by the maximal dot size `s2`. By doing so, a approximate amount of dots in this area can be calculated.