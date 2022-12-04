import os
import sys
import cv2
import base64
import json



def read_image(file_name):
    photo = cv2.imread(file_name, 0)        
    photo_in_base64 = base64.b64encode(photo) 
    photo_as_string = photo_in_base64.decode('utf-8')  
    photo_as_json = json.dumps({"Photo": photo_as_string}, indent=2)   
  #  print(photo_as_json)
    return photo_as_string

if __name__ == '__main__':
    files =os.listdir(".") 
   # print(files)
    file_name = "testingData/"+sys.argv[1]
    #print(file_name)
    output = read_image(file_name)
    print(output)


