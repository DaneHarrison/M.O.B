from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from training import Trainer
import numpy as np
import json

app = Flask(__name__)
api = Api(app)


class mainPage(Resource):
    def get(self,):
        return {'main':'Main page'}

    def post(self,):
        pass


class meanVector(Resource):
    def get(self,):
        values = json.dumps(my_model.mean_vector.tolist())
        return jsonify({'mean_vector':values, 'rows':'5600', 'columns':'1'})

class get_eVectors(Resource):

    def get(self,):
        
        matrixShape = my_model.eVectors.shape
        rows = matrixShape[0]
        cols = matrixShape[1]

        arr = np.array([[1,2,3],[4,5,6],[7,8,9]])#my_model.eVectors
        arr = arr.tolist()
        arr = json.dumps(arr)
        return jsonify({'evectors':arr, 'rows':rows, 'columns':cols})
        
        
api.add_resource(mainPage, '/')
api.add_resource(meanVector, '/meanvector')
api.add_resource(get_eVectors,'/evectors')


if __name__ == '__main__':

    #train the model
    path = '../../../res/trainingData/'
    my_model = Trainer(height = 80, width = 70, num_images=320, img_path=path)
    my_model.run_training()

    #run the app
    app.run(host='localhost', port=3500, debug=True)
