from persistance.adapter import Adapter
from collections import namedtuple
from typing import Dict, Optional
import sqlalchemy as sq
import numpy as np

class FaceQueries:
    def mapDB(self, conn: Adapter, img: np.ndarray[np.float64]) -> Dict[int, float]:
        """
        Maps the input to the closest users in a database
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

    def reduceDB(self, bestMapping: namedtuple) -> Dict[Optional[str], Optional[bytes]]:
        """
        Fetches the name and photo of the closest user once they are determined as such
        """
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