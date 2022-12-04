# --------------------------------
# dbAdapter (class)
#
# Connects a worker to all databases a worker requires access to fufill authentication requests
#   - DBA: holds users [0, 13]
#   - DBB: holds users [14, 26]
#   - DBC: holds the remaining users [27, 40)
#   - logDB: holds a history of previously submitted photos
#
# NOTE: A new connection can only be grabbed if the previous connection to that database was closed
# --------------------------------
from dotenv import load_dotenv
import psycopg2, os

class DBAdapter:
    def __init__(self):
        load_dotenv()       # Loads the .env file
        self.DBA = None     # Holds a connection for Face Database DBA
        self.DBB = None     # Holds a connection for Face Database DBB
        self.DBC = None     # Holds a connection for Face Database DBC
        self.logs = None    # Holds a connection for Log Database logs


# --------------------------------
# connect_to_DBA
# Connects to database A unless there is already an ongoing connection, in which case, that connection is provided
#
# Returns:
# A connection to face database DBA
# --------------------------------
    def connect_to_DBA(self):
        if(not self.DBA):
            self.DBA = psycopg2.connect(host='http://postgres-a-service', port=5432, database='MOB', user='user', password='password')
        
        return self.DBA

# --------------------------------
# connect_to_DBB
# Connects to database B unless there is already an ongoing connection, in which case, that connection is provided
#
# Returns:
# A connection to face database DBB
# --------------------------------
    def connect_to_DBB(self):
        if(not self.DBB):
            self.DBB = psycopg2.connect(host='http://postgres-b-service', port=5433, database='MOB', user='user', password='password')
        
        return self.DBB

# --------------------------------
# connect_to_DBC
# Connects to database C unless there is already an ongoing connection, in which case, that connection is provided
#
# Returns:
# A connection to face database DBC
# --------------------------------
    def connect_to_DBC(self):
        if(not self.DBC):
            self.DBC = psycopg2.connect(host='http://postgres-c-service', port=5434, database='MOB', user='user', password='password')
        
        return self.DBC

# --------------------------------
# connect_to_logs
# Connects to the log database unless there is already an ongoing connection, in which case, that connection is provided
#
# Returns:
# A connection to log database
# --------------------------------
    def connect_to_logs(self):
        if(not self.logs):
            self.logs = psycopg2.connect(host='http://logs-service', port=5435, database='MOB', user='user', password='password')
        
        return self.logs

# --------------------------------
# close_DBA
# Closes the connection to face database DBA if one currently exists
# --------------------------------
    def close_DBA(self):
        if(self.DBA):
            self.DBA.close()
        
        self.DBA = None

# --------------------------------
# close_DBB
# Closes the connection to face database DBB if one currently exists
# --------------------------------
    def close_DBB(self):
        if(self.DBB):
            self.DBB.close()
        
        self.DBB = None

# --------------------------------
# close_DBC
# Closes the connection to face database DBC if one currently exists
# --------------------------------
    def close_DBC(self):
        if(self.DBC):
            self.DBC.close()
        
        self.DBC = None

# --------------------------------
# close_logs
# Closes the connection to the log database if one currently exists
# --------------------------------
    def close_logs(self):
        if(self.logs):
            self.logs.close()
        
        self.logs = None