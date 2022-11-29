from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import threading, json, requests

app = Flask()     # Flask server instance
api = Api(app)    # Controls the Flask server API

URL = None

def delegateReq(photo, res):
    res.append(requests.post(URL, json = photo))

    
class processImg(Resource):
    def get(self,):
        photo = request.json  # Accesses photo sent in request (MIME type should be JSON)
        res = []

        thread = threading.Thread(target=delegateReq, args=[photo, res]) 
        thread.start()

        return jsonify(res)
    
api.add_resource(processImg, '/')
app.run(host='localhost', port=3500, debug=True)