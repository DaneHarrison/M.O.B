import unittest, nose2, sys

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

    
    def test_add_entry(self):
        adapter = DBAdapter()
        queries = DBQueries()

        test_img = '../../res/trainingData/1_1.jpg'

        logs = adapter.connect_to_logs()
        queries.check_for_prev_entry(open(test_img, "rb").read(), logs)

        adapter.close_logs()
    # try adding a new value
    # try adding a duplicate value


    def test_check_prev_entry(self):
        print()
    # its in there
    # it is not in there


if __name__ == '__main__':
    nose2.main()  