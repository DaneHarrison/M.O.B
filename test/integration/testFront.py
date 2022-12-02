import unittest, sys, requests, nose2

sys.path.append('../../src/persistance')

from dbAdapter import DBAdapter

class Front(unittest.TestCase):
    def test_frontfacing_api(self):
        # load image
        # send as JSON to worker
        # wait for a response
        # assert response
        print()


if __name__ == '__main__':
    nose2.main()  