from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import threading

app = Flask(__name__)
handler = Handler()
api = Api(app)

class processImg(Resource):
    def get(self,):
        req = Request()
        
        thread = threading.Thread(target=req.process)
        thread.start()

        return req.getResults()
    
api.add_resource(processImg, '/')
app.run(host='localhost', port=3500, debug=True)
