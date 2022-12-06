# encode.py
# encodes image to a base64 string

import os
import sys
import cv2
import base64
import json


# read_image
# reads image file and converts it to a base64 string
# returns it as string 
def read_image(file_name):
    photo = cv2.imread(file_name, 0)        
    photo_in_base64 = base64.b64encode(photo) 
    photo_as_string = photo_in_base64.decode('utf-8')  
    return photo_as_string

if __name__ == '__main__':
    file_name = "testingData/"+sys.argv[1]
    output = read_image(file_name)
    print(output)    # outputs string for javascript backend to read


