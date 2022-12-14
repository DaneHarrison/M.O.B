import unittest, sys, nose2

sys.path.append('../../src/logic/worker')
sys.path.append('../../src/persistance')

from request import Request
from dbAdapter import DBAdapter
from dbQueries import DBQueries

class Requests(unittest.TestCase):
    def test_default_values(self):
        req = Request()

        self.assertTrue(isinstance(req.db_adapter, DBAdapter))
        self.assertTrue(isinstance(req.queries, DBQueries))
        self.assertTrue(req.res_DBA == None)
        self.assertTrue(req.res_DBB == None)
        self.assertTrue(req.res_DBB == None)
        self.assertTrue(req.closest == None)


    def test_min_query_details_basic(self):
        req = Request()

        req.res_DBA = {"ID": 1, "Distance": 5}
        req.res_DBB = {"ID": 5, "Distance": 15}
        req.res_DBC = {"ID": 10, "Distance": 25}
        bestRes = req.calc_min_query_details()

        self.assertEqual(bestRes["ID"], 1)
        self.assertEqual(bestRes["DB"], req.db_adapter.connect_to_DBA())

        req.db_adapter.close_DBA()


    def test_min_query_details_complex(self):
        req = Request()

        req.res_DBA = {"ID": 11, "Distance": 5}
        req.res_DBB = {"ID": 2, "Distance": 2}
        req.res_DBC = {"ID": 10, "Distance": 25}
        bestRes = req.calc_min_query_details()

        self.assertEqual(bestRes["ID"], 2)
        self.assertEqual(bestRes["DB"], req.db_adapter.connect_to_DBB())

        req.db_adapter.close_DBB()


    def test_min_query_details_edge(self):
        req = Request()

        req.res_DBA = {"ID": 11, "Distance": 5}
        req.res_DBB = {"ID": 2, "Distance": 5}
        req.res_DBC = {"ID": 10, "Distance": 25}
        bestRes = req.calc_min_query_details()

        self.assertEqual(bestRes["ID"], 11)
        self.assertEqual(bestRes["DB"], req.db_adapter.connect_to_DBA())

        req.db_adapter.close_DBA()


if __name__ == '__main__':
    nose2.main()  