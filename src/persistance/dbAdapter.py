# --------------------------------
# dbAdapter (class)
#
# Holds instances of all databases a worker requires access to fufill authentication requests:
#   - DBA: holds the first 100 user photos
#   - DBB: holds the second 100 user photos
#   - DBC: holds the remaining user photos
#   - logDB: holds a history of previously submitted photos
# --------------------------------
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


# --------------------------------
# get_DBA
# Getter for reference to face database DBA
#
# Returns:
# A reference to face database DBA
# --------------------------------
    def get_DBA(self):
        return self.DBA

# --------------------------------
# get_DBB
# Getter for reference to face database DBB
#
# Returns:
# A reference to face database DBB
# --------------------------------
    def get_DBB(self):
        return self.DBB

# --------------------------------
# get_DBC
# Getter for reference to face database DBC
#
# Returns:
# A reference to face database DBC
# --------------------------------
    def get_DBC(self):
        return self.DBC

# --------------------------------
# get_logDB
# Getter for reference to log database logDB
#
# Returns:
# A reference to log database logDB
# --------------------------------
    def get_logDB(self):
        return self.logDB