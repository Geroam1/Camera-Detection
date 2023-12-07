import os
from DetectionFunctions import update_Circle, get_CircleBin


Circle_Text_File_path = "CircleBin.txt"
circle = get_CircleBin(Circle_Text_File_path)

print(circle)