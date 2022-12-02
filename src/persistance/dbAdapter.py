# --------------------------------
# dbAdapter (class)
#
# Connects a worker to all databases a worker requires access to fufill authentication requests
#   - DBA: holds users [0, 13]
#   - DBB: holds users [14, 26]
#   - DBC: holds the remaining users [27, 40)
#   - logDB: holds a history of previously submitted photos
#
# NOTE: A connection can only be grabbed if the previous connection to that database was closed
# --------------------------------
from dotenv import load_dotenv
import psycopg2, os

class DBAdapter:
    def __init__(self):
        load_dotenv()           # Loads the .env file
        self.DBA = None         # Holds a connection for Face Database DBA
        self.DBB = None         # Holds a connection for Face Database DBB
        self.DBC = None         # Holds a connection for Face Database DBC
        self.logs = None        # Holds a connection for Log Database logs


# --------------------------------
# get_DBA
# Getter for reference to face database DBA
#
# Returns:
# A reference to face database DBA
# --------------------------------
    def connect_to_DBA(self):
        if(not self.DBA):
            self.DBA = psycopg2.connect(host=os.getenv('HOST'), port=os.getenv('DB_A_PORT'), database=os.getenv('DB'), user=os.getenv('USER'),password=os.getenv('PASSWORD'))
        
        return self.DBA

# --------------------------------
# get_DBB
# Getter for reference to face database DBB
#
# Returns:
# A reference to face database DBB
# --------------------------------
    def connect_to_DBB(self):
        if(not self.DBB):
            self.DBB = psycopg2.connect(host=os.getenv('HOST'), port=os.getenv('DB_B_PORT'), database=os.getenv('DB'), user=os.getenv('USER'),password=os.getenv('PASSWORD'))
        
        return self.DBB

# --------------------------------
# get_DBC
# Getter for reference to face database DBC
#
# Returns:
# A reference to face database DBC
# --------------------------------
    def connect_to_DBC(self):
        if(not self.DBC):
            self.DBC = psycopg2.connect(host=os.getenv('HOST'), port=os.getenv('DB_C_PORT'), database=os.getenv('DB'), user=os.getenv('USER'),password=os.getenv('PASSWORD'))
        
        return self.DBC

# --------------------------------
# get_logDB
# Getter for reference to log database logDB
#
# Returns:
# A reference to log database logDB
# --------------------------------
    def connect_to_logs(self):
        if(not self.logs):
            self.logs = psycopg2.connect(host=os.getenv('HOST'), port=os.getenv('DB_LOG_PORT'), database=os.getenv('DB'), user=os.getenv('USER'),password=os.getenv('PASSWORD'))
        
        return self.logs

    def close_DBA(self):
        if(self.DBA):
            self.DBA.close()
        
        self.DBA = None

    def close_DBB(self):
        if(self.DBB):
            self.DBB.close()
        
        self.DBB = None

    def close_DBC(self):
        if(self.DBC):
            self.DBC.close()
        
        self.DBC = None

    def close_logs(self):
        if(self.logs):
            self.logs.close()
        
        self.logs = None