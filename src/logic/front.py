# --------------------------------
# front (server)
#
# front is a server responsible for delegating authenticaation requests to workers
# once a response is recieved, the response is then sent back to the user
# --------------------------------
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import threading, json, requests

HOST = 'localhost'      # The front servers address
PORT = 5000             # The front servers port
URL = 'localhost:4000'  # URL where the worker(s) can be reached   

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
    res.append(requests.get(URL, json = photo))
    
class ProcessImg(Resource):
    def get(self,):
        photo = request.json    # Accesses photo sent in request (MIME type should be JSON)
        res = []                # Used to store the response from the thread we use to process the request

        # start a new thread to handle the request
        thread = threading.Thread(target=delegate_req, args=[photo, res]) 
        thread.start()

        return jsonify(res)  # responds to the user
    
api.add_resource(ProcessImg, '/')
app.run(host=HOST, port=PORT, debug=True)