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
import sys, json, base64, numpy, requests, os

os.chdir('../')
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
            results = logic.runEigenFace(img.read())
            # compress data recieved in results into zip file (closest face and mean face)
            send_file()


api.add_resource(ProcessImg, '/')
app.run(host=HOST, port=PORT, debug=True)