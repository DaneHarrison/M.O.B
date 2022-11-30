# --------------------------------
# queries (class)
#
# Queries hold different requests we'd wouldlike to make to various database
#   - Face databases [DBA, DBB, DBC]:
#       - These databases use the mapDB and reduceDB queries
#
#   - Log database [logDB]:
#       - This database uses the check_for_prev_entry and add_entry queries
# --------------------------------
class Queries:
# --------------------------------
# mapDB
# Maps the processed input photo to the closest users
#
# Parameters:
# db: A reference of the database we would like to query 
# processed_photo: Holds the processed input image to be used for comparison of size 5600x1
#
# Returns:
# A tuple of the mapped results (ID, Distance)
# --------------------------------
    def mapDB(self, db, processed_photo) -> None: # here we need the index [ID] and a distance [Distance]
        db.connect()
    #     db.query_first( # this 
    # 'SELECT name, email FROM User WHERE id = ?',
    # 'abc',
    # model=UserInLogin,
    #     'creaTE EXTENSION plpython3u;' # I think this needs to go into the DB script
    #     # ...

        db.disconnect()

# --------------------------------
# reduceDB
# Fetches the name and photo of the closest user once they are determined as such
#
# Parameters:
# query_details: A tuple that holds the ID (int) and database reference according to the smallest distance
#
# Returns
# A tuple of the closest user (Name, Photo)
# --------------------------------
    def reduceDB(self, query_details) -> None:
        db.connect()
        
        # ...

        db.disconnect()

# --------------------------------
# check_for_prev_entry
# Checks if a photo has previously been submitted for authentication
#
# Parameters:
# photo: [bytes] the input image we are using for authenticated
# database: Holds a reference to the database we would like to use for the query
#
# Returns:
# The results of the query: None if its a new request or the ID (int) and photo (bytes) if it was already used 
# --------------------------------
    def check_for_prev_entry(photo, database) -> None:
        database.connect()
        found = database.entry.find_unique( where = {'Photo': photo}) # Checks if this photo is already saved in our log database
        database.disconnect()

        return found

# --------------------------------
# add_entry
# Adds an image to logs to maintain a history of recieving it
#
# Parameters:
# photo: [bytes] the input image we would like to add to logs
# database: Holds a reference to the database we would like to use for the query
# --------------------------------
    def add_entry(photo, database) -> None:
        database.connect()
        database.entry.create( data = {'Photo': photo})
        database.disconnect()