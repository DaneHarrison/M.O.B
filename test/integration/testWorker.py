import unittest, requests, sys, requests, nose2, json, base64, cv2, numpy, psycopg2, os

sys.path.append('../../src/persistance')

from dbAdapter import DBAdapter
from dotenv import load_dotenv

class Worker(unittest.TestCase):
    def clear_logs(self):
        con = psycopg2.connect(host=os.getenv('HOST'), port=os.getenv('DB_LOG_PORT'), database=os.getenv('DB'), user=os.getenv('USER'),password=os.getenv('PASSWORD'))
        cur = con.cursor()

        cur.execute("BEGIN; TRUNCATE TABLE public.\"Entry\"; COMMIT;")

        cur.close()
        con.close()

    def test_worker_api(self):
        photo = cv2.imread('../../res/testingData/9_1.jpg', 0)
        photo_in_base64 = base64.b64encode(photo)
        photo_as_string = photo_in_base64.decode('utf-8')
        photo_as_json = json.dumps({"Photo": photo_as_string}, indent=2)

        res = requests.post('http://localhost:4000/', json = photo_as_json)
        res = json.loads(res.json())
        self.clear_logs()

        self.assertEqual(res["Name"], 'Milo Wolfe')


if __name__ == '__main__':
    load_dotenv()           # Loads the .env file
    nose2.main()  