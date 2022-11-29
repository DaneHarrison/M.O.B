from src.persistance.dbAdapter import DBAdapter
from src.persistance.queries import Queries
import numpy, json 

class Request:
    def __init__(self):
        self.dbAdapter = DBAdapter()    # Holds each database reference
        self.queries = Queries()        # Holds the queries we want to perform against the databases
        self.resDBA = null              # Map results from Database A (ID, Distance)
        self.resDBB = null              # Map results from Database B (ID, Distance)
        self.resDBC = null              # Map results from Database C (ID, Distance)
        self.closest = null             # Reduce results from closest user (Name, Photo)


    def process(self, photo, eVector, meanVector):
        if(self.isNewPhoto(photo)):
            imageVector = self.computeImageVector(photo, eVector, meanVector) # manipulate our input image

            # Map each database to find the closest match for the input photo
            self.resDBA = self.queries.mapDB(self.dbAdapter.getDBA())
            self.resDBB = self.queries.mapDB(self.dbAdapter.getDBB())
            self.resDBC = self.queries.mapDB(self.dbAdapter.getDBC())
            
            self.queries.addEntry(photo, self.dbAdapter.getLogDB()) # Add photo to our log database
            queryDetails = self.calcMinQueryDetails(minDist)        # Locate the smallest distance and its associated database
            self.closest = self.queries.reduceDB(queryDetails)      # Query that database for the name and image of the user

    def computeImageVector(self, photo, eVector, meanVector):
        img_col = numpy.array(img, dtype='float64').flatten()           # Flatten the input image
        img_col -= meanVector                                           # Subtract the mean vector from the input image
        img_col = numpy.reshape(img_col, (self.width*self.height, 1))   # Reshape the image into a vector  

        return eVector * img_col    # Multiply eVectors against the image vector

    def calcMinQueryDetails(self):
        distances = [self.resDBA.Distance, self.resDBB.Distance, self.resDBC.Distance]
        minIndex = distances.index(min(distances))  

        # Check which index was the smallest, that is the ID and database we want
        if(minIndex == 0):
            queryDetails = (self.resDBA.ID, self.dbAdapter.getDBA())
        elif(minIndex == 1):
            queryDetails = (self.resDBB.ID, self.dbAdapter.getDBB())
        else:
            queryDetails = (self.resDBC.ID, self.dbAdapter.getDBC())

        return queryDetails

    def getResults(self):
        return self.closest

    def isNewPhoto(self, photo):
        return self.queries.checkForPrevEntry(photo, self.dbAdapter.getLogDB()) == None
