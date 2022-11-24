import requests
import numpy as np

#make a get request to the api
result = requests.get('http://localhost:3500/meanvector')

#JSON
data = result.json()

#Determine what shape the matrix is supposed to be
myshape = data['shape'].split(',')
rows = int(myshape[0])
cols = int(myshape[1])

#read all the values of the matrix, convert them to float and store them in a list
myValues = [[int(x) for x in data['mean_vector']]]

#recreate the matirx with the proper shape
myMatrix = np.array(myValues).reshape((rows,cols))

print(myMatrix.shape)