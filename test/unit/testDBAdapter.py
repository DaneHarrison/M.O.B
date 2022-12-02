import unittest, sys, nose2

sys.path.append('../../src/persistance')

from dbAdapter import DBAdapter

class Seed(unittest.TestCase):
    def test_default_values(self):
        adapter = DBAdapter()
        
        self.assertEqual(adapter.DBA, None)
        self.assertEqual(adapter.DBB, None)
        self.assertEqual(adapter.DBC, None)
        self.assertEqual(adapter.logs, None)


    def test_conn_DBA(self):
        adapter = DBAdapter()
        conn = adapter.connect_to_DBA()
        anotherConn = adapter.connect_to_DBA()
        self.assertEqual(conn, anotherConn)

        adapter.close_DBA()


    def test_conn_DBB(self):
        adapter = DBAdapter()
        conn = adapter.connect_to_DBB()
        anotherConn = adapter.connect_to_DBB()
        self.assertEqual(conn, anotherConn)

        adapter.close_DBB()


    def test_conn_DBC(self):
        adapter = DBAdapter()
        conn = adapter.connect_to_DBC()
        anotherConn = adapter.connect_to_DBC()
        self.assertEqual(conn, anotherConn)

        adapter.close_DBC()


    def test_conn_logs(self):
        adapter = DBAdapter()
        conn = adapter.connect_to_logs()
        anotherConn = adapter.connect_to_logs()
        self.assertEqual(conn, anotherConn)

        adapter.close_logs()


if __name__ == '__main__':
    nose2.main() 