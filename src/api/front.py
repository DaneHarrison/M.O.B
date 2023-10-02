# --------------------------------
# front (server)
#
# front is a server responsible for delegating authentication requests to workers
# once a response is recieved, the response is then sent back to the user
# --------------------------------
from flask import Flask, request, jsonify, render_template, Response, abort
from flask_restful import Resource, Api
import json, requests, base64

HOST = 'localhost'              # The front servers address
PORT = 5000                     # The front servers port
URL = 'http://localhost:4000/'  # URL where the worker(s) can be reached   

# Setups up the Flask server
app = Flask(__name__, template_folder='../presentation/build/', static_folder='../presentation/build/static/')
app.config['UPLOAD_FOLDER'] = './'
api = Api(app)

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
                'name': workerResponse['name'],
                'photo': workerResponse['photo'],
                'meanFace': workerResponse['meanFace']
            }

        except Exception as e:
            print(e)
            abort(400, description=e)

        return jsonify(response)
    

api.add_resource(Index,'/')
app.run(host=HOST, port=PORT, debug=True)