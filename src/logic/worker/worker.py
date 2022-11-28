from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import threading

app = Flask()   # Flask server instance
api = Api(app)  # Controls the Flask server API


class processImg(Resource):
    def get(self,):
        req = Request() # Processes images sent to the worker
        
        thread = threading.Thread(target=req.process)
        thread.start()

        return req.getResults()
    
api.add_resource(processImg, '/')
app.run(host='localhost', port=3500, debug=True)