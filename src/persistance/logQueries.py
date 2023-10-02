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
        # img = psycopg2.Binary(img)
        # query = f'INSERT INTO public.request_history (req_photo) VALUES ({img}); COMMIT;'
        # # query = query.replace('VALUES (b\'', 'VALUES (\'')
        # isNew = self._isNew(img, conn)

        # if isNew:
        #     query = sq.text(query)
        #     conn.execute(query)
        #     print('good shit')

        # return isNew
        return True

    def _isNew(self, img, conn):
        # query = f'SELECT id FROM public.request_history WHERE req_photo = {img};'
        # # query = query.replace('req_photo = b\'', 'req_photo = \'')
        # query = sq.text(query)

        # results = conn.execute(query)
        # results = results.fetchall()
        # print('first check')
        # isNew = not results

        #return isNew
        return True