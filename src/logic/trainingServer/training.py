import numpy as np
import os
import cv2
import json
import re
#---------------------------------------------------
# Trainer (class)
#
#Trainer uses a set of training images and used the eigen faces algorithm to build a model.
#This process involves:
#   - Reading each input images as a grayscale flattened vector
#   - Creating a matrix, where each column in the matrix is a flattened image
#   - Calcualting the mean column of the matrix
#   - Subtracting the mean column from each column in the matrix
#   - Calculating the Covarience matrix of the above matrix
#   - Calcualting eigen values and eigen vectors of the covarience matrix
#   - Ordering the eigen vectors according to their corresponding eigen values
#   - Determining the top N eigen vectors that make up 95% of the difference
#   - Calcualting the Weights of the eigen vectors
#   - Saving the model informaiton in json format 
#---------------------------------------------------
class Trainer:
    
    #this initializes all the variables
    def __init__(self, height, width, num_images, img_path):

        self.height = height  #height of the training image
        self.width = width    #width of the training image
        self.num_images = num_images #number of training images
        self.img_path = img_path #the path of the training images

        #this matrix will contains all the training images after the
        #images have been flattened
        self.L = np.empty(shape=(self.height * self.width, num_images))

        #this will contain the Covariance matrix
        self.LTL = []

        #these hold the eigen values and eigen vectors
        self.eValues = []
        self.eVectors = []

        #this is the number of eigen values that make of 95% of the total sum
        self.K = 0

        #this holds the normalised evectors
        self.norms = []

        #this holds the weights corresponding to the evectors
        self.Weights = []

        #this list hold all the names of the training files
        self.training_names = self.sorted_alphanumeric(os.listdir(self.img_path))
        
        #this vector holds the mean vector of L
        self.mean_vector = []

    #---------------------------------
    #sorted_alphanumeric(self, data)
    #
    #This methods receives a list containing strings and sorts them in sorted alphanumeric order
    #---------------------------------
    def sorted_alphanumeric(self, data):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
        return sorted(data, key=alphanum_key)

    #--------------------------------
    #read_images(self,)
    #
    #This methods reads all of the training images in grayscale using the open-cv library
    #Then it flattens all of the images into a vectors and adds them as columns in the
    #matrix L
    #--------------------------------
    def read_images(self,):
        index = 0
        for name in self.training_names:
            try:
                image = cv2.imread(self.img_path+name,0) #0 reads the image in grayscale
            except:
                print(f"Error while reading training images. File name = {name}")
            self.L[:,index] = np.array(image, dtype='float64').flatten()[:]
            index += 1

    #--------------------------------
    #subtract_mean_face(self,)
    #
    #This methods calculates the mean column from the matrix L
    #Then it subtracts the mean column from every column in L
    #--------------------------------
    def subtract_mean_face(self,):
        
        self.mean_vector = np.sum(self.L, axis=1) / self.num_images
        for i in range(self.num_images):
            self.L[:,i] -= self.mean_vector[:]

    #--------------------------------
    #Covariance(self,)
    #
    #This methos calculates the covariance matrix of L
    #Then it calcualtes the eigen values and eigen vectors of L
    #--------------------------------
    def Covariance(self,):
        self.LTL = np.matrix(self.L.transpose()) * np.matrix(self.L)  
        self.LTL /= self.num_images

        self.eValues, self.eVectors = np.linalg.eig(self.LTL)

    #--------------------------------
    #find_k(self,)
    #
    #This method orders the eigenvectors according to their eigen values
    #in descending order. Then it calcualtes the number of eigen values
    #it takes to make up 95% of the sum of all eigen values. Then it 
    #removes any eigen vectors that i not part of the 95%
    #--------------------------------
    def find_k(self):
        sort_indices = self.eValues.argsort()[::-1]

        self.eValues = self.eValues[sort_indices]
        self.eVectors = self.eVectors[sort_indices]

        #find K
        self.K = 0
        curr_sum = 0
        total_sum = np.sum(self.eValues)
        for v in self.eValues:
            curr_sum += v

            if curr_sum / total_sum > 0.95:
                break
            else:
                self.K += 1

    #--------------------------------
    #find_weights(self,)
    #
    #This method uses numpy to normalize the eigen vectors
    #and calculates the weight of each eigen vector
    #--------------------------------
    def find_weights(self,):

        #first reduce the number of eigen vectors and values to K
        self.eValues = self.eValues[0:self.K]
        self.eVectors = self.eVectors[:,0:self.K]

        #normalise evectors and find weights
        self.eVectors = self.L * self.eVectors 
        self.norms = np.linalg.norm(self.eVectors, axis=0)   
        self.eVectors = self.eVectors / self.norms

        self.Weights = self.eVectors.transpose() * self.L  

        self.eVectors = self.eVectors.transpose()

    #--------------------------------
    #run_training(self,)
    #
    #This methods runs all the methods necessary to 
    #train the model
    #--------------------------------
    def run_training(self,):
        self.read_images()
        self.subtract_mean_face()
        self.Covariance()
        self.find_k()
        self.find_weights()

    #--------------------------------
    #test_model(self, degub, stats, testpath)
    #
    #This method received the following parameters:
    #   - Degub: a boolean that determine if debug information if printed to console
    #   - Stats: a boolean that determines if stats of each test are printed to console
    #   - testpath: a string that contains the path of the test images
    #
    #This methods takes all of the test images privided and runs them
    #against the model to determine its accuracy.
    #--------------------------------
    def test_model(self, debug, stats, testpath):
        testing_names = os.listdir(testpath)
        wrong = 0
        correct = 0

        for name in testing_names:
            
            #read the input image in gray scale
            img = cv2.imread(testpath+name, 0)

            #flatten the input image
            img_col = np.array(img, dtype='float64').flatten() 

            #subtract the mean vector from the input image
            img_col -= self.mean_vector 

            #Reshape the image into a vector
            img_col = np.reshape(img_col, (self.width*self.height, 1))  
            
            #transpose the evectors and multiply them with the image vector
            S = self.eVectors * img_col  
            
            #subtract the input image(S) from each column in the weight matrix
            diff = self.Weights - S

            #normalize each column in the matrix.
            #normalize means sum all values in the column and 
            #divide them by the number of values in the column
            norm = np.linalg.norm(diff, axis=0) 
            
            #find the index of the smallest value 
            idx = np.argmin(norm)

            #print debug data
            if debug == True:
                print('================================================')
                print(f'Shape of W {self.Weights.shape}')
                print(f'Shape of mean col {self.mean_vector.shape}')
                print(f'Sahpe of evectors {self.eVectors.shape}')
                print(f'shape of img_col {img_col.shape}')
                print(f'shape of S {S.shape}')
                print(f'shape of diff {diff.shape}')
                print(f'shape or norms {norm.shape}')
                print('================================================')
                debug = False

            #find number of correct and incorrect
            t_name = name.split('_')[1]
            x = self.training_names[idx].split('_')[1]
            
            if t_name == x:
                correct += 1
                if stats == True: print(f'Correct! distance={norm[idx]}, index: {idx}, name: {name}')
            else:
                wrong += 1
                if stats == True: print(f'Wrong! distance={norm[idx]}, index: {idx}, name: {name}')

        print(f'Correct = {correct} Wrong = {wrong}')

if __name__ == '__main__':
    path = '../../../res/trainingData/'
    testing_path = '../../../res/testingData/'
    model = Trainer(height = 80, width = 70, num_images=320, img_path=path)
    model.run_training()
    model.test_model(debug=True, stats=True, testpath=testing_path)

    #read the weights matrix and store in the data folder
    W = model.Weights.transpose()
    arr2 = W.tolist()
    myJson = json.dumps(arr2)

    weightsPath = '../../persistance/seed/'
    f = open(weightsPath+'weights.json', 'w')
    f.write(myJson)
    f.close()

    dataPath = '../../logic/worker/data/'
    #read the eVectors and store in the data foler
    eV = model.eVectors
    arr2 = eV.tolist()
    myJson = json.dumps(arr2)

    f = open(dataPath+'eVectors.json', 'w')
    f.write(myJson)
    f.close()

    #read the mean vector and store it in the data folder
    myMean = model.mean_vector
    arr2 = myMean.tolist()
    myJson = json.dumps(arr2)

    f = open(dataPath+'meanVector.json', 'w')
    f.write(myJson)
    f.close()