# --------------------------------
# front (server)
#
# front is a server responsible for delegating authentication requests to workers
# once a response is recieved, the response is then sent back to the user
# --------------------------------
from flask import Flask, request, jsonify, render_template, Response
from flask_restful import Resource, Api
import json, requests, os, io
from werkzeug.utils import secure_filename

HOST = 'localhost'              # The front servers address
PORT = 5000                     # The front servers port
URL = 'http://localhost:4000/'  # URL where the worker(s) can be reached   

app = Flask(__name__, template_folder='../presentation/build/', static_folder='../presentation/build/static/')   # Flask server instance
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
        if 'file' not in request.files:
            return jsonify({'error': 'No file, kinda cringe'})
        
        file = request.files['file']
        if file.filename == "":
            return jsonify({'error':'No image selected, kinda weird'})
        
        if file:
            url = 'http://localhost:4000/'
            file_contents = file.read()
            file_like_object = io.BytesIO(file_contents)

            files = [
                ('file', ('image.jpg', file_like_object, 'image/jpg'))
            ]

            response = requests.post(url, files=files)
            print(response.text)
        # if file:
        #     url = 'http://localhost:4000/'
        #     files = [
        #         ('file', (file, 'image/jpg'))
        #     ]

        #     response = requests.request("POST", url, files=files)
        #     print(response.text)
        
    

#api.add_resource(ProcessImg, '/')
api.add_resource(Index,'/')
app.run(host=HOST, port=PORT, debug=True)