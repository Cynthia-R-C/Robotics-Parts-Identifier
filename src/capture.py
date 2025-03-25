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
class Ref_INT:
    def __init__(self, value):
        self.value = value
    
    def plus1(self):
        self.value+=1
        
        
#Basic Function that finds current path
def get_current_path():
    return os.getcwd()


#Basic function that creates a directory
def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        assert os.path.exists(dir_name), "File Was Not Created, check path input"
    else:
        print(f"There already exists a directory {dir_name}, Saving there")
        

#Basic helper function that validates a video
def HELPER_valid_video(video):
    cap = cv2.VideoCapture(video)
    is_valid = cap.isOpened
    cap.release()
    return is_valid


#Basic helper function that displats an image
def HELPER_display(image):
    window = 'Image'
    #Display the image in a window called Image
    cv2.imshow(window, image)
    
    #Wait for key press
    cv2.waitKey(0)
    
    #Close the window 'Image'
    cv2.destroyWindow(window)


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


def get_angle_from_line(main_line):
    x1,y1,x2,y2 = main_line
    slope = (y2-y1)/(x2-x1)
    #tanx = opposite/adjacent
    #tanx = slope
    angle_with_axis = math.atan(slope)
    return angle_with_axis
    

#Since this background wont change we only need to find it once and capture these contours
def find_background(frame):
    #Convet to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #Gaussian Blur in order to isolate the important edges
    #Parameters: image, pixel matrix ur tryna blur out standard deviation (0 = auto)
    #TODO: test the Blur Matrix
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    #Apply Canny edge detection (parametrs described above)
    edges = cv2.Canny(blur, 50, 150)
    
    #Find Contours(aka closed outlined shape [Cauchy integral theorem :3. I like it when they = 0])
    #Parameters: Image, Outermost countours only, Only stores end points
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #TODO: assure that our background is max
    background = max(contours, key=cv2.contourArea)
    
    #Get the rectangle that best fits the background
    #(x,y) = top left corner. w = width, h = height.
    x, y, w, h = cv2.boundingRect(background)
    
    #return this rectangle
    return (x, y, w, h)


#gets the rotation matrix based on angle (based on moving our center to the origin then translating back)
def get_rotation_matrix(center, theta):
    rotation_matrix = np.array([
        [np.cos(theta), -np.sin(theta), (1 - np.cos(theta)) * center[0] + np.sin(theta) * center[1]],
        [np.sin(theta), np.cos(theta), (1 - np.cos(theta)) * center[1] - np.sin(theta) * center[0]]
    ])
    return rotation_matrix


#rotate the background about its center depending on the angle 
#might cut off some stuff What is the smallest square?
#if we rotate around the center then the diagonal is the diameter of the circle
#square enclosing this diameter is the smallest
def rotate_background(image, background, angle):
    #find the center of the background
    x,y,w,h = background
    
    roi = image[y:y+h, x:x+w]
    
    diagonal = int(math.sqrt(w**2 + h**2))
    
    canvas = np.zeros((diagonal, diagonal, roi.shape[2]), dtype=roi.dtype)
    
    '''
    the thing is we want this to be around 0,0
    we only have diagonal so we know we want to start at diagonal//2 so should start half back half in front 
    
    '''
    
    xBegin = diagonal//2 - w/2
    
    xEnd = diagonal//2 +w/2
    
    yBegin = diagonal//2 - h/2
    
    yEnd = diagonal//2 + h/2
        
    canvas[yBegin:yEnd, xBegin:xEnd] = roi
    
    center = (diagonal//2, diagonal//2)
    #
    rotation_matrix = get_rotation_matrix(center, angle)
    #TODO: figure out this constant 
    k = 100
    
    rotated_roi = cv2.warpAffine(canvas, rotation_matrix, (diagonal+k, diagonal+k))
    
    return rotated_roi
        

#saves the image to the output_dir under filename counter
def take_image(roi, output_dir, counter):
    save_path = os.path.join(output_dir, str(counter.value))
    counter.plus1
    cv2.imwrite(save_path, roi)
    

#test background
def test_find_background():
    video_path = input("video path: ")
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened():
        opened, frame = cap.read()
        if(opened):
            background = find_background(frame)
            if(len(background) == 0):
                print(f"There is no background")
            else:
                #draws the background of index 0(Hopefully only background),  in yellow, with width 2
                cv2.drawContours(frame, background, 0, (0,255,255), 2)
                print(len(background))
                cv2.imshow("Background", frame)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        else:
            print(f"Did not open the first frame")
    else:
        print(f"Did not open at all")
    cap.release()
    
    
def main():
    currentPath = get_current_path();
    uploadDir = currentPath+"/Videos"
    outputDir = currentPath+"/Output"
    count = Ref_INT(0)
    create_directory(uploadDir)
    create_directory(outputDir)
    #TODO: auto from server uploaded from video (from RPI)
    #TODO: (cont) create server and logic + RPI capture device aka camera + wifi
    t = input("Place videos in Videos directory, press a button when done")
    for video in os.listdir(uploadDir):
        video_path = os.path.join(uploadDir, video)
        cap = cv2.VideoCapture(video_path)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            #cv2.imshow('Cur' frame)
            background = find_background(frame)
            line = background_line(frame)
            theta = get_angle_from_line(line)
            rotated_roi = rotate_background(frame, background, theta)
            take_image(rotated_roi, outputDir, count)
            #const break with x
            if cv2.waitKey(1) & 0xFF == ord('x'):
                break
        
    
if __name__ == "__main__":
    main()
    

    
        
    
    
