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
import psycopg2

class FaceQueries:
    def mapDB(self, connection, processed_photo):
        """
        Maps the processed input photo to the closest users in that database
        
        Parameters:
        - connection: A connection to the database we would like to query 
        - processed_photo: Holds the processed input image to be used for comparison (size 5600x1)
        
        Returns:
        - Dictionary containing the details of the closest mapped results 
            - {ID: int Distance: float}
        """
        cur = connection.cursor()

        # Perform the query
        cur.execute(f'SELECT find_min(ARRAY{processed_photo})')
        results = cur.fetchall()
        cur.close()

        # Load the data (custom datatype returned from a database script)
        rowID = int(results[0][0][1:-1].split(',')[0])
        distance = float(results[0][0][1:-1].split(',')[1])

        return {'ID': rowID, 'Distance': distance}

    def reduceDB(self, query_details):
        """
        Fetches the name and photo of the closest user once they are determined as such

        Parameters:
        - query_details: A dictionary that holds an ID integer (ID) and database connection (DB) according to the smallest distance
        
        Returns
        - Dictionary of the closest user 
            - {Name: string, Photo: bytes} 
        """
        name = None     # Default value incase the user specified could not be found
        photo = None    # Default value incase the uesr specified could not be found

        # Perform the query
        cur = query_details["DB"].cursor()
        cur.execute(f'SELECT * FROM public.user_faces WHERE id = {query_details["ID"]}')
        results = cur.fetchall()
        cur.close()

        # Load the results (there will only ever be one)
        for result in results:
            name = result[1]
            photo = result[3]

        return {'Name': name, 'Photo': photo}