from persistance.adapter import Adapter
import sqlalchemy as sq
import psycopg2


class LogQueries:
    def recordIfNewImage(self, img: bytes, conn: Adapter) -> bool:
        query = f'INSERT INTO public.request_history (req_photo) VALUES ({psycopg2.Binary(img)}); COMMIT;'
        query = query.replace('VALUES (b\'', 'VALUES (\'')
        isNew = self._isNew(img, conn)

        if isNew:
            query = sq.text(query)
            conn.execute(query)

        return isNew

    def _isNew(self, img: bytes, conn: Adapter) -> bool:
        query = f'SELECT id FROM public.request_history WHERE req_photo = {psycopg2.Binary(img)};'
        query = sq.text(query)

        results = conn.execute(query)
        results = results.fetchall()
        isNew = not results

        return isNew