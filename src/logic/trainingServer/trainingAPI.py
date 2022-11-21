from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from training import Trainer

app = Flask(__name__)
api = Api(app)


class mainPage(Resource):
    def get(self,):
        return {'main':'Main page'}

    def post(self,):
        pass


class meanVector(Resource):
    def get(self,):
        values = []
        for num in my_model.mean_vector:
            values.append(float(num))

        return jsonify({'mean_vector':values})



api.add_resource(mainPage, '/')
api.add_resource(meanVector, '/meanvector')


if __name__ == '__main__':

    #train the model
    path = '../../../res/trainingData/'
    my_model = Trainer(height = 80, width = 70, num_images=320, img_path=path, debug=True, stats = True)
    my_model.run_training()

    #run the app
    app.run(host='localhost', port=3500)
