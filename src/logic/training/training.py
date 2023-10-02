import numpy as np
import os
import cv2
import json
import re

class Trainer:

    """
        A class for training a facial recognition model using principle component analysis.
    """
    
    def __init__(self, height, width, num_images, img_path):
        """
        Initializes the Trainer object with specified parameters.

        Parameters:
            height (int): Height of the images.
            width (int): Width of the images.
            num_images (int): Number of training images.
            img_path (str): Path to the directory containing training images.
        """
        self.height = height
        self.width = width
        self.num_images = num_images
        self.img_path = img_path
        self.L = np.empty(shape=(self.height * self.width, num_images))
        self.LTL = []
        self.eValues = []
        self.eVectors = []
        self.K = 0
        self.norms = []
        self.Weights = []
        self.training_names = self._sorted_alphanumeric(os.listdir(self.img_path))
        self.mean_vector = []

    def _sorted_alphanumeric(self, data):
        """
        Sorts a list of strings alphanumerically.

        Parameters:
            data (list): List of strings to be sorted.

        Returns:
            list: Sorted list of strings.
        """
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(data, key=alphanum_key)

    def _read_image(self, name):
        """
        Reads and flattens an image from the specified file path.

        Parameters:
            name (str): File name of the image.

        Returns:
            numpy.ndarray: Flattened image data as a 1D numpy array.
        """
        try:
            image = cv2.imread(os.path.join(self.img_path, name), 0)
            return np.array(image, dtype='float64').flatten()[:]
        except Exception as e:
            print(f"Error while reading training image '{name}': {e}")
            return None
        
    def read_images(self):
        """
        Reads all training images, flattens them, and stores in self.L.
        """
        for index, name in enumerate(self.training_names):
            img_data = self._read_image(name)
            if img_data is not None:
                self.L[:, index] = img_data

    def subtract_mean_face(self):
        """
        Subtracts the mean face from all training images.
        """
        self.mean_vector = np.sum(self.L, axis=1) / self.num_images
        for i in range(self.num_images):
            self.L[:,i] -= self.mean_vector[:]

    def Covariance(self):
        """
        Calculates the covariance matrix of the training images.
        """
        self.LTL = np.matrix(self.L.transpose()) * np.matrix(self.L)  
        self.LTL /= self.num_images
        self.eValues, self.eVectors = np.linalg.eig(self.LTL)

    def find_k(self):
        """
        Determines the number of principal components (K) to retain.
        """
        sort_indices = self.eValues.argsort()[::-1]
        self.eValues = self.eValues[sort_indices]
        self.eVectors = self.eVectors[sort_indices]

        self.K = 0
        curr_sum = 0
        total_sum = np.sum(self.eValues)
        for v in self.eValues:
            curr_sum += v

            if curr_sum / total_sum > 0.95:
                break
            else:
                self.K += 1

    def find_weights(self):
        """
        Calculates the weights for the training images.
        """
        self.eValues = self.eValues[0:self.K]
        self.eVectors = self.eVectors[:, 0:self.K]
        self.eVectors = self.L * self.eVectors
        self.norms = np.linalg.norm(self.eVectors, axis=0)
        self.eVectors /= self.norms
        self.Weights = self.eVectors.transpose() * self.L  
        self.eVectors = self.eVectors.transpose()

    def run_training(self):
        """
        Runs the training process, including reading images, subtracting mean face,
        calculating covariance, determining K, and finding weights.
        """
        self.read_images()
        self.subtract_mean_face()
        self.Covariance()
        self.find_k()
        self.find_weights()

if __name__ == '__main__':
    path = '../../../data/trainingData/'
    testing_path = '../../../data/testingData/'
    model = Trainer(height=80, width=70, num_images=320, img_path=path)
    model.run_training()

    weightsPath = '../../persistance/seed/'
    dataPath = '../../logic/worker/data/'

    with open(os.path.join(weightsPath, 'weights.json'), 'w') as f:
        json.dump(model.Weights.transpose().tolist(), f)

    with open(os.path.join(dataPath, 'eVectors.json'), 'w') as f:
        json.dump(model.eVectors.tolist(), f)

    with open(os.path.join(dataPath, 'meanVector.json'), 'w') as f:
        json.dump(model.mean_vector.tolist(), f)