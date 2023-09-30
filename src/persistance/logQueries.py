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
    def recordIfNewImage(self, img, connection):
        successful = False
        results = None

        try:
            cur = connection.cursor()
            cur.execute(f'INSERT INTO public.request_history (req_photo) VALUES ({psycopg2.Binary(img)}); COMMIT;')
            cur.close()

            results = True
        except Exception as e:
            print(f'[ERROR]: {e}')

        return results