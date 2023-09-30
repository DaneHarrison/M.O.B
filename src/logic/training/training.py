import numpy as np
import os
import cv2
import json
import re

class Trainer:
    '''
    Trainer (Class)
    
    The trainer utilizes a curated set of training images and employs the eigenfaces algorithm to construct a model.
    This process involves the following steps:

    - Parsing each input image as a grayscale flattened vector
    - Constructing a matrix where each column represents a flattened image
    - Computing the mean column of the matrix
    - Normalizing each column by subtracting the mean column
    - Calculating the Covariance matrix of the normalized matrix
    - Determining eigenvalues and eigenvectors of the covariance matrix
    - Sorting the eigenvectors based on their corresponding eigenvalues
    - Selecting the top N eigenvectors that collectively capture 95% of the variance
    - Deriving the weights associated with these selected eigenvectors
    - Storing the model information in JSON format
    '''
    
    def __init__(self, height, width, num_images, img_path):

        '''
        Initializes the Trainer object.

        Parameters: 
            height (int): The height of each image in pixels
            width (int): The width of each image in pixels
            num_images (int): The total number of training images
            img_path (string): Path to the training images 
        '''

        self.height = height
        self.width = width
        self.num_images = num_images
        self.img_path = img_path

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

    def sorted_alphanumeric(self, data):

        '''
        Sorts a list of strigns in alphanumeric order

        Parameters:
            data (List[]): List of strings
        Returns:
            List [] : sorted list of strings
        '''

        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
        return sorted(data, key=alphanum_key)

    def read_images(self,):
        '''
        Reads all of the training images in grayscale using the open-cv library,
        then flattens all of the images into vectors and adds them as columns in the
        matrix L
        '''
        index = 0
        for name in self.training_names:
            try:
                image = cv2.imread(self.img_path+name,0) #0 reads the image in grayscale
            except:
                print(f"Error while reading training images. File name = {name}")
            self.L[:,index] = np.array(image, dtype='float64').flatten()[:]
            index += 1

    def subtract_mean_face(self,):
        '''
        Calculates the mean column from the matrix L, and subtracts it from every column in L
        '''
        
        self.mean_vector = np.sum(self.L, axis=1) / self.num_images
        for i in range(self.num_images):
            self.L[:,i] -= self.mean_vector[:]

    def Covariance(self,):
        '''
        Calculates the covariance matrix of L and its eigen values and eigen vectors
        '''
        self.LTL = np.matrix(self.L.transpose()) * np.matrix(self.L)  
        self.LTL /= self.num_images

        self.eValues, self.eVectors = np.linalg.eig(self.LTL)

    def find_k(self):
        '''
        Orders the eigen vectors of L according to their eigen values in descending order. 
        Calcualtes the number of top eigen values needed to make of 95% of the sum of all eigen values.
        Removes all the eigen vectors that do not correspond to the top 95%
        '''
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

    def find_weights(self,):
        '''
        Uses numpy to normalize the eigen vectors and calculates the weight of each eigen vector
        '''
        #first reduce the number of eigen vectors and values to K
        self.eValues = self.eValues[0:self.K]
        self.eVectors = self.eVectors[:,0:self.K]

        #normalise evectors and find weights
        self.eVectors = self.L * self.eVectors 
        self.norms = np.linalg.norm(self.eVectors, axis=0)   
        self.eVectors = self.eVectors / self.norms

        self.Weights = self.eVectors.transpose() * self.L  

        self.eVectors = self.eVectors.transpose()

    def run_training(self,):
        '''
        Runs all of the methods necessary to train the model
        '''
        self.read_images()
        self.subtract_mean_face()
        self.Covariance()
        self.find_k()
        self.find_weights()

    def test_model(self, debug, stats, testpath):
        '''
        Uses the test images provided and runs them against the model to determine its accuracy.

        Parameters:
            debug (boolean): Determines if the debug information is printed to the console
            stats (boolean): Determines if the stats are printed to the console
            testpath (string): Path to the test images
        '''
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
    path = '../../../data/trainingData/'
    testing_path = '../../../data/testingData/'
    model = Trainer(height = 80, width = 70, num_images=320, img_path=path)
    model.run_training()
    #model.test_model(debug=True, stats=True, testpath=testing_path)

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