import unittest, psycopg2, nose2, sys, os, cv2, json
import numpy as np

sys.path.append('../../src/persistance')

from dotenv import load_dotenv
from dbAdapter import DBAdapter
from dbQueries import DBQueries

class Queries(unittest.TestCase):
    def test_map_reduce(self):
        adapter = DBAdapter()
        queries = DBQueries()

        first_image = '../../res/testingData/49_5.jpg'
        second_image = '../../res/testingData/109_11.jpg'
        third_image = '../../res/testingData/19_2.jpg'

        with open('../../src/logic/worker/data/eVectors.json', 'r') as e_vector_file:
            e_vectors = json.load(e_vector_file)
        with open('../../src/logic/worker/data/meanVector.json', 'r') as mean_vector_file:
            mean_vector = json.load(mean_vector_file) 

        img = cv2.imread(first_image, 0)
        img_col = np.array(img, dtype='float64').flatten()
        img_col -= mean_vector 
        img_col = np.reshape(img_col, (70*80, 1))
        processed_photo = e_vectors @ img_col 
        processed_photo = processed_photo.reshape((1,len(processed_photo)))
        processed_photo = str(processed_photo.tolist())[1:-1]

        resultsA = queries.mapDB(adapter.connect_to_DBA(), processed_photo)
        resultsB = queries.mapDB(adapter.connect_to_DBB(), processed_photo)
        resultsC = queries.mapDB(adapter.connect_to_DBC(), processed_photo)

        self.assertEqual(resultsA["ID"], '39')
        self.assertEqual(resultsA["Distance"], '1194.6788829612085')

        self.assertEqual(resultsB["ID"], '36')
        self.assertEqual(resultsB["Distance"], '4236.122116229758')

        self.assertEqual(resultsC["ID"], '108')
        self.assertEqual(resultsC["Distance"], '3163.126918052494')

        # now reduce db 2

        img = cv2.imread(second_image, 0)
        img_col = np.array(img, dtype='float64').flatten()
        img_col -= mean_vector 
        img_col = np.reshape(img_col, (70*80, 1)) 
        processed_photo = e_vectors @ img_col 
        processed_photo = processed_photo.reshape((1,len(processed_photo)))
        processed_photo = str(processed_photo.tolist())[1:-1]

        resultsA = queries.mapDB(adapter.connect_to_DBA(), processed_photo)
        resultsB = queries.mapDB(adapter.connect_to_DBB(), processed_photo)
        resultsC = queries.mapDB(adapter.connect_to_DBC(), processed_photo)

        self.assertEqual(resultsA["ID"], '82')
        self.assertEqual(resultsA["Distance"], '3128.435564785918')

        self.assertEqual(resultsB["ID"], '10')
        self.assertEqual(resultsB["Distance"], '5364.219668292008')

        self.assertEqual(resultsC["ID"], '7')
        self.assertEqual(resultsC["Distance"], '4533.552196276505')

        # now reduce db1

        img = cv2.imread(third_image, 0)
        img_col = np.array(img, dtype='float64').flatten()
        img_col -= mean_vector 
        img_col = np.reshape(img_col, (70*80, 1))  
        processed_photo = e_vectors @ img_col 
        processed_photo = processed_photo.reshape((1,len(processed_photo)))
        processed_photo = str(processed_photo.tolist())[1:-1]       

        resultsA = queries.mapDB(adapter.connect_to_DBA(), processed_photo)
        resultsB = queries.mapDB(adapter.connect_to_DBB(), processed_photo)
        resultsC = queries.mapDB(adapter.connect_to_DBC(), processed_photo)

        self.assertEqual(resultsA["ID"], '11')
        self.assertEqual(resultsA["Distance"], '2751.9057720045453')

        self.assertEqual(resultsB["ID"], '13')
        self.assertEqual(resultsB["Distance"], '3731.622787359892')

        self.assertEqual(resultsC["ID"], '45')
        self.assertEqual(resultsC["Distance"], '4779.442387720476')

        # now reduce db 1

        adapter.close_DBA()
        adapter.close_DBB()
        adapter.close_DBC()


    def test_invalid_reduce_row(self):
        adapter = DBAdapter()
        queries = DBQueries()

        query_details = {"ID": 1000, "DB": adapter.connect_to_DBA()}
        results = queries.reduceDB(query_details)

        self.assertEqual(results["Name"], None)
        self.assertEqual(results["Photo"], None)

        adapter.close_DBA()

        query_details = {"ID": 10000, "DB": adapter.connect_to_DBB()}
        results = queries.reduceDB(query_details)

        self.assertEqual(results["Name"], None)
        self.assertEqual(results["Photo"], None)

        adapter.close_DBB()

        query_details = {"ID": -1000, "DB": adapter.connect_to_DBC()}
        results = queries.reduceDB(query_details)

        self.assertEqual(results["Name"], None)
        self.assertEqual(results["Photo"], None)

        adapter.close_DBC()

    
    def clearLogs(self):
        con = psycopg2.connect(host=os.getenv('HOST'), port=os.getenv('DB_LOG_PORT'), database=os.getenv('DB'), user=os.getenv('USER'),password=os.getenv('PASSWORD'))
        cur = con.cursor()

        cur.execute("BEGIN; TRUNCATE TABLE public.\"Entry\"; COMMIT;")

        cur.close()
        con.close()

    def test_mod_logs(self):
        adapter = DBAdapter()
        queries = DBQueries()

        test_img = '../../res/trainingData/1_1.jpg'
        second_test_img = '../../res/trainingData/2_1.jpg'

        self.clearLogs()
        
        logs = adapter.connect_to_logs()
        results = queries.check_for_prev_entry(open(test_img, "rb").read(), logs)
        self.assertEqual(len(results), 0)

        queries.add_entry(open(test_img, "rb").read(), logs)
        results = queries.check_for_prev_entry(open(test_img, "rb").read(), logs)
        self.assertEqual(len(results), 1)

        queries.add_entry(open(test_img, "rb").read(), logs)
        results = queries.check_for_prev_entry(open(test_img, "rb").read(), logs)
        self.assertEqual(len(results), 1)

        logs = adapter.connect_to_logs()
        results = queries.check_for_prev_entry(open(second_test_img, "rb").read(), logs)
        self.assertEqual(len(results), 0)

        queries.add_entry(open(second_test_img, "rb").read(), logs)
        results = queries.check_for_prev_entry(open(second_test_img, "rb").read(), logs)
        self.assertEqual(len(results), 1)

        adapter.close_logs()
        self.clearLogs()


if __name__ == '__main__':
    load_dotenv()           # Loads the .env file
    nose2.main()  