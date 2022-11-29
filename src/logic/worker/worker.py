from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from vectorHolder import VectorHolder
import threading, json

app = Flask()     # Flask server instance
api = Api(app)    # Controls the Flask server API
eVectors = None   #
meanVector = None # 

with open('src/logic/worker/data/eVectors.json', 'r') as eVectorFile:
  eVectors = json.load(eVectorFile)
with open('src/logic/worker/data/meanVector.json', 'r') as meanVectorFile:
  meanVector = json.load(meanVectorFile)


class processImg(Resource):
    def get(self,):
        req = Request() # Processes images sent to the worker
        
        thread = threading.Thread(target=req.process, args=[photo, eVector, meanVector]) 
        thread.start()

        return req.getResults()
    
api.add_resource(processImg, '/')
app.run(host='localhost', port=3500, debug=True)