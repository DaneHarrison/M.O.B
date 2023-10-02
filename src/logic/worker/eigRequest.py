# --------------------------------
# EigRequest
#
# EigRequest delegates the Eigenface authentication processes that are used to identify users
# The involves:
#   - Input image processing (in preparation for cv2)           - compute_image_vector()
#   - Mapping the image to the closest user from each database  - map()
#   - Selecting the closest user                                - chooseBest()
#   - Reducing the image query to that single user              - reduce()
#   - Output formatting                                         - formatOutput()
# --------------------------------
from persistance.faceQueries import FaceQueries
from typing import List, Optional
from collections import namedtuple
import sqlalchemy as sq
import numpy as np

import json, sys, cv2


class EigRequest:
    MapResult = namedtuple('MapResult', ['ID', 'Dist', 'Conn'])
    ReduceResult = namedtuple('ReduceResult', ['Photo'])

    E_VECTOR_LOCATION = './data/eVectors.json'      # The location of the eVectors file
    MEAN_VECTOR_LOCATION = './data/meanVector.json' # The location of the meanVector file
    NUM_PIXELS = 5600   # The expected number of total pixels
    IMG_WIDTH = 70      # The expected width
    IMG_HEIGHT = 80     # The expected height


    def __init__(self):
        self.e_vectors = json.load(open(EigRequest.E_VECTOR_LOCATION, 'r'))
        self.mean_vector = json.load(open(EigRequest.MEAN_VECTOR_LOCATION, 'r'))

        self.mean_vector_bytes = np.array(self.mean_vector)
        self.mean_vector_bytes = np.reshape(img, (80, 70))
        self.mean_vector_bytes = self.prepareOutput(self.mean_vector_bytes)


    def getMeanVectorBytes(self) -> Optional[bytes]:
        return self.mean_vector_bytes

    def prepareInput(self, img: bytes) -> np.array:
        img = np.frombuffer(img, np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (EigRequest.IMG_WIDTH, EigRequest.IMG_HEIGHT))

        return img
    
    def compute_image_vector(self, img: np.array) -> np.array:
        img_col = np.array(img, dtype='float64').flatten()                      # Flatten the input image into a vector
        mean_vector = np.reshape(self.mean_vector, (EigRequest.NUM_PIXELS, 1))  # Ensures the vector is registered correctly 
        img_col = np.reshape(img_col, (EigRequest.NUM_PIXELS, 1))               # Ensures the image is registered correctly
        
        img_col -= mean_vector                      # Subtract the mean vector from the input image
        processed_image = self.e_vectors @ img_col  # Multiply eVectors by the image vector to get what we need to compare

        return processed_image        

    def mapDB(self, faceConns: List[sq.engine.Connection], querier: FaceQueries) -> List[namedtuple]:
        results = []

        for conn in faceConns:
            mapResults = querier.mapDB(conn, self.image_vector)
            mapResults = EigRequest.MapResult(ID=mapResults['ID'], Dist=mapResults['Dist'], Conn=conn)
            results.append(mapResults)

        return results

    def reduceDB(self, bestMapping: namedtuple) -> Optional[namedtuple]:
        reduceResults = self.queries.reduceDB(bestMapping)
        reduceResults = EigRequest.ReduceResults(Photo=reduceResults['Photo'])

        return reduceResults

    def chooseBest(self) -> Optional[namedtuple]: 
        return min(mappings, key=lambda x: x['Distance'], default=None)

    def prepareOutput(self, img: np.array) -> Optional[bytes]:
        successful, img = cv2.imencode('.jpg', img)
        results = None

        if successful:
            results = img.tobytes()

        return results