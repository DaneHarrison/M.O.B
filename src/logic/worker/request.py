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
import numpy, sys

sys.path.append('../../persistance')
from dbAdapter import DBAdapter
from dbQueries import DBQueries

class Request:
    def __init__(self):
        self.db_adapter = DBAdapter()   # Holds each database reference
        self.queries = DBQueries()      # Holds the queries we want to perform against the databases
        self.res_DBA = None             # Map results from Database A {ID: int, Distance: float}
        self.res_DBB = None             # Map results from Database B {ID: int, Distance: float}
        self.res_DBC = None             # Map results from Database C {ID: int, Distance: float}
        self.closest = None             # Reduce results from closest user {Name: string, Photo: bytes}


# --------------------------------
# process
# Is responsible for controlling the authentication process thats been delegated to the worker
#
# Parameters:
# photo: [bytes[][]] the input image (size 70x80) we are using for authenticated
# e_vectors: [int[][]] Holds the eVectors (size 5600x136) used to determine which face is closest to the input image
# mean_vector: [int[]] Holds the mean vector (size 5600x1) used to determines which face is closest to the input image
# --------------------------------
    def process(self, photo, e_vectors, mean_vector):
        if(self.is_new_photo(photo)):
            image_vector = self.compute_image_vector(photo, e_vectors, mean_vector) # manipulate our input image

            # Map each database to find the closest match for the input photo
            self.res_DBA = self.queries.mapDB(self.db_adapter.connect_to_DBA(), image_vector)
            self.res_DBB = self.queries.mapDB(self.db_adapter.connect_to_DBB(), image_vector)
            self.res_DBC = self.queries.mapDB(self.db_adapter.connect_to_DBC(), image_vector)
            
            self.queries.add_entry(photo, self.dbAdapter.connect_to_logs()) # Add photo to our log database
            query_details = self.calc_min_query_details()           # Locate the smallest distance and its associated database
            self.closest = self.queries.reduceDB(query_details)     # Query that database for the name and image of the user

            # Close database connections
            self.db_adapter.close_DBA()
            self.db_adapter.close_DBB()
            self.db_adapter.close_DBC()
            self.db_adapter.close_logs()


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
    def compute_image_vector(self, photo, e_vectors, mean_vector):
        img_col = numpy.array(photo, dtype='float64').flatten() # Flatten the input image into a vector
        mean_vector = numpy.reshape(mean_vector, (5600, 1))     # Ensures the vector is registered correctly 
        img_col = numpy.reshape(img_col, (5600, 1))             # Ensures the vector is registered correctly 
        
        img_col -= mean_vector                        # Subtract the mean vector from the input image
        img_col = numpy.reshape(img_col, (5600, 1))   # Reshape the image into a vector  
        processed_image = e_vectors @ img_col         # Multiply eVectors by the image vector to get what we need to compare
        
        # Puts processed_image into a sendable format
        processed_image = processed_image.reshape((1,len(processed_image)))
        processed_image = str(processed_image.tolist())[1:-1]

        return processed_image

# --------------------------------
# calc_min_query_details
# Identifies the smallest distance and maps it to either DBA, DBB or DBC (depending on the index of that distance) 
#
# Returns:
# A dictionary that holds the int (ID) and database reference (DB) according to the smallest distance
# --------------------------------
    def calc_min_query_details(self):
        distances = [self.res_DBA["Distance"], self.res_DBB["Distance"], self.res_DBC["Distance"]]
        min_index = distances.index(min(distances))  

        # Check which index was the smallest, that is the ID and database we want
        if(min_index == 0):      # Choose database A
            query_details = {"ID": self.res_DBA["ID"], "DB": self.db_adapter.connect_to_DBA()}
        elif(min_index == 1):    # Choose database B
            query_details = {"ID": self.res_DBB["ID"], "DB": self.db_adapter.connect_to_DBB()}
        else:                   # Choose database C
            query_details = {"ID": self.res_DBC["ID"], "DB": self.db_adapter.connect_to_DBC()}

        return query_details

# --------------------------------
# get_results
# Fetch the results for the processed request
#
# Returns:
# A dictionary of the results to the authentication request - {Name: string, Photo: bytes} of the closest user
# --------------------------------
    def get_results(self):
        return self.closest

# --------------------------------
# is_new_photo
# Checks if the current photo has already been used for authentication
#
# Parameters:
# photo: [bytes[][]] the input image (size 70x80) we are using for authentication
#
# Returns:
# A boolean representing if that image has already been used for authentication
# --------------------------------
    def is_new_photo(self, photo):
        return len(self.queries.check_for_prev_entry(photo, self.db_adapter.connect_to_logs())) == 0