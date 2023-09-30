# --------------------------------
# request (class)
#
# A request processes authentication requests delegated to a worker from the front facing server
# This process involves:
#   - Verifying that this particular image has not been recieved before with a log database (to prevent replay attacks)
#   - Input image processing
#   - Maping the processed image to the closest user from each database
#   - Selecting the overall closest user
#   - Reduces the query to that single user
#   - Saves the results
# --------------------------------
import sqlalchemy as sq
import numpy, json, sys
from typing import Dict, List
from src.persistance.faceQueries import FaceQueries




# --------------------------------
# process
# Is responsible for controlling the authentication process thats been delegated to the worker
#
# Parameters:
# photo: [bytes[][]] the input image (size 70x80) we are using for authenticated
# e_vectors: [int[][]] Holds the eVectors (size 5600x136) used to determine which face is closest to the input image
# mean_vector: [int[]] Holds the mean vector (size 5600x1) used to determines which face is closest to the input image
# --------------------------------


        # self.img_vector = None
        # self.mappedResults = []
        # self.res_DBA = None             # Map results from Database A 
        # self.res_DBB = None             # Map results from Database B {ID: int, Distance: float}
        # self.res_DBC = None             # Map results from Database C {ID: int, Distance: float}
        # self.closest = None             # Reduce results from closest user {Photo: bytes}

class EigRequest:
    MapResult = namedtuple('MapResult', ['ID', 'Dist', 'Conn'])
    ReduceResult = namedtuple('ReduceResult', ['Photo'])

    E_VECTOR_LOCATION = './data/eVectors.json'      # The location of the eVectors file
    MEAN_VECTOR_LOCATION = './data/meanVector.json' # The location of the meanVector file


    def __init__(self):
        self.e_vectors = json.load(open(Request.MEAN_VECTOR_LOCATION, 'r'))
        self.mean_vector = json.load(open(Request.MEAN_VECTOR_LOCATION, 'r'))


# --------------------------------
# compute_image_vector
# Manipulates the input image so that we can effectively compare it against our users
#
# Parameters:
# photo: [bytes[][]] the input image (size 70x80) we are using for authenticated
# e_vectors: [int[][]] Holds the eVectors (size 5600x136) used to determine which face is closest to the input image
# mean_vector: [int[]] Holds the mean vector (size 5600x1) used to determines which face is closest to the input image
#
# Returns:
# a stringified vector of size 5600x1 representing the processed input image to be used for comparison
# --------------------------------
    def prepareInput(self, img: List[List[bytes]]):
        print()
    
    def compute_image_vector(self, img: List[List[bytes]]):
        img_col = numpy.array(img, dtype='float64').flatten() # Flatten the input image into a vector
        mean_vector = numpy.reshape(self.mean_vector, (5600, 1))     # Ensures the vector is registered correctly 
        img_col = numpy.reshape(img_col, (5600, 1))             # Ensures the vector is registered correctly 
        
        img_col -= mean_vector                        # Subtract the mean vector from the input image
        img_col = numpy.reshape(img_col, (5600, 1))   # Reshape the image into a vector  
        processed_image = self.e_vectors @ img_col    # Multiply eVectors by the image vector to get what we need to compare
        
        # Puts processed_image into a sendable format?
        processed_image = processed_image.reshape((1,len(processed_image)))
        processed_image = str(processed_image.tolist())[1:-1]

        return processed_image


    def process(self, photo, e_vectors, mean_vector):
        if(self.is_new_photo(photo)):
            image_vector = self.compute_image_vector(photo, e_vectors, mean_vector) # manipulate our input image

            # Map each database to find the closest match for the input photo
            self.res_DBA = self.queries.mapDB(self.db_adapter.connect_to_DBA(), image_vector)
            self.res_DBB = self.queries.mapDB(self.db_adapter.connect_to_DBB(), image_vector)
            self.res_DBC = self.queries.mapDB(self.db_adapter.connect_to_DBC(), image_vector)
            
            self.queries.add_entry(photo, self.db_adapter.connect_to_logs()) # Add photo to our log database
            
            

    def mapDB(self, faceConns: List[sq.engine.Connection], querier: FaceQueries) -> List[EigRequest.MapResult]:
        results = []

        for conn in faceConns:
            mapResults = querier.mapDB(conn, self.image_vector)
            mapResults = EigRequest.MapResult(ID=mapResults['ID'], Dist=mapResults['Dist'], Conn=conn)
            results.append(mapResults)

        return results

    def reduceDB(self, bestMapping: EigRequest.MapResult):
        reduceResults = self.queries.reduceDB(bestMapping)
        reduceResults = EigRequest.ReduceResults(Photo=reduceResults['Photo'])

        return reduceResults

# --------------------------------
# calc_min_query_details
# Identifies the smallest distance and maps it to either DBA, DBB or DBC (depending on the index of that distance) 
#
# Returns:
# A dictionary that holds the int (ID) and database reference (DB) according to the smallest distance
# --------------------------------
    def calc_min_query_details(self): 
        """
        # Locate the smallest distance and its associated database
        
        min is used to find the minimum mapping based on the 'Distance' key in each mapping dictionary. 
        The key parameter specifies the function to extract the value on which to perform the comparison, 
        and default=None ensures that if mappings is an empty list, it returns None 
        """
        return min(mappings, key=lambda x: x['Distance'], default=None)

    def prepareOutput(self, img):
        print()