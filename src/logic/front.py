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
    
class ProcessImg(Resource):
    def post(self,):
        print(request.get_json())
        print('wow tthis didnt crash\n\n\n\n')
        jsonThing = request.get_json()
        jsonThing = jsonThing['Photo']
        print(jsonThing)
        # Forward the request to a worker, once a response is recieved forward that back to the user
        res = requests.post(URL, json = json.dumps({'Photo': jsonThing}))
        res = res.json()

        return res # Forward the response back to the user
    
api.add_resource(ProcessImg, '/')
app.run(host=HOST, port=PORT, debug=True)