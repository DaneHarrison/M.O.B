from dotenv import load_dotenv
from logs.DB import Prisma as logDB
from faces.DB import Prisma as faceDB
import os

class DBAdapter:
    def __init__(self):
        load_dotenv()           # Loads the .env file
        self.DBA = faceDB()     # Creates an instance of Database A (default)
        self.logDB = logDB()    # Creates an instance of Log Database

        # Replaces default Database URL to B and C respectively
        self.DBB = faceDB( datasource = {'url': os.getenv('DB_B_URL')})     # Creates an instance of Database B
        self.DBC = faceDB( datasource = {'url': os.getenv('DB_C_URL')})     # Creates an instance of Database C


    def getDBA(self):
        return self.DBA

    def getDBB(self):
        return self.DBB

    def getDBC(self):
        return self.DBC

    def getLogDB(self):
        return self.logDB