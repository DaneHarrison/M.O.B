# --------------------------------
# front (server)
#
# front is a server responsible for delegating authenticaation requests to workers
# once a response is recieved, the response is then sent back to the user
# --------------------------------
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import threading, json, requests

HOST = 'localhost'              # The front servers address
PORT = 5000                     # The front servers port
URL = 'http://localhost:4000/'  # URL where the worker(s) can be reached   

app = Flask(__name__)   # Flask server instance
api = Api(app)          # Controls the Flask server API 

# --------------------------------
# delegate_req
# Delegates the work to the workers
#
# Parameters:
# photo: [bytes] the input image we are using for authenticated
# res: The results to our authentication request - the name (string) and photo (bytes) of the closest user
# --------------------------------
def delegate_req(photo, res):
    res.append()
    
class ProcessImg(Resource):
    def post(self,):
        res = requests.post(URL, json = request.json)
        res = res.json()

        return res
    
api.add_resource(ProcessImg, '/')
app.run(host=HOST, port=PORT, debug=True)