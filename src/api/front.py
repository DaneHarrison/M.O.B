# --------------------------------
# front (server)
#
# front is a server responsible for delegating authentication requests to workers
# once a response is recieved, the response is then sent back to the user
# --------------------------------
from flask import Flask, request, jsonify, render_template, Response
from flask_restful import Resource, Api
import threading, json, requests, os, urllib.request
from werkzeug.utils import secure_filename

HOST = 'localhost'              # The front servers address
PORT = 5000                     # The front servers port
URL = 'http://localhost:4000/'  # URL where the worker(s) can be reached   

app = Flask(__name__, template_folder='../presentation/src/templates/')   # Flask server instance
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
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        return Response("Success", mimetype='text/html')
    

#api.add_resource(ProcessImg, '/')
api.add_resource(Index,'/')
app.run(host=HOST, port=PORT, debug=True)