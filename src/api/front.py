# --------------------------------
# front (server)
#
# front is a server responsible for delegating authentication requests to workers
# once a response is recieved, the response is then sent back to the user
# --------------------------------
from flask import Flask, request, jsonify, render_template, Response, abort
from flask_restful import Resource, Api
import json, requests, os, io, base64
from werkzeug.utils import secure_filename
from flask_cors import CORS
HOST = 'localhost'              # The front servers address
PORT = 5000                     # The front servers port
URL = 'http://localhost:4000/'  # URL where the worker(s) can be reached   

app = Flask(__name__, template_folder='../presentation/build/', static_folder='../presentation/build/static/')   # Flask server instance
CORS(app)
app.config['UPLOAD_FOLDER'] = './'
api = Api(app)          # Controls the Flask server API 


class ProcessImg(Resource):
    def post(self,):
        recvdPhoto = request.get_json()
        recvdPhoto = recvdPhoto['Photo']

        # Forward the request to a worker, once a response is recieved forward that back to the user
        res = requests.post(URL, json = json.dumps({'Photo': recvdPhoto}))
        res = res.json()

        return res # Forward the response back to the user

class Index(Resource):
    def get(self,):
        return Response(render_template('index.html'), mimetype='text/html')
    
    def post(self,):
        response = None

        try:
            imgData = request.json.get('img')       
            _, encoded_data = imgData.split(',', 1) # Remove meta data
            img = base64.b64decode(encoded_data)    # Converts string to bytes

            files = [
                ('img', ('image.jpg', img, 'image/jpg'))
            ]

            workerResponse = requests.post(URL, files=files)
            workerResponse = workerResponse.json()

            response = {
                'a': workerResponse['a'],
                'b': workerResponse['b'],
                'c': workerResponse['c']
            }

            print(workerResponse['a'])

        except Exception as e:
            print(e)
            abort(400, description=e)

        return jsonify(response)
    

#api.add_resource(ProcessImg, '/')
api.add_resource(Index,'/')
app.run(host=HOST, port=PORT, debug=True)