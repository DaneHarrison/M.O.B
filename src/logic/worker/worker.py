# --------------------------------
# worker (server)
#
# Workers are responsible for recieving work from the front facing server.
# Each request should include a stringified representation of an image and the name of the user
# A worker will then process it using the Request class and return the results
#
# NOTE: all workers should be started from inside the worker directory
# --------------------------------
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from request import Request
import threading, json, base64, numpy

HOST = 'localhost'                              # The workers address
PORT = 4000                                     # The workers port
E_VECTOR_LOCATION = './data/eVectors.json'      # The location of the eVectors file
MEAN_VECTOR_LOCATION = './data/meanVector.json' # The location of the meanVector file

app = Flask(__name__)  # Flask server instance
api = Api(app)         # Controls the Flask server API
e_vectors = None       # Holds the eVectors (size 5600x136) used to determine which face is closest to the input image
mean_vector = None     # Holds the mean vector (size 5600x1) used to determines which face is closest to the input image

# Loads then closes the eVectors and mean vector respectively
with open(E_VECTOR_LOCATION, 'r') as e_vector_file:
  e_vectors = json.load(e_vector_file)
with open(MEAN_VECTOR_LOCATION, 'r') as mean_vector_file:
  mean_vector = json.load(mean_vector_file)

# Adds the image processing route
class ProcessImg(Resource):
    def post(self,):
        req = Request() # Processes images sent to the worker
        
        # Read the raw image bytes from JSON and then start processing the authentication request
        photo = json.loads(request.json)
        photo = photo["Photo"].encode('utf-8')
        photo = base64.decodebytes(photo)
        photo = numpy.fromstring(photo, numpy.uint8)
        req.process(photo, e_vectors, mean_vector)
        results = req.get_results()

        if(results):  # If this is a new picture for the system
            photo_in_base64 = base64.b64encode(results["Photo"])
            photo_as_string = photo_in_base64.decode('utf-8')

            # Prepare matched image to be sent over JSON if this is a valid authentication request
            json_results = json.dumps({"Name": results["Name"],"Photo": photo_as_string}, indent=2)
        else:         # If the sent image has been previously seen we dont want to grant access to the user
          json_results = json.dumps({"Name": None,"Photo": None})

        return json_results  # responds to the front facing servers request
    
api.add_resource(ProcessImg, '/')
app.run(host=HOST, port=PORT, debug=True)