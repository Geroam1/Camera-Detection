# imports required for reading the varible
import os
from DetectionFunctions import update_Circle, get_CircleBin

# defines the file path for the text file
Circle_Text_File_path = "CircleBin.txt"

# defines the binary variable
circle = get_CircleBin(Circle_Text_File_path)

print(circle)