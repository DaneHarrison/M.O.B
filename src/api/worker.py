# --------------------------------
# worker (server)
#
# Workers are responsible for recieving work from the front facing server.
# Each request should include an image of a face which the worker than attempts to match against the available databases
# Using EigRequest, after these processes are completed, the image is sent as a response
#
# NOTE: all workers should be started from inside the worker directory
# --------------------------------
from flask import Flask, request, jsonify, abort, send_file
from flask_restful import Resource, Api
import sys, json, base64, numpy, requests, os, base64

# os.chdir('../')
sys.path.append(os.getcwd())
from logic.worker.logic import Logic


app = Flask(__name__)  # Flask server instance
api = Api(app)         # Controls the Flask server API

HOST = 'localhost'  # The workers address
PORT = 4000         # The workers port
logic = Logic()


class ProcessImg(Resource):
    def post(self,):
        
        if 'img' not in request.files:
            abort(400, description='img not found')
        else:
            img = request.files['img']
            img_bytes = None
            
            with open('a.jpg', 'rb') as image_file:
                image_bytes = image_file.read()
            
            static = {
                'a': str(base64.b64encode(image_bytes)),
                'b': str(base64.b64encode(image_bytes)),
                'c': str(base64.b64encode(image_bytes))
            }
            
            try :
                results = logic.runEigenFace(img.read()) # this is two results, req.getMeanVectorBytes()
                if results:
                    print('works')
            except Exception as e:
                print(e)

            return jsonify(static)


api.add_resource(ProcessImg, '/')
app.run(host=HOST, port=PORT, debug=True)