import os
import numpy as np
import cv2
from pathlib import Path
'''
Goal of this File:
To help Generate a multitude of Training data through OpenCV
We will be taking an input of a video file and then outputting a directory of Images
These Images will be used as training data
We also need ot keep in mind that this data might be rotated
Thus we can use OpenCV's Hough Line Transform in Order to get the rotation of a background line
Then we can simply subtract the angles to get the Theta Rotation
Next we rotate Screen Capture by this
We proceed to Capture Images as normal and described by the Reference File (My Own EcoDrones image capturing in C++)
'''

#Basic Function that finds current path
def get_current_path():
    return os.getcwd()

def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        assert os.path.exists(dir_name), "File Was Not Created, check path input"
    else:
        print(f"There already exists a directory {dir_name}, Saving there")
def def_get_background_angles(source_image):
    #convert to grayscale
    gray = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
    
    
    
