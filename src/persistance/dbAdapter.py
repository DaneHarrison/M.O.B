from dotenv import load_dotenv
from prisma.DB import Prisma
import os

class DBAdapter:
    def __init__(self):
        load_dotenv()
        self.DBA = Prisma()
        self.DBB = Prisma( datasource = {'url': os.getenv('DB_B_URL')})
        self.DBC = Prisma( datasource = {'url': os.getenv('DB_C_URL')})

    def getDBA(self):
        return self.DBA

    def getDBB(self):
        return self.DBB

    def getDBC(self):
        return self.DBC