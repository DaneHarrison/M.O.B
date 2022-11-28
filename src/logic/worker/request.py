from src.persistance.dbAdapter import DBAdapter
from src.persistance.prisma.queries import Queries

class Request:
    def __init__(self):
        self.dbAdapter = DBAdapter()
        self.queries = Queries()
        self.resDBA = null
        self.resDBB = null
        self.resDBC = null
        self.closest = null


    def process(self):
        distances = []
        min = -1

        self.resDBA = self.queries.mapDB(self.dbAdapter.getDBA())
        self.resDBB = self.queries.mapDB(self.dbAdapter.getDBB())
        self.resDBC = self.queries.mapDB(self.dbAdapter.getDBC())

        distances.append(self.resDBA.Distance)
        distances.append(self.resDBB.Distance)
        distances.append(self.resDBC.Distance)
        min = self.findMinDistance(distances)

        # if(distances[min] is within a threshold)
        if(min == 0):
            self.closest = self.queries.reduceDB(self.resDBA.ID, self.dbAdapter.getDBA())
        elif(min == 1):
            self.closest = self.queries.reduceDB(self.resDBB.ID, self.dbAdapter.getDBB())
        else:
            self.closest = self.queries.reduceDB(self.resDBC.ID, self.dbAdapter.getDBC())

    def findMinDistance(self, distances):
        distances = []
        minDistance = min(distances)

        return distances.index(minDistance)

    def getResults(self):
        return self.closest