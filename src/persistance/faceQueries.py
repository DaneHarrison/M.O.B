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
import sqlalchemy as sq

class FaceQueries:
    def mapDB(self, conn, img):
        """
        Maps the processed input photo to the closest users in that database
        
        Parameters:
        - connection: A connection to the database we would like to query 
        - processed_photo: Holds the processed input image to be used for comparison (size 5600x1)
        
        Returns:
        - Dictionary containing the details of the closest mapped results 
            - {ID: int Distance: float}
        """
        img = img.flatten()
        img = img.tolist()
        query = sq.text(f'SELECT find_min(ARRAY{img})')

        # Returns results similar to: [('(48,7444.449291597461)',)]
        results = conn.execute(query)
        results = results.fetchall()

        # Fetches the inner tuple then splits the two values
        results = '' + results[0][0]
        results = results.split(',')

        # Formats both values to integers and floats respectively
        faceID = int(results[0].replace('(', ''))
        dist = float(results[1].replace(')', ''))

        return {'ID': faceID, 'Dist': dist}

    def reduceDB(self, bestMapping):
        """
        Fetches the name and photo of the closest user once they are determined as such

        Parameters:
        - query_details: A dictionary that holds an ID integer (ID) and database connection (DB) according to the smallest distance
        
        Returns
        - Dictionary of the closest user 
            - {Name: string, Photo: bytes} 
        """
        # ID=mapResults['ID'], Dist=mapResults['Dist'], Conn=conn
        reduceResults = None

        query = sq.text(f'SELECT user_name, photo FROM public.user_faces WHERE id = {bestMapping[0]}')
        results = bestMapping.Conn.execute(query)
        results = results.fetchall()
        results = results[0]    # get first row

        if results:
            reduceResults = {}
            reduceResults['Name'] = results[0]
            reduceResults['Photo'] = results[1]

        return reduceResults