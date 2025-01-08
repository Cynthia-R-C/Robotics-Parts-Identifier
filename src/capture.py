import os
import math
from pathlib import Path
import numpy as np
import cv2
MAINLINE_LENGTH = 100 #TODO: find this length

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
        
def find_line_of_length_MAIN(lines):
    assert lines != None, "Background_line is not returning anything, check that function"
    for line in lines:
        x1, y1, x2, y2 = line[0] #returns a 3d array, extra wrapper around the line
        length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        if length == MAINLINE_LENGTH:
            return line
    print(f"Debug Constant. Lines cannot find any line of that length")
def background_line(source_image):
    #convert to grayscale
    gray = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
    #Now we need to run edge Dection (We use OpenCV's Canny edge detection)
    #thresholds (first two ints) for Hysteresis Thresholding lower means that splotches are more likely to be turned white
    #Higher means that splotches are also harder to detect
    '''
    Hysteresis thresholding: Uses a loop to turn pixels above the upper threshold white. 
    The run a BFS on nearby. If above lower threshold also turn white
    '''
    #apertureSize = 3-7 and odd, Higher captures higher detail
    #Final optional parameter are L2 Gradients, helps with edge gradient (aka find the strongest change in pixel color for possible edges)
    edges = cv2.Canny(gray, 50, 150, apertureSize=5)
    #now that the image is converted to grayscale input into Hough Line
    #how do we find center of rotation?
    #second parameter rho, increase if too many redunant lines (precision of distance parameter)
    #other two parameters minlinelenght and maxlinegap 
    #TODO: increase the threshold so that the thick long line in the background will recieve more votes
    #thus be filitered to be the only line
    lines = cv2.HoughLinesP(gray, 1, np.pi / 180, 100)
    #TODO: find a way to filter all possible lines. Maybe By lengths
    main_line = find_line_of_length_MAIN(lines)
    return main_line

    
        
    
    
