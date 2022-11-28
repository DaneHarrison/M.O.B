from src.persistance.dbAdapter import DBAdapter
from src.persistance.prisma.queries import Queries

class Request:
    def __init__(self):
        self.dbAdapter = DBAdapter()    # Holds each database reference
        self.queries = Queries()        # Holds the queries we want to perform against the databases
        self.resDBA = null              # Map results from Database A (ID, Distance)
        self.resDBB = null              # Map results from Database B (ID, Distance)
        self.resDBC = null              # Map results from Database C (ID, Distance)
        self.closest = null             # Reduce results from closest user (Name, Photo)


    def process(self):
        distances = []  # Holds distances from our database mappings
        min = -1        # the index of the smallest distance from distances

        # Map each database
        self.resDBA = self.queries.mapDB(self.dbAdapter.getDBA())
        self.resDBB = self.queries.mapDB(self.dbAdapter.getDBB())
        self.resDBC = self.queries.mapDB(self.dbAdapter.getDBC())

        # Put each distance into the distance list order: A, B, C
        distances.append(self.resDBA.Distance)
        distances.append(self.resDBB.Distance)
        distances.append(self.resDBC.Distance)
        min = self.findMinDistance(distances)

        # Find the closest user based on the smallest from the smallest distance
        # if(distances[min] is within a threshold)
        if(min == 0):
            self.closest = self.queries.reduceDB(self.resDBA.ID, self.dbAdapter.getDBA())
        elif(min == 1):
            self.closest = self.queries.reduceDB(self.resDBB.ID, self.dbAdapter.getDBB())
        else:
            self.closest = self.queries.reduceDB(self.resDBC.ID, self.dbAdapter.getDBC())

    def findMinDistance(self, distances):
        minDistance = min(distances)

        return distances.index(minDistance)

    def getResults(self):
        return self.closest