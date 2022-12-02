import unittest, psycopg2, nose2, sys, os

sys.path.append('../../src/persistance')

from dbAdapter import DBAdapter
from dbQueries import DBQueries

class Queries(unittest.TestCase):
    # def test_map_basic(self):
    #     print()


#     def test_reduce_basic(self):
#         print()     #-reguar query


#     def test_reduce_invalid(self):
#         print()     #-try pulling an invalid row

    
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
    nose2.main()  