from dotenv import load_dotenv
from prisma.DB import Prisma
import os

class DBAdapter:
    def __init__(self):
        load_dotenv()       # Loads the .env file
        self.DBA = Prisma() # Stored instance of Database A (default URL)

        # Replaces default Database URL's from A to B and C respectively
        self.DBB = Prisma( datasource = {'url': os.getenv('DB_B_URL')}) # Stored instance of Database B
        self.DBC = Prisma( datasource = {'url': os.getenv('DB_C_URL')}) # Stored isntance of Database C

    def getDBA(self):
        return self.DBA

    def getDBB(self):
        return self.DBB

    def getDBC(self):
        return self.DBC