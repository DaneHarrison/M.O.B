import sqlalchemy as sq
import psycopg2



class LogQueries:
    # --------------------------------
# is_new_photo
# Checks if the current photo has already been used for authentication
#
# Parameters:
# photo: [bytes[][]] the input image (size 70x80) we are using for authentication
#
# Returns:
# A boolean representing if that image has already been used for authentication
# --------------------------------
    def recordIfNewImage(self, img, conn):
        query = f'INSERT INTO public.request_history (req_photo) VALUES ({psycopg2.Binary(img)}); COMMIT;'
        query = query.replace('VALUES (b\'', 'VALUES (\'')
        isNew = self._isNew(img, conn)

        if isNew:
            query = sq.text(query)
            conn.execute(query)

        return isNew

    def _isNew(self, img, conn):
        query = f'SELECT id FROM public.request_history  WHERE req_photo = {psycopg2.Binary(img)};'
        query = query.replace('VALUES (b\'', 'VALUES (\'')
        query = sq.text(query)

        results = conn.execute(query)
        results = results.fetchall()
        isNew = not results

        return isNew